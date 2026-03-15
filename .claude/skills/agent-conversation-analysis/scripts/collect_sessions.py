#!/usr/bin/env python
"""
collect_sessions.py - Collect and parse Claude session data from ~/.claude

Reads JSONL session files from ~/.claude/projects/ and outputs structured
session data ready for scoring. Also cross-references ~/.claude/history.jsonl
for session metadata.

Usage:
    python collect_sessions.py [--project SLUG] [--days N] [--out OUTPUT.json]

    --project SLUG  Filter to a specific project slug (partial match ok).
                    Example: "gostructure" or "daominah"
    --days N        Only include sessions from the last N days (default: 30)
    --out FILE      Write JSON output to FILE (default: stdout)

Output format:
    {
      "generated_at": "2026-03-14T...",
      "projects": {
        "C:/Users/.../gostructure": {
          "slug": "C--Users-...-gostructure",
          "session_count": 5,
          "sessions": [ <session objects> ]
        }
      }
    }

Each session object:
    {
      "session_id": "...",
      "cwd": "C:/...",
      "git_branch": "main",
      "started_at": "2026-03-14T...",
      "ended_at": "2026-03-14T...",
      "duration_minutes": 12.3,
      "messages": [
        {
          "role": "user" | "assistant",
          "content": "...",   # text only, thinking blocks stripped
          "timestamp": "2026-03-14T...",
          "uuid": "..."
        }
      ],
      "stats": {
        "user_messages": 5,
        "assistant_messages": 8,
        "corrections": 2,
        "correction_examples": ["no, I meant...", "try again"],
        "setup_gaps": 1,
        "setup_gap_examples": ["here is the relevant code: ...]
      }
    }
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


# Phrases that indicate the user is correcting or frustrated with Claude
CORRECTION_PHRASES = [
    "no,", "no.", "nope", "wrong", "that's wrong", "thats wrong",
    "not what i asked", "not what i wanted", "try again",
    "revert", "undo", "that's not", "thats not",
    "i meant", "i mean ", "actually,", "wait,",
    "you misunderstood", "not correct", "incorrect",
    "please fix", "fix this", "this is wrong",
    "not work", "doesn't work", "doesnt work",
    "i said",
    # Frustration signals
    "wtf", "wth", "the fuck", "the hell", "shit",
]

# Patterns that indicate the user is pasting context Claude could have fetched
SETUP_GAP_PATTERNS = [
    "here is the", "here's the", "the file is at", "the path is",
    "below is the", "this is the content", "copied from",
    "pasting the", "here are the", "let me give you",
    "for context,", "for reference,", "fyi,",
]

# Long user messages often indicate pastes (threshold in characters)
PASTE_LENGTH_THRESHOLD = 500


def claude_home() -> Path:
    return Path.home() / ".claude"


def slugify_path(path: str) -> str:
    """Convert a filesystem path to a ~/.claude/projects/ slug."""
    # Claude replaces path separators with --
    return path.replace("\\", "-").replace("/", "-").replace(":", "-").lstrip("-")


def load_history(since: datetime) -> dict:
    """Load history.jsonl and return {sessionId: {project, timestamp}} for sessions since `since`."""
    history_file = claude_home() / "history.jsonl"
    result = {}
    if not history_file.exists():
        return result
    with open(history_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts_ms = obj.get("timestamp", 0)
            ts = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
            if ts < since:
                continue
            sid = obj.get("sessionId")
            if sid and sid not in result:
                result[sid] = {
                    "project": obj.get("project", ""),
                    "timestamp": ts.isoformat(),
                }
    return result


def extract_text(content) -> str:
    """Extract plain text from message content (string or block list)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                btype = block.get("type", "")
                if btype == "text":
                    parts.append(block.get("text", ""))
                elif btype == "thinking":
                    pass  # skip thinking blocks
                elif btype == "tool_use":
                    pass  # skip tool calls
                elif btype == "tool_result":
                    # sometimes results contain text
                    rc = block.get("content", "")
                    if isinstance(rc, str):
                        parts.append(rc)
        return "\n".join(parts)
    return ""


def is_correction(text: str) -> bool:
    """Return True if the message looks like a user correction."""
    lower = text.lower().strip()
    for phrase in CORRECTION_PHRASES:
        if phrase in lower:
            return True
    return False


def is_setup_gap(text: str) -> bool:
    """Return True if the message looks like the user pasting context."""
    lower = text.lower().strip()
    for pattern in SETUP_GAP_PATTERNS:
        if pattern in lower:
            return True
    # Long message = likely a paste
    if len(text) > PASTE_LENGTH_THRESHOLD and "```" in text:
        return True
    return False


