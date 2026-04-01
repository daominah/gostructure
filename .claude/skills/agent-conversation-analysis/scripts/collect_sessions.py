#!/usr/bin/env python3
"""
collect_sessions.py - Collect and parse Claude session data from ~/.claude

Reads JSONL session files from ~/.claude/projects/ and outputs structured
session data ready for scoring. Also cross-references ~/.claude/history.jsonl
for session metadata.

Supports multiple .claude directories so you can include session data copied
from other machines. Repo paths from other machines will not exist locally,
so git-dependent steps will gracefully skip those projects.

Usage:
    python3 collect_sessions.py [--project SLUG] [--days N] [--out OUTPUT.json]
                                [--claude-dirs DIR [DIR ...]]

    --project SLUG      Filter to a specific project slug (partial match ok).
                        Example: "gostructure" or "daominah"
    --days N            Sessions from last N days (default: 0 = all time)
    --out FILE          Write JSON output to FILE (default: stdout)
    --claude-dirs DIRS  One or more .claude directories to scan
                        (default: ~/.claude)

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
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


# Regex patterns for correction detection (case-insensitive, applied to full message).
# Start-anchored patterns reduce false positives from mid-sentence matches.
# Updated 2026-04-01 based on analysis of 5440 real user messages (Mac + Windows).
CORRECTION_REGEXES = [
    re.compile(p, re.I) for p in [
        # Direct disagreement
        r"^no[,.\s!]",
        r"^nah",
        r"^wrong",
        r"^actually[,.\s]",
        r"^wait[\s,!]",
        r"^stop[\s,.!]",
        r"^revert",
        r"^i mean[,\s]",
        r"^not (really|quite|happy|smooth|work)",
        r"^you (edit|review|delete|did).*wrong",
        r"^screw it",
        # Frustration
        r"^(wtf|wth|what the (hell|fuck))",
        r"^(shit|fuck|holy ?shit)",
        r"^(aggg|huh)[,.\s]",
        r"^why (the hell|the fuck|did you skip|are you)",
        r"remember my.*(writ|style|rule)",
    ]
]

# Plain substring phrases (case-insensitive `in` check).
# These work well without regex because they are multi-word
# and unlikely to appear in non-correction contexts.
CORRECTION_PHRASES = [
    "nope", "that's wrong", "thats wrong",
    "not what i asked", "not what i wanted",
    "that's not", "thats not",
    "i meant", "my meaning",
    "you misunderstood", "not correct", "incorrect",
    "please fix", "fix this", "this is wrong",
    "not work", "doesn't work", "doesnt work",
    "i said", "undo", "revert",
    # Mismatch signals
    "hmm",
]

# Patterns that indicate the user is pasting context Claude could have fetched
SETUP_GAP_PATTERNS = [
    "here is the", "here's the", "the file is at", "the path is",
    "below is the", "this is the content", "copied from",
    "pasting the", "here are the", "let me give you",
    "for context,", "for reference,", "fyi,",
]

# Minimum message length (chars) for structural paste detection.
# Messages shorter than this are only checked against SETUP_GAP_PATTERNS keywords.
# Messages at or above this AND matching _looks_like_pasted_data() count as setup gaps.
# Based on message length distribution: p75=88, p90=138, p95=178, p99=414.
# 128 catches most pasted data (JSON, logs, SQL results) while relying on
# _looks_like_pasted_data() to filter out normal long questions.
PASTE_LENGTH_THRESHOLD = 128


def default_claude_dirs() -> list[Path]:
    return [Path.home() / ".claude"]


def slugify_path(path: str) -> str:
    """Convert a filesystem path to a ~/.claude/projects/ slug."""
    # Claude replaces path separators with --
    return path.replace("\\", "-").replace("/", "-").replace(":", "-").lstrip("-")


def load_history(since: datetime, claude_dirs: list[Path] = None) -> dict:
    """Load history.jsonl from all claude dirs.

    Returns {sessionId: {project, timestamp}} for sessions since `since`.
    """
    if claude_dirs is None:
        claude_dirs = default_claude_dirs()
    result = {}
    for claude_dir in claude_dirs:
        history_file = claude_dir / "history.jsonl"
        if not history_file.exists():
            continue
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
                        "source_dir": str(claude_dir),
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


def _is_system_injected(text: str) -> bool:
    """Return True if the message is system-injected content, not human input.

    Catches: skill auto-loads, task-notifications, command outputs,
    context summaries, and local-command messages.
    """
    stripped = text.strip()
    # Skill auto-load messages
    if stripped.startswith("Base directory for this skill:"):
        return True
    # Task notifications from subagents
    if "<task-notification>" in stripped:
        return True
    # Command invocations and outputs (slash commands, local commands)
    if stripped.startswith("<command-") or stripped.startswith("<local-command"):
        return True
    # Context continuation summaries
    if stripped.startswith("This session is being continued from a previous"):
        return True
    # Tool loaded messages
    if stripped == "Tool loaded.":
        return True
    return False


def _is_grammar_check_request(text: str) -> bool:
    """Return True if the user is asking for grammar help, not correcting AI.

    Examples: "grammar?", "check grammar", "fix grammar", "smooth grammar".
    """
    lower = text.lower().strip()
    # Short messages that are grammar-check requests
    grammar_patterns = [
        "grammar?", "grammar.", "grammar,",
        "check grammar", "fix grammar", "correct grammar",
        "smooth grammar", "rephrase grammar", "rephase grammar",
        "smooth?", "smoother?", "shorter?", "sorter?",
    ]
    for pattern in grammar_patterns:
        if pattern in lower:
            return True
    return False


def is_correction(text: str) -> bool:
    """Return True if the message looks like a user correction.

    Excludes system-injected messages and grammar-check requests.
    Checks regex patterns first (start-anchored, lower FP),
    then falls back to plain substring phrases.
    """
    if _is_system_injected(text):
        return False
    if _is_grammar_check_request(text):
        return False
    lower = text.lower().strip()
    for rx in CORRECTION_REGEXES:
        if rx.search(lower):
            return True
    for phrase in CORRECTION_PHRASES:
        if phrase in lower:
            return True
    return False


def _looks_like_pasted_data(text: str) -> bool:
    """Return True if the text looks like pasted structured data.

    Detects JSON, log output, test output, SQL results, structured tables,
    and other data the user likely copied from a terminal, file, or UI.
    """
    lines = text.strip().split("\n")
    stripped = text.strip()
    indicators = 0

    # JSON-like data: array or object at start, or "result [", "result {"
    if stripped.startswith(("[", "{")):
        indicators += 2
    elif re.search(r'(?:result|output|response|data)\s*[\[{]', stripped[:200], re.IGNORECASE):
        indicators += 2

    # Repeated JSON keys pattern ("key": "value") appearing multiple times
    json_key_count = len(re.findall(r'"[^"]+"\s*:', text))
    if json_key_count >= 4:
        indicators += 2

    # Log output patterns (timestamps, level=, msg=)
    log_lines = sum(1 for line in lines if "level=" in line or "msg=" in line)
    if log_lines >= 2:
        indicators += 2

    # Test output (=== RUN, --- PASS, --- FAIL)
    if any(line.strip().startswith(("=== RUN", "--- PASS", "--- FAIL")) for line in lines):
        indicators += 2

    # Repeated pipe-separated structure (table data)
    pipe_lines = sum(1 for line in lines if line.count("|") >= 2)
    if pipe_lines >= 3:
        indicators += 1

    # Code fences
    if "```" in text:
        indicators += 1

    # Many indented lines (structured content, 3+ lines minimum)
    if len(lines) >= 3:
        indented = sum(1 for line in lines if line.startswith(("  ", "\t")))
        if indented > len(lines) * 0.5:
            indicators += 1

    return indicators >= 2


def is_setup_gap(text: str) -> bool:
    """Return True if the message looks like the user pasting context.

    Excludes system-injected messages (skill content, task notifications).
    Detects both keyword-based pastes and structural patterns in long messages.
    """
    if _is_system_injected(text):
        return False
    lower = text.lower().strip()
    for pattern in SETUP_GAP_PATTERNS:
        if pattern in lower:
            return True
    # Long message with structural patterns = likely a paste
    if len(text) > PASTE_LENGTH_THRESHOLD and _looks_like_pasted_data(text):
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


def collect_project(project_slug: str, since: datetime, history_sessions: set,
                    claude_dirs: list[Path] = None) -> dict:
    """Collect all sessions for a given project slug.

    Searches for the project slug across all provided claude_dirs.
    """
    if claude_dirs is None:
        claude_dirs = default_claude_dirs()

    # Find all project dirs matching this slug across all claude homes
    project_dirs = []
    for cd in claude_dirs:
        candidate = cd / "projects" / project_slug
        if candidate.exists():
            project_dirs.append(candidate)

    if not project_dirs:
        return {}

    sessions = []
    seen_session_ids = set()
    for project_dir in project_dirs:
        for jsonl_file in sorted(project_dir.glob("*.jsonl")):
            session_id = jsonl_file.stem
            if session_id in seen_session_ids:
                continue
            seen_session_ids.add(session_id)
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


def parse_claude_dirs(raw: list[str] | None) -> list[Path]:
    """Parse --claude-dirs argument into a list of Path objects."""
    if not raw:
        return default_claude_dirs()
    return [Path(d).expanduser() for d in raw]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", default="", help="Filter projects by partial slug match")
    parser.add_argument("--days", type=int, default=0,
                        help="Include sessions from the last N days (default: 0 = all time)")
    parser.add_argument("--out", default="-", help="Output file path (default: stdout)")
    parser.add_argument("--claude-dirs", nargs="+", default=None,
                        help="One or more .claude directories to scan (default: ~/.claude)")
    args = parser.parse_args()

    claude_dirs = parse_claude_dirs(args.claude_dirs)

    if args.days > 0:
        since = datetime.now(tz=timezone.utc) - timedelta(days=args.days)
    else:
        since = datetime(2020, 1, 1, tzinfo=timezone.utc)

    # Load history for session cross-reference
    history = load_history(since, claude_dirs)
    history_session_ids = set(history.keys())

    # Find matching project directories across all claude dirs
    project_slugs = set()
    found_any = False
    for cd in claude_dirs:
        projects_dir = cd / "projects"
        if not projects_dir.exists():
            print(f"WARN: {projects_dir} not found, skipping", file=sys.stderr)
            continue
        found_any = True
        for d in projects_dir.iterdir():
            if d.is_dir() and (not args.project or args.project.lower() in d.name.lower()):
                project_slugs.add(d.name)

    if not found_any:
        print("ERROR: no .claude/projects/ found in any provided directory", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {len(claude_dirs)} .claude dir(s), "
          f"{len(project_slugs)} project slug(s) found", file=sys.stderr)

    output = {
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "since": since.isoformat(),
        "claude_dirs": [str(cd) for cd in claude_dirs],
        "projects": {},
    }

    for slug in sorted(project_slugs):
        data = collect_project(slug, since, history_session_ids, claude_dirs)
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
