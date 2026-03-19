#!/usr/bin/env python3
"""
detect_manual_edits.py - Detect manual edits by comparing
git commit diffs against Claude's Write/Edit tool outputs.

Two detection methods:
1. Line-level: compare committed file diffs against Claude's
   Edit new_string / Write content. Lines in the commit that
   don't appear in any AI output = manual edits.
2. Stale-read: detect Edit tool failures where old_string
   wasn't found (someone edited the file between Read and Edit).

Usage:
    python3 detect_manual_edits.py --sessions SESSIONS.json [--out OUTPUT.json]

Output format:
    {
      "projects": {
        "<project-path>": {
          "ai_edited_files": ["path/to/file.py", ...],
          "committed_files": ["path/to/file.py", ...],
          "manual_edits": {
            "path/to/file.py": {
              "committed_lines_not_in_ai": 12,
              "total_committed_lines": 30
            }
          },
          "manual_edit_count": N,
          "stale_read_failures": 3,
          "stale_read_examples": ["Edit failed on foo.py: ..."]
        }
      }
    }
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def extract_ai_outputs(sessions_data: dict) -> dict:
    """Extract Claude's Write/Edit outputs from session JSONL files.

    Returns {project_path: {
        "files": {filepath: set(content_lines)},
        "stale_reads": [error messages],
    }}.
    """
    claude_home = Path.home() / ".claude"
    result = {}

    for project_path, project_info in sessions_data.get("projects", {}).items():
        ai_files = {}   # filepath -> set of lines AI wrote
        stale_reads = []
        slug = project_info.get("slug", "")
        project_dir = claude_home / "projects" / slug

        for session in project_info.get("sessions", []):
            sid = session.get("session_id", "")
            jsonl_path = project_dir / f"{sid}.jsonl"
            if not jsonl_path.exists():
                continue

            with open(jsonl_path, encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    msg_type = obj.get("type")

                    # Extract AI Write/Edit tool calls
                    if msg_type == "assistant":
                        content = obj.get("message", {}).get("content", [])
                        if not isinstance(content, list):
                            continue
                        for block in content:
                            if not isinstance(block, dict):
                                continue
                            if block.get("type") != "tool_use":
                                continue
                            name = block.get("name", "")
                            inp = block.get("input", {})
                            file_path = inp.get("file_path", "")
                            if not file_path:
                                continue

                            rel = _to_relative(file_path, project_path)
                            if rel not in ai_files:
                                ai_files[rel] = set()

                            if name == "Write":
                                text = inp.get("content", "")
                                ai_files[rel].update(
                                    l.strip() for l in text.splitlines() if l.strip()
                                )
                            elif name == "Edit":
                                text = inp.get("new_string", "")
                                ai_files[rel].update(
                                    l.strip() for l in text.splitlines() if l.strip()
                                )

                    # Detect stale-read Edit failures
                    if msg_type == "user":
                        content = obj.get("message", {}).get("content", [])
                        if not isinstance(content, list):
                            continue
                        for block in content:
                            if not isinstance(block, dict):
                                continue
                            if block.get("type") != "tool_result":
                                continue
                            if not block.get("is_error"):
                                continue
                            err_text = str(block.get("content", ""))
                            if "not found in file" in err_text.lower():
                                stale_reads.append(err_text[:200])

        result[project_path] = {
            "files": ai_files,
            "stale_reads": stale_reads,
        }

    return result


def _to_relative(file_path: str, project_path: str) -> str:
    """Convert absolute file path to relative from project root."""
    fp = file_path.replace("\\", "/")
    pp = project_path.replace("\\", "/").rstrip("/")
    if fp.lower().startswith(pp.lower()):
        return fp[len(pp):].lstrip("/")
    return fp


def get_committed_diffs(project_path: str, since: str) -> dict:
    """Get per-file committed diff lines from git.

    Returns {filepath: {"added_lines": set, "total_added": int}}.
    """
    p = Path(project_path.replace("/", "\\"))
    git_root = None
    while p != p.parent:
        if (p / ".git").exists():
            git_root = str(p)
            break
        p = p.parent

    if not git_root:
        return {}

    try:
        result = subprocess.run(
            ["git", "log", "-p", "--diff-filter=AM",
             "--no-color", f"--since={since}", "--format="],
            cwd=git_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        if result.returncode != 0:
            return {}
    except Exception:
        return {}

    files = {}
    current_file = None

    for raw_line in result.stdout.splitlines():
        if raw_line.startswith("diff --git"):
            # Extract filename from "diff --git a/foo b/foo"
            parts = raw_line.split(" b/", 1)
            current_file = parts[1] if len(parts) > 1 else None
            if current_file and current_file not in files:
                files[current_file] = {"added_lines": set(), "total_added": 0}
        elif raw_line.startswith("+") and not raw_line.startswith("+++"):
            if current_file and current_file in files:
                added = raw_line[1:].strip()
                if added:
                    files[current_file]["added_lines"].add(added)
                    files[current_file]["total_added"] += 1

    return files


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--sessions", required=True,
        help="Path to collect_sessions.py output JSON",
    )
    parser.add_argument(
        "--out", default="-",
        help="Output file path (default: stdout)",
    )
    args = parser.parse_args()

    sessions_data = json.loads(
        Path(args.sessions).read_text(encoding="utf-8")
    )
    since = sessions_data.get("since", "1970-01-01T00:00:00+00:00")

    ai_data = extract_ai_outputs(sessions_data)

    output = {"projects": {}}

    for project_path in sessions_data.get("projects", {}):
        ai_info = ai_data.get(project_path, {"files": {}, "stale_reads": []})
        ai_files = ai_info["files"]
        stale_reads = ai_info["stale_reads"]

        committed_diffs = get_committed_diffs(project_path, since)

        manual_edits = {}
        for filepath, diff_info in committed_diffs.items():
            ai_lines = ai_files.get(filepath, set())
            committed_lines = diff_info["added_lines"]

            # Lines in commit that don't match any AI output
            manual_lines = committed_lines - ai_lines
            if manual_lines:
                manual_edits[filepath] = {
                    "committed_lines_not_in_ai": len(manual_lines),
                    "total_committed_lines": diff_info["total_added"],
                }

        output["projects"][project_path] = {
            "ai_edited_files": sorted(ai_files.keys()),
            "committed_files": sorted(committed_diffs.keys()),
            "manual_edits": manual_edits,
            "manual_edit_count": len(manual_edits),
            "stale_read_failures": len(stale_reads),
            "stale_read_examples": stale_reads[:5],
        }

        # Summary
        total_manual_lines = sum(
            v["committed_lines_not_in_ai"] for v in manual_edits.values()
        )
        print(
            f"{project_path}: "
            f"{len(ai_files)} AI-edited files, "
            f"{len(committed_diffs)} committed files, "
            f"{len(manual_edits)} files with manual edits "
            f"({total_manual_lines} lines), "
            f"{len(stale_reads)} stale-read failures",
            file=sys.stderr,
        )
        for filepath, info in sorted(
            manual_edits.items(),
            key=lambda x: x[1]["committed_lines_not_in_ai"],
            reverse=True,
        )[:5]:
            n = info["committed_lines_not_in_ai"]
            t = info["total_committed_lines"]
            print(f"  {filepath}: {n}/{t} lines manual", file=sys.stderr)

    result = json.dumps(output, indent=2, ensure_ascii=False)

    if args.out == "-":
        print(result)
    else:
        Path(args.out).write_text(result, encoding="utf-8")
        print(f"Written to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