def parse_session_file(jsonl_path: Path) -> list:
    """Parse a session JSONL file into a list of message dicts."""
    messages = []
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
            if msg_type not in ("user", "assistant"):
                continue
            message = obj.get("message", {})
            role = message.get("role", msg_type)
            raw_content = message.get("content", "")

            # Skip tool-result user messages (skill injections, hook outputs, etc.)
            # These are user-role but not actual human input.
            if role == "user" and isinstance(raw_content, list):
                if all(
                    isinstance(b, dict) and b.get("type") in ("tool_result", "tool_use")
                    for b in raw_content
                    if isinstance(b, dict)
                ):
                    continue

            content = extract_text(raw_content)
            if not content:
                continue
            messages.append({
                "role": role,
                "content": content,
                "timestamp": obj.get("timestamp", ""),
                "uuid": obj.get("uuid", ""),
                "cwd": obj.get("cwd", ""),
                "git_branch": obj.get("gitBranch", ""),
                "session_id": obj.get("sessionId", ""),
            })
    return messages


def compute_stats(messages: list) -> dict:
    user_msgs = [m for m in messages if m["role"] == "user"]
    assistant_msgs = [m for m in messages if m["role"] == "assistant"]

    corrections = []
    setup_gaps = []
    for m in user_msgs:
        text = m["content"]
        if is_correction(text):
            corrections.append(text[:200])
        if is_setup_gap(text):
            setup_gaps.append(text[:200])

    return {
        "user_messages": len(user_msgs),
        "assistant_messages": len(assistant_msgs),
        "corrections": len(corrections),
        "correction_examples": corrections[:3],
        "setup_gaps": len(setup_gaps),
        "setup_gap_examples": setup_gaps[:3],
    }


def collect_project(project_slug: str, since: datetime, history_sessions: set) -> dict:
    """Collect all sessions for a given project slug."""
    project_dir = claude_home() / "projects" / project_slug
    if not project_dir.exists():
        return {}

    sessions = []
    for jsonl_file in sorted(project_dir.glob("*.jsonl")):
        session_id = jsonl_file.stem
        # Check modification time as quick filter
        mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime, tz=timezone.utc)
        if mtime < since:
            continue

        messages = parse_session_file(jsonl_file)
        if not messages:
            continue

        # Timestamps
        timestamps = [m["timestamp"] for m in messages if m["timestamp"]]
        started_at = min(timestamps) if timestamps else ""
        ended_at = max(timestamps) if timestamps else ""

        # Duration
        duration_minutes = None
        if started_at and ended_at:
            try:
                def parse_ts(ts):
                    # handle both ISO and ms-epoch formats
                    if isinstance(ts, (int, float)):
                        return datetime.fromtimestamp(ts / 1000, tz=timezone.utc)
                    return datetime.fromisoformat(ts.replace("Z", "+00:00"))
                t0 = parse_ts(started_at)
                t1 = parse_ts(ended_at)
                duration_minutes = round((t1 - t0).total_seconds() / 60, 1)
            except Exception:
                pass

        # CWD and branch from first message that has them
        cwd = next((m["cwd"] for m in messages if m.get("cwd")), "")
        git_branch = next((m["git_branch"] for m in messages if m.get("git_branch")), "")

        stats = compute_stats(messages)

        sessions.append({
            "session_id": session_id,
            "cwd": cwd,
            "git_branch": git_branch,
            "started_at": started_at,
            "ended_at": ended_at,
            "duration_minutes": duration_minutes,
            "stats": stats,
            "messages": [
                {"role": m["role"], "content": m["content"], "timestamp": m["timestamp"]}
                for m in messages
            ],
        })

    sessions.sort(key=lambda s: s["started_at"], reverse=True)

    # Use actual cwd from sessions as the canonical project path (more reliable than slug parsing)
    project_path = next(
        (s["cwd"].replace("\\", "/") for s in sessions if s.get("cwd")),
        project_slug,  # fallback to slug if no cwd found
    )

    return {
        "slug": project_slug,
        "path": project_path,
        "session_count": len(sessions),
        "sessions": sessions,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", default="", help="Filter projects by partial slug match")
    parser.add_argument("--days", type=int, default=30, help="Include sessions from the last N days (default: 30)")
    parser.add_argument("--out", default="-", help="Output file path (default: stdout)")
    args = parser.parse_args()

    since = datetime.now(tz=timezone.utc) - timedelta(days=args.days)

    # Load history for session cross-reference
    history = load_history(since)
    history_session_ids = set(history.keys())

    # Find matching project directories
    projects_dir = claude_home() / "projects"
    if not projects_dir.exists():
        print("ERROR: ~/.claude/projects/ not found", file=sys.stderr)
        sys.exit(1)

    project_slugs = [
        d.name for d in projects_dir.iterdir()
        if d.is_dir() and (not args.project or args.project.lower() in d.name.lower())
    ]

    output = {
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "since": since.isoformat(),
        "projects": {},
    }

    for slug in sorted(project_slugs):
        data = collect_project(slug, since, history_session_ids)
        if data and data.get("session_count", 0) > 0:
            output["projects"][data["path"]] = data

    result = json.dumps(output, indent=2, ensure_ascii=False)

    if args.out == "-":
        print(result)
    else:
        Path(args.out).write_text(result, encoding="utf-8")
        print(f"Written to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
