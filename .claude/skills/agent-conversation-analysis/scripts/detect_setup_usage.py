#!/usr/bin/env python
"""
detect_setup_usage.py - Detect which skills, MCP tools,
and setup features were actually used during sessions.

Scans session JSONL files for:
- Skill invocations (<command-name> tags in user messages)
- MCP tool calls (tool_use blocks with mcp__ prefix in assistant messages)
- Built-in tool usage (Write, Edit, Read, Bash, Grep, Glob, etc.)

Usage:
    python detect_setup_usage.py --sessions SESSIONS.json [--out OUTPUT.json]

Output format:
    {
      "projects": {
        "<project-path>": {
          "skills_triggered": {
            "skill-name": { "count": 3, "sessions": ["sid1", "sid2"] }
          },
          "mcp_tools_called": {
            "mcp__server__tool": { "count": 5, "sessions": ["sid1"] }
          },
          "builtin_tools": {
            "Write": 42, "Edit": 30, "Read": 80, ...
          },
          "total_skills_triggered": 3,
          "total_mcp_tools_called": 2
        }
      }
    }
"""

import argparse
import json
import re
import sys
from pathlib import Path


COMMAND_NAME_RE = re.compile(r"<command-name>/?([\w-]+)</command-name>")


def scan_sessions(sessions_data: dict) -> dict:
    """Scan session JSONL files for setup usage."""
    claude_home = Path.home() / ".claude"
    result = {}

    for project_path, project_info in sessions_data.get("projects", {}).items():
        skills = {}       # skill_name -> {count, sessions set}
        mcp_tools = {}    # tool_name -> {count, sessions set}
        builtin_tools = {}  # tool_name -> count
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

                    # Detect skill invocations from <command-name> tags
                    # These appear in user messages (skill loading)
                    if msg_type == "user":
                        content = obj.get("message", {}).get("content", "")
                        text = _content_to_text(content)
                        for match in COMMAND_NAME_RE.finditer(text):
                            skill_name = match.group(1)
                            if skill_name not in skills:
                                skills[skill_name] = {
                                    "count": 0,
                                    "sessions": set(),
                                }
                            skills[skill_name]["count"] += 1
                            skills[skill_name]["sessions"].add(sid)

                    # Detect tool calls from assistant messages
                    if msg_type == "assistant":
                        content = obj.get("message", {}).get("content", [])
                        if not isinstance(content, list):
                            continue
                        for block in content:
                            if not isinstance(block, dict):
                                continue
                            if block.get("type") != "tool_use":
                                continue
                            tool_name = block.get("name", "")
                            if not tool_name:
                                continue

                            if tool_name.startswith("mcp__"):
                                if tool_name not in mcp_tools:
                                    mcp_tools[tool_name] = {
                                        "count": 0,
                                        "sessions": set(),
                                    }
                                mcp_tools[tool_name]["count"] += 1
                                mcp_tools[tool_name]["sessions"].add(sid)
                            else:
                                builtin_tools[tool_name] = (
                                    builtin_tools.get(tool_name, 0) + 1
                                )

        # Convert sets to sorted lists for JSON serialization
        for v in skills.values():
            v["sessions"] = sorted(v["sessions"])
        for v in mcp_tools.values():
            v["sessions"] = sorted(v["sessions"])

        result[project_path] = {
            "skills_triggered": skills,
            "mcp_tools_called": mcp_tools,
            "builtin_tools": dict(
                sorted(builtin_tools.items(), key=lambda x: x[1], reverse=True)
            ),
            "total_skills_triggered": len(skills),
            "total_mcp_tools_called": len(mcp_tools),
        }

        # Summary
        print(
            f"{project_path}: "
            f"{len(skills)} skills triggered, "
            f"{len(mcp_tools)} MCP tools, "
            f"{sum(builtin_tools.values())} builtin tool calls",
            file=sys.stderr,
        )
        for name, info in sorted(
            skills.items(), key=lambda x: x[1]["count"], reverse=True
        )[:5]:
            print(
                f"  skill: {name} ({info['count']}x "
                f"in {len(info['sessions'])} sessions)",
                file=sys.stderr,
            )
        for name, info in sorted(
            mcp_tools.items(), key=lambda x: x[1]["count"], reverse=True
        )[:5]:
            short = name.replace("mcp__", "")
            print(
                f"  mcp: {short} ({info['count']}x "
                f"in {len(info['sessions'])} sessions)",
                file=sys.stderr,
            )

    return result


def _content_to_text(content) -> str:
    """Convert message content to plain text for regex scanning."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                btype = block.get("type", "")
                if btype == "text":
                    parts.append(block.get("text", ""))
                elif btype == "tool_result":
                    rc = block.get("content", "")
                    if isinstance(rc, str):
                        parts.append(rc)
                    elif isinstance(rc, list):
                        for sub in rc:
                            if isinstance(sub, dict) and sub.get("type") == "text":
                                parts.append(sub.get("text", ""))
        return "\n".join(parts)
    return ""


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

    output = {"projects": scan_sessions(sessions_data)}

    result = json.dumps(output, indent=2, ensure_ascii=False)

    if args.out == "-":
        print(result)
    else:
        Path(args.out).write_text(result, encoding="utf-8")
        print(f"Written to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
