#!/usr/bin/env python3
"""
git_stats.py - Collect git statistics for project directories found in session data.

Runs git log commands to detect reverts/fixups, measure file churn, and
cross-validate conversation-based scores.

Handles three cases:
- Project directory is a git repo: collects stats directly.
- Project directory contains git sub-repos: collects stats per sub-repo.
- Both (e.g. ~/workspace is a git repo with nested sub-repos).

Usage:
    python3 git_stats.py --sessions SESSIONS.json [--out OUTPUT.json]

    --sessions FILE  Path to output from collect_sessions.py
    --out FILE       Write JSON output to FILE (default: stdout)

Output format:
    {
      "projects": {
        "/path/to/project": {
          "commits_total": 42,
          "commits_recent": 10,
          "reverts_amends": 3,
          "revert_examples": ["revert: foo bar", ...],
          "top_churned_files": [
            {"file": "foo/bar.go", "modifications": 8}
          ],
          "net_lines_added": 120,
          "net_lines_removed": 45,
          "sub_repos": {              // present when sub-repos detected
            "/path/to/sub": { ...same fields... }
          },
          "sub_repos_total_commits": N,
          "error": null
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


def find_sub_repos(project_path: str, max_depth: int = 4) -> list[str]:
    """Find git sub-repos inside project_path (not the project itself).

    Useful for meta-repos like ~/workspace that contain many sub-repos.
    Returns a list of sub-repo root paths.
    """
    project = Path(project_path)
    sub_repos = []
    try:
        # This uses the Unix `find` command, which works in Git Bash
        # (not in Windows cmd, but that is OK).
        result = subprocess.run(
            ["find", str(project), "-maxdepth", str(max_depth),
             "-name", ".git", "-type", "d"],
            capture_output=True, text=True, timeout=10,
        )
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            repo_root = str(Path(line).parent)
            # Skip the project itself
            if repo_root != str(project):
                sub_repos.append(repo_root)
    except Exception:
        pass
    return sub_repos


def _empty_stats(git_root: str = "") -> dict:
    return {
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


def _collect_single_repo_stats(git_root: str, since: str) -> dict:
    """Collect git stats from a single git repo root."""
    stats = _empty_stats(git_root)

    # Total commits
    rc, out, err = run_git(["rev-list", "--count", "HEAD"], git_root)
    if rc == 0:
        stats["commits_total"] = int(out.strip() or 0)
    elif "git not found" in err:
        return {"error": "git not found"}

    # Recent commits
    rc, out, err = run_git(
        ["log", "--oneline", f"--since={since}", "--no-merges"],
        git_root,
    )
    if rc == 0:
        lines = [line for line in out.strip().split("\n") if line]
        stats["commits_recent"] = len(lines)

    # Revert/amend/fixup commits
    rc, out, err = run_git(
        ["log", "--oneline", "--grep=revert\\|fixup\\|amend\\|revert:", "-i", f"--since={since}"],
        git_root,
    )
    if rc == 0:
        examples = [line.strip() for line in out.strip().split("\n") if line.strip()]
        stats["reverts_amends"] = len(examples)
        stats["revert_examples"] = examples[:5]

    # File churn
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

    # Net lines changed
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


def collect_git_stats(project_path: str, since: str) -> dict:
    """Collect git statistics for a project directory.

    The project directory may be:
    - A git repo itself (collect stats directly)
    - A parent directory containing git sub-repos (collect per sub-repo)
    - Both (a git repo with nested sub-repos, e.g. ~/workspace)
    """
    git_root = find_git_root(project_path)

    if git_root:
        stats = _collect_single_repo_stats(git_root, since)
    else:
        stats = _empty_stats()

    # Check for sub-repos regardless of whether the parent is a git repo
    sub_repos = find_sub_repos(project_path)
    if sub_repos:
        sub_stats = {}
        for sub_path in sub_repos:
            sub = _collect_single_repo_stats(sub_path, since)
            if sub.get("commits_recent", 0) > 0:
                sub_stats[sub_path] = sub
        if sub_stats:
            stats["sub_repos"] = sub_stats
            stats["sub_repos_total_commits"] = sum(
                s.get("commits_recent", 0) for s in sub_stats.values()
            )
            stats["sub_repos_total_added"] = sum(
                s.get("net_lines_added", 0) for s in sub_stats.values()
            )
            stats["sub_repos_total_removed"] = sum(
                s.get("net_lines_removed", 0) for s in sub_stats.values()
            )

    if not git_root and not sub_repos:
        return {"error": "not a git repo and no sub-repos found"}

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
