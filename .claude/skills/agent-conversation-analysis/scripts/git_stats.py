#!/usr/bin/env python
"""
git_stats.py - Collect git statistics for project directories found in session data.

Runs git log commands to detect reverts/fixups, measure file churn, and
cross-validate conversation-based scores.

Usage:
    python git_stats.py --sessions SESSIONS.json [--out OUTPUT.json]

    --sessions FILE  Path to output from collect_sessions.py
    --out FILE       Write JSON output to FILE (default: stdout)

Output format:
    {
      "projects": {
        "C:/path/to/project": {
          "commits_total": 42,
          "commits_recent": 10,
          "reverts_amends": 3,
          "revert_examples": ["revert: foo bar", ...],
          "top_churned_files": [
            {"file": "foo/bar.go", "modifications": 8}
          ],
          "net_lines_added": 120,
          "net_lines_removed": 45,
          "error": null  | "not a git repo" | "git not found"
        }
      }
    }
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_git(args: list, cwd: str) -> tuple[int, str, str]:
    """Run a git command, return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return -1, "", "git not found"
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except Exception as e:
        return -1, "", str(e)


def find_git_root(path: str) -> str | None:
    """Walk up directory tree to find the git root."""
    p = Path(path)
    while p != p.parent:
        if (p / ".git").exists():
            return str(p)
        p = p.parent
    return None


def collect_git_stats(project_path: str, since: str) -> dict:
    """Collect git statistics for a project directory."""
    git_root = find_git_root(project_path)
    if not git_root:
        return {"error": "not a git repo"}

    stats = {
        "git_root": git_root,
        "commits_total": 0,
        "commits_recent": 0,
        "reverts_amends": 0,
        "revert_examples": [],
        "top_churned_files": [],
        "net_lines_added": 0,
        "net_lines_removed": 0,
        "error": None,
    }

    # Total commits
    rc, out, err = run_git(["rev-list", "--count", "HEAD"], git_root)
    if rc == 0:
        stats["commits_total"] = int(out.strip() or 0)
    elif "git not found" in err:
        return {"error": "git not found"}

    # Recent commits (since the analysis period)
    rc, out, err = run_git(
        ["log", "--oneline", f"--since={since}", "--no-merges"],
        git_root,
    )
    if rc == 0:
        lines = [l for l in out.strip().split("\n") if l]
        stats["commits_recent"] = len(lines)

    # Revert/amend/fixup commits
    rc, out, err = run_git(
        ["log", "--oneline", "--grep=revert\\|fixup\\|amend\\|revert:", "-i", f"--since={since}"],
        git_root,
    )
    if rc == 0:
        examples = [l.strip() for l in out.strip().split("\n") if l.strip()]
        stats["reverts_amends"] = len(examples)
        stats["revert_examples"] = examples[:5]

    # File churn: files modified multiple times
    rc, out, err = run_git(
        ["log", "--diff-filter=M", "--name-only", "--format=", f"--since={since}"],
        git_root,
    )
    if rc == 0:
        file_counts: dict[str, int] = {}
        for line in out.strip().split("\n"):
            line = line.strip()
            if line:
                file_counts[line] = file_counts.get(line, 0) + 1
        top_files = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        stats["top_churned_files"] = [
            {"file": f, "modifications": c} for f, c in top_files
        ]

    # Net lines changed (added/removed)
    rc, out, err = run_git(
        ["log", "--numstat", "--format=", f"--since={since}"],
        git_root,
    )
    if rc == 0:
        added = 0
        removed = 0
        for line in out.strip().split("\n"):
            parts = line.split("\t")
            if len(parts) >= 2:
                try:
                    added += int(parts[0])
                    removed += int(parts[1])
                except ValueError:
                    pass
        stats["net_lines_added"] = added
        stats["net_lines_removed"] = removed

    return stats


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sessions", required=True, help="Path to collect_sessions.py output JSON")
    parser.add_argument("--out", default="-", help="Output file path (default: stdout)")
    args = parser.parse_args()

    sessions_data = json.loads(Path(args.sessions).read_text(encoding="utf-8"))
    since = sessions_data.get("since", "1970-01-01T00:00:00+00:00")

    output = {"projects": {}}

    for project_path, project_data in sessions_data.get("projects", {}).items():
        # Resolve the actual filesystem path (may differ on Windows)
        # Try the path directly and some common variations
        candidates = [project_path]
        if project_path.startswith("C:/"):
            candidates.append(project_path.replace("C:/", "C:\\"))

        resolved = None
        for candidate in candidates:
            if Path(candidate).exists():
                resolved = candidate
                break

        if not resolved:
            output["projects"][project_path] = {"error": f"directory not found: {project_path}"}
            continue

        output["projects"][project_path] = collect_git_stats(resolved, since)

    result = json.dumps(output, indent=2, ensure_ascii=False)

    if args.out == "-":
        print(result)
    else:
        Path(args.out).write_text(result, encoding="utf-8")
        print(f"Written to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
