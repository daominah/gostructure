#!/usr/bin/env python3
"""Extract detailed task-level information for scoring.

Usage:
    python3 extract_task_details.py <json_path> [--session <prefix>]

Without --session: prints a compact summary of all sessions with user messages.
With --session: prints full user messages for that specific session.
"""

import json
import sys


def load_data(path):
    with open(path) as f:
        return json.load(f)


def summarize_all(data):
    for proj_path, proj in data["projects"].items():
        git = proj.get("git", {})
        print(f"=== {proj_path} ===")
        print(f"Git: {git.get('commits_recent', '?')} commits, "
              f"{git.get('reverts_amends', '?')} reverts/amends, "
              f"{git.get('net_lines_added', '?')}+ / {git.get('net_lines_removed', '?')}-")
        if git.get("top_churned_files"):
            print("Top churned files:")
            for f_info in git["top_churned_files"][:5]:
                print(f"  {f_info}")
        print()

        for s in proj["sessions"]:
            sid = s["session_id"][:8]
            dur = s["duration_minutes"]
            um = s["stats"]["user_messages"]
            am = s["stats"]["assistant_messages"]
            c = s["stats"]["corrections"]
            g = s["stats"]["setup_gaps"]

            # Extract first meaningful user message
            first_msg = ""
            for msg in s["messages"]:
                if msg["role"] == "user":
                    content = msg["content"]
                    if content.startswith("<command-") or content.startswith("<local-command"):
                        continue
                    first_msg = content.strip().replace("\n", " ")[:150]
                    break

            flag = ""
            if c >= 4:
                flag = " *** HIGH CORRECTIONS ***"
            elif c >= 2:
                flag = " ** NOTABLE **"

            print(f"  {sid} | {dur:>5.0f}m | {um}u/{am}a | c={c} g={g}{flag}")
            print(f"    > {first_msg}")

            if c > 0 and s["stats"].get("correction_examples"):
                for ex in s["stats"]["correction_examples"][:4]:
                    ex_clean = str(ex).strip().replace("\n", " ")[:150]
                    print(f"    ! {ex_clean}")
            print()


def show_session(data, prefix):
    for proj_path, proj in data["projects"].items():
        for s in proj["sessions"]:
            if s["session_id"].startswith(prefix):
                print(f"=== Session {s['session_id'][:8]} ({proj_path}) ===")
                print(f"Duration: {s['duration_minutes']}m")
                print(f"Messages: {s['stats']['user_messages']}u / {s['stats']['assistant_messages']}a")
                print(f"Corrections: {s['stats']['corrections']}")
                print(f"Setup gaps: {s['stats']['setup_gaps']}")
                print()

                for i, msg in enumerate(s["messages"]):
                    role = msg["role"][0].upper()
                    content = msg["content"]
                    if role == "A":
                        content = content[:300]
                    else:
                        content = content[:500]
                    content = content.strip().replace("\n", " | ")
                    print(f"  [{i:>3}] {role}: {content}")
                print()
                return
    print(f"Session with prefix '{prefix}' not found")


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_task_details.py <json_path> [--session <prefix>]")
        sys.exit(1)

    data = load_data(sys.argv[1])

    if "--session" in sys.argv:
        idx = sys.argv.index("--session")
        prefix = sys.argv[idx + 1]
        show_session(data, prefix)
    else:
        summarize_all(data)


if __name__ == "__main__":
    main()
