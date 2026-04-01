#!/usr/bin/env python3
"""
analyze.py - Run full data collection pipeline and produce a JSON report.

This is the main entry point. It runs collect_sessions.py and git_stats.py,
then merges the output into a single structured report for Claude to reason about.

Usage:
    python3 analyze.py [--project SLUG] [--days N] [--out OUTPUT.json]
                       [--claude-dirs DIR [DIR ...]]

    --project SLUG      Filter to a specific project slug (partial match ok)
    --days N            Sessions from last N days (default: 0 = all time)
    --out FILE          Write JSON output to FILE (default: sessions_report.json)
    --claude-dirs DIRS  Additional .claude directories (~/.claude is always included)

Typical Claude invocation (from SKILL.md):
    python3 .claude/skills/agent-conversation-analysis/scripts/analyze.py \
        --project gostructure --out <skill-dir>/tmp_replay_data.json

Output is a merged JSON:
    {
      "generated_at": "...",
      "since": "...",
      "projects": {
        "C:/path/to/project": {
          "slug": "...",
          "session_count": N,
          "git": { <git_stats output> },
          "sessions": [ <session objects with stats> ]
        }
      }
    }
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def run_script(script: Path, extra_args: list) -> dict:
    cmd = [sys.executable, str(script)] + extra_args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR running {script.name}:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", default="", help="Filter projects by partial slug match")
    parser.add_argument("--days", type=int, default=0, help="Sessions from last N days (default: 0 = all time)")
    parser.add_argument("--out", default="sessions_report.json", help="Output file (default: sessions_report.json)")
    parser.add_argument("--claude-dirs", nargs="+", default=None,
                        help="Additional .claude directories (~/.claude is always included)")
    args = parser.parse_args()

    import time
    t0 = time.monotonic()

    print(f"Collecting sessions (last {args.days} days)...", file=sys.stderr)

    # Build shared --claude-dirs args for sub-scripts
    claude_dirs_args = []
    if args.claude_dirs:
        claude_dirs_args = ["--claude-dirs"] + args.claude_dirs

    # Step 1: collect sessions
    collect_args = ["--days", str(args.days)]
    if args.project:
        collect_args += ["--project", args.project]
    collect_args += claude_dirs_args

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        sessions_file = tmp.name

    collect_args += ["--out", sessions_file]
    subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "collect_sessions.py")] + collect_args,
        check=True,
    )

    sessions_data = json.loads(Path(sessions_file).read_text(encoding="utf-8"))
    print(f"Found {len(sessions_data['projects'])} projects with sessions.", file=sys.stderr)

    # Step 2: git stats
    print("Collecting git stats...", file=sys.stderr)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        git_file = tmp.name

    subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "git_stats.py"), "--sessions", sessions_file, "--out", git_file],
        check=True,
    )
    git_data = json.loads(Path(git_file).read_text(encoding="utf-8"))

    # Step 3: detect manual edits
    print("Detecting manual edits...", file=sys.stderr)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        manual_file = tmp.name

    subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "detect_manual_edits.py"),
         "--sessions", sessions_file, "--out", manual_file] + claude_dirs_args,
        check=True,
    )
    manual_data = json.loads(Path(manual_file).read_text(encoding="utf-8"))

    # Step 4: detect setup usage (skills, MCP tools triggered)
    print("Detecting setup usage...", file=sys.stderr)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        usage_file = tmp.name

    subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "detect_setup_usage.py"),
         "--sessions", sessions_file, "--out", usage_file] + claude_dirs_args,
        check=True,
    )
    usage_data = json.loads(Path(usage_file).read_text(encoding="utf-8"))

    # Step 5: merge
    merged = {
        "generated_at": sessions_data["generated_at"],
        "since": sessions_data["since"],
        "projects": {},
    }

    for project_path, project_info in sessions_data["projects"].items():
        git_stats = git_data.get("projects", {}).get(project_path, {})
        manual_stats = manual_data.get("projects", {}).get(project_path, {})
        usage_stats = usage_data.get("projects", {}).get(project_path, {})
        merged["projects"][project_path] = {
            **project_info,
            "git": git_stats,
            "manual_edits": manual_stats,
            "setup_usage": usage_stats,
        }

    # Step 6: print summary to stderr for quick sanity check
    total_sessions = sum(p["session_count"] for p in merged["projects"].values())
    total_corrections = sum(
        sum(s["stats"]["corrections"] for s in p["sessions"])
        for p in merged["projects"].values()
    )
    print(f"\nSummary:", file=sys.stderr)
    print(f"  Projects: {len(merged['projects'])}", file=sys.stderr)
    print(f"  Sessions: {total_sessions}", file=sys.stderr)
    print(f"  Corrections detected: {total_corrections}", file=sys.stderr)
    for path, pdata in merged["projects"].items():
        sc = pdata["session_count"]
        gc = pdata.get("git", {}).get("commits_recent", "?")
        rv = pdata.get("git", {}).get("reverts_amends", "?")
        print(f"  {path}: {sc} sessions, {gc} commits, {rv} reverts", file=sys.stderr)

    # Step 7: write output
    duration_seconds = round(time.monotonic() - t0, 1)
    merged["duration_seconds"] = duration_seconds

    out_path = Path(args.out)
    out_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nCompleted in {duration_seconds}s", file=sys.stderr)
    print(f"Report written to: {out_path.resolve()}", file=sys.stderr)

    # Also clean up temp files
    Path(sessions_file).unlink(missing_ok=True)
    Path(git_file).unlink(missing_ok=True)
    Path(manual_file).unlink(missing_ok=True)
    Path(usage_file).unlink(missing_ok=True)


if __name__ == "__main__":
    main()
