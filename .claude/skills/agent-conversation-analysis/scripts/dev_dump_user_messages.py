#!/usr/bin/env python3
"""DEV TOOL: Dump all user messages for manual review.

This script is NOT part of the analysis pipeline. It is a development helper
used when editing this skill to discover new correction/mismatch keywords
from real conversation data. The output needs human or LLM judgment to
interpret (the output is input for dev_suggest_correction_phrases.md workflow).

Usage:
    python3 dev_dump_user_messages.py [--claude-dirs DIR [DIR ...]] [--out OUTPUT]

Default output: tmp_dump_user_messages_<timestamp>.md in the skill directory.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from collections import Counter

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent


def _default_output() -> Path:
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%dT%H%M")
    return SKILL_DIR / f"tmp_dump_user_messages_{ts}.md"

# Truncate displayed messages at this length
DISPLAY_LIMIT = 256


def extract_text(msg_obj) -> str:
    """Extract plain text from a JSONL line, handling the Claude Code format.

    Claude Code JSONL lines have: {type, message: {role, content}, ...}
    Content can be a string or a list of blocks.
    """
    # Get the inner message object
    inner = msg_obj.get("message")
    if not inner:
        # Fallback: some lines use top-level content (system messages)
        content = msg_obj.get("content", "")
        if isinstance(content, str):
            return content
        return ""

    content = inner.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                btype = block.get("type", "")
                if btype == "text":
                    parts.append(block.get("text", ""))
        return "\n".join(parts)
    return ""


def extract_tool_names(msg_obj) -> list[str]:
    """Extract tool names from an assistant message's content blocks."""
    inner = msg_obj.get("message", {})
    content = inner.get("content", "")
    if not isinstance(content, list):
        return []
    tools = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "tool_use":
            name = block.get("name", "")
            # For Edit/Write, try to grab the filename from input
            inp = block.get("input", {})
            if name in ("Edit", "Write", "Read") and isinstance(inp, dict):
                fpath = inp.get("file_path", "")
                if fpath:
                    name = f"{name}({Path(fpath).name})"
            tools.append(name)
    return tools


def _meaningful_line(text: str, from_end: bool = False) -> str:
    """Return the first (or last) non-empty, non-formatting line from text.

    Skips blank lines, markdown fences, horizontal rules, and pipe-only lines.
    """
    lines = text.split("\n")
    if from_end:
        lines = reversed(lines)
    skip_prefixes = ("```", "---", "===", "| ", "|--")
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if any(stripped.startswith(p) for p in skip_prefixes):
            continue
        if stripped == "|":
            continue
        return stripped
    return ""


def is_system_injected(text: str) -> bool:
    """Return True if the message is system-injected, not actual human input."""
    stripped = text.strip()
    if not stripped:
        return True
    # Skill auto-load messages
    if stripped.startswith("Base directory for this skill:"):
        return True
    # Task notifications from subagents
    if "<task-notification>" in stripped:
        return True
    # Command invocations and outputs
    if stripped.startswith("<command-") or stripped.startswith("<local-command"):
        return True
    if "<command-name>" in stripped and "<command-message>" in stripped:
        return True
    # Context continuation summaries
    if stripped.startswith("This session is being continued"):
        return True
    # Tool loaded messages
    if stripped == "Tool loaded.":
        return True
    # System reminders
    if "<system-reminder>" in stripped:
        return True
    return False


def _truncate(text: str) -> str:
    """Truncate to DISPLAY_LIMIT, collapsing newlines."""
    flat = text.replace("\n", " ↵ ")
    if len(flat) <= DISPLAY_LIMIT:
        return flat
    return flat[:DISPLAY_LIMIT] + "..."


def collect_bash_aliases() -> dict[str, str]:
    """Collect user's bash aliases. Returns {alias: meaning}."""
    import subprocess
    try:
        result = subprocess.run(
            ["bash", "-ic", "alias"],
            capture_output=True, text=True, timeout=5,
        )
        aliases = {}
        for line in result.stdout.strip().splitlines():
            # Format: alias name='value'
            if line.startswith("alias "):
                line = line[6:]
            eq = line.find("=")
            if eq > 0:
                name = line[:eq].strip()
                value = line[eq + 1:].strip().strip("'\"")
                aliases[name] = value
        return aliases
    except Exception:
        return {}


