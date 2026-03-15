"""Summarize replay_data.json for quick overview and task grouping.

Usage:
    python summarize.py [--timeline] /tmp/replay_data.json

Modes:
    default:    project stats + sessions with corrections/gaps
    --timeline: all sessions with date, branch, duration, first message
"""

import json
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


def summarize(data, timeline=False):
    for path, proj in data["projects"].items():
        sc = proj["session_count"]
        if sc == 1:
            s = proj["sessions"][0]
            user_msgs = s["stats"]["user_messages"]
            assistant_msgs = s["stats"]["assistant_messages"]
            if user_msgs <= 2 and assistant_msgs <= 2:
                continue
        elif sc < 1:
            continue

        print(f"\n=== {path} ({sc} sessions) ===")
        git = proj.get("git", {})
        print(
            f"  Git: {git.get('commits_recent', '?')} commits, "
            f"{git.get('reverts_amends', '?')} reverts"
        )
        me = proj.get("manual_edits", {})
        print(
            f"  Manual edits: {me.get('manual_edit_count', 0)} lines, "
            f"{me.get('stale_read_failures', 0)} stale reads"
        )
        su = proj.get("setup_usage", {})
        print(
            f"  Setup: {su.get('total_skills_triggered', 0)} skills, "
            f"{su.get('total_mcp_tools_called', 0)} MCP tools"
        )

        total_corrections = 0
        total_setup_gaps = 0
        total_user_msgs = 0
        for s in proj["sessions"]:
            stats = s["stats"]
            total_corrections += stats["corrections"]
            total_setup_gaps += stats["setup_gaps"]
            total_user_msgs += stats["user_messages"]

            first_msg = _first_user_message(s, maxlen=120)

            if timeline:
                branch = s.get("git_branch", "?")
                print(
                    f"  {s['started_at'][:10]} {s['session_id'][:8]} "
                    f"branch={branch} dur={s['duration_minutes']:.0f}m "
                    f"msgs={stats['user_messages']}u/{stats['assistant_messages']}a "
                    f"c={stats['corrections']} g={stats['setup_gaps']}"
                )
                print(f"    > {first_msg}")
            elif stats["corrections"] > 0 or stats["setup_gaps"] > 0:
                print(
                    f"  Session {s['session_id'][:8]}: "
                    f"{stats['corrections']}c {stats['setup_gaps']}g "
                    f"dur={s['duration_minutes']:.0f}m | {first_msg[:80]}"
                )
        print(
            f"  Totals: {total_corrections} corrections, "
            f"{total_setup_gaps} setup gaps, {total_user_msgs} user msgs"
        )


def _first_user_message(session, maxlen=120):
    for m in session["messages"]:
        if m["role"] == "user" and not m["content"].startswith("<"):
            return m["content"][:maxlen].replace("\n", " ")
    return ""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    if not args:
        import tempfile, os
        path = os.path.join(tempfile.gettempdir(), "replay_data.json")
    else:
        path = args[0]
    timeline = "--timeline" in flags
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    summarize(data, timeline=timeline)


if __name__ == "__main__":
    main()