def scan_all_sessions(claude_dirs: list[Path]):
    messages = []  # list of dicts with text, project, session, agent_context
    total_user_messages = 0

    jsonl_files = []
    for cd in claude_dirs:
        projects_dir = cd / "projects"
        if projects_dir.exists():
            jsonl_files.extend(sorted(projects_dir.rglob("*.jsonl")))
    jsonl_files = [f for f in jsonl_files if "subagents" not in str(f)]

    print(f"Scanning {len(jsonl_files)} session files "
          f"from {len(claude_dirs)} .claude dir(s)...", file=sys.stderr)

    for filepath in jsonl_files:
        session_name = filepath.stem[:12]
        project = filepath.parent.name
        try:
            # Two-pass: first collect all messages, then pair user with preceding assistant
            all_lines = []
            with open(filepath, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        all_lines.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

            last_assistant = None
            for msg in all_lines:
                if msg.get("type") == "assistant":
                    last_assistant = msg
                    continue

                if msg.get("type") != "user":
                    continue

                text = extract_text(msg)
                text = text.strip()

                if not text or is_system_injected(text):
                    continue

                total_user_messages += 1

                # Build agent context from preceding assistant message
                agent_ctx = ""
                if last_assistant:
                    tools = extract_tool_names(last_assistant)
                    a_text = extract_text(last_assistant)
                    first = _meaningful_line(a_text, from_end=False)
                    last = _meaningful_line(a_text, from_end=True)

                    parts = []
                    if tools:
                        parts.append("tools=" + ",".join(tools[:4]))
                    if first:
                        parts.append("first=" + first[:100])
                    if last and last != first:
                        parts.append("last=" + last[:100])
                    agent_ctx = " | ".join(parts)

                messages.append({
                    "text": text,
                    "project": project,
                    "session": session_name,
                    "agent_context": agent_ctx,
                })
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)

    return messages, total_user_messages


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--out", default=None,
        help="Output file path (default: tmp_dump_user_messages_<timestamp>.md)",
    )
    parser.add_argument(
        "--claude-dirs", nargs="+", default=None,
        help="Additional .claude directories to scan (~/.claude is always included)",
    )
    args = parser.parse_args()

    output_path = Path(args.out) if args.out else _default_output()
    claude_dirs = [Path.home() / ".claude"]
    if args.claude_dirs:
        for d in args.claude_dirs:
            p = Path(d).expanduser()
            if p not in claude_dirs:
                claude_dirs.append(p)

    all_messages, total_user_messages = scan_all_sessions(claude_dirs)
    aliases = collect_bash_aliases()

    print(f"Total user messages: {total_user_messages}", file=sys.stderr)
    print(f"Collected: {len(all_messages)}", file=sys.stderr)
    if aliases:
        print(f"Bash aliases detected: {len(aliases)}", file=sys.stderr)

    # Count exact duplicates (case-insensitive, truncated)
    text_counter = Counter(
        _truncate(m["text"]).lower() for m in all_messages)

    # Group by first word
    by_first_word = {}
    for m in all_messages:
        words = m["text"].lower().strip().split()
        if words:
            fw = words[0].rstrip(".,!?:;")
            by_first_word.setdefault(fw, []).append(m)

    # Compute length distribution
    lengths = sorted(len(m["text"]) for m in all_messages)
    n = len(lengths)

    with open(output_path, "w", encoding="utf-8") as out:
        out.write("# User Messages Dump for Mismatch Signal Discovery\n\n")
        out.write(f"Total user messages scanned: {total_user_messages}\n")
        out.write(f"Display truncated at {DISPLAY_LIMIT} chars.\n\n")

        # Message length distribution
        out.write("## Message Length Distribution\n\n")
        if n > 0:
            buckets = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
            out.write("| Range | Count | % |\n")
            out.write("|-------|-------|---|\n")
            prev = 0
            for b in buckets:
                count = sum(1 for l in lengths if prev < l <= b)
                pct = count / n * 100
                out.write(f"| {prev+1}-{b} | {count} | {pct:.1f}% |\n")
                prev = b
            over = sum(1 for l in lengths if l > buckets[-1])
            out.write(f"| {buckets[-1]+1}+ | {over} | {over/n*100:.1f}% |\n")
            out.write("\n")
            for p in [50, 75, 90, 95, 99]:
                idx = min(int(n * p / 100), n - 1)
                out.write(f"- p{p}: {lengths[idx]} chars\n")
            out.write("\n")

        # Section 0: Bash aliases (false positive context)
        if aliases:
            out.write("## 0. Bash Aliases (false positives)\n\n")
            out.write("These are the user's bash aliases. Short messages "
                      "matching these are mistyped terminal commands,\n"
                      "NOT mismatch signals. They are often followed by "
                      "Esc (request interrupted).\n\n")
            out.write("| Alias | Meaning |\n")
            out.write("|-------|----------|\n")
            for name, value in sorted(aliases.items()):
                out.write(f"| `{name}` | `{value}` |\n")
            out.write("\n")

        # Section 1: Most repeated messages
        out.write("## 1. Most Repeated Messages\n\n")
        out.write("Messages said more than once (case-insensitive):\n\n")
        out.write("| Count | Message |\n")
        out.write("|-------|----------|\n")
        for text, count in text_counter.most_common():
            if count >= 2:
                escaped = text.replace("|", "\\|")
                out.write(f"| {count} | `{escaped}` |\n")

        # Section 2: All messages grouped by first word
        out.write("\n\n## 2. All Messages Grouped by First Word\n\n")
        out.write("Sorted by frequency of first word. "
                  "Review for mismatch patterns.\n\n")

        sorted_groups = sorted(
            by_first_word.items(), key=lambda x: -len(x[1]))

        for first_word, msgs in sorted_groups:
            out.write(f"### `{first_word}` ({len(msgs)} messages)\n\n")
            seen = set()
            for m in msgs:
                truncated = _truncate(m["text"])
                key = truncated.lower()
                if key in seen:
                    continue
                seen.add(key)
                escaped = truncated.replace("|", "\\|")
                ctx = m.get("agent_context", "")
                if ctx:
                    ctx_escaped = ctx.replace("|", "\\|")
                    out.write(f"- `{escaped}`\n"
                              f"  - _agent: {ctx_escaped}_\n")
                else:
                    out.write(f"- `{escaped}`\n")
            out.write("\n")

        # Section 3: Very short messages (≤20 chars)
        out.write("\n## 3. Very Short Messages (≤20 chars)\n\n")
        very_short = [m for m in all_messages if len(m["text"]) <= 20]
        vs_counter = Counter(m["text"].lower().strip() for m in very_short)
        out.write("| Count | Message |\n")
        out.write("|-------|----------|\n")
        for text, count in vs_counter.most_common():
            escaped = text.replace("|", "\\|")
            out.write(f"| {count} | `{escaped}` |\n")

        # Section 4: Messages with question marks
        out.write("\n\n## 4. Messages with `?`\n\n")
        question_msgs = [m for m in all_messages if "?" in m["text"]]
        q_counter = Counter(
            _truncate(m["text"]).lower() for m in question_msgs)
        out.write("| Count | Message |\n")
        out.write("|-------|----------|\n")
        for text, count in q_counter.most_common():
            escaped = text.replace("|", "\\|")
            out.write(f"| {count} | `{escaped}` |\n")

    size_bytes = output_path.stat().st_size
    size_kib = size_bytes / 1024
    est_tokens = size_bytes // 4  # rough estimate: ~4 bytes per token
    print(f"\nWritten to {output_path} ({size_kib:.0f} KiB, ~{est_tokens:,} tokens)",
          file=sys.stderr)
    if size_kib > 2048:
        print("WARNING: dump exceeds 2 MiB. Consider filtering with --claude-dirs "
              "or fewer sessions to fit in LLM context.", file=sys.stderr)


if __name__ == "__main__":
    main()
