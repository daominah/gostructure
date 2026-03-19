"""Scan all user messages in replay_data.json for potential frustration keywords.

Prints unique words/phrases from short user messages (likely corrections)
that aren't already in CORRECTION_PHRASES, to help discover new keywords.

Usage:
    python3 scan_frustration.py /tmp/replay_data.json
"""

import json
import re
import sys
from collections import Counter

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


# Known frustration/profanity patterns to search for
CANDIDATE_PATTERNS = [
    r"\bwtf\b", r"\bwth\b", r"\bfuck\b", r"\bshit\b", r"\bdamn\b",
    r"\bcrap\b", r"\bhell\b", r"\bugh\b", r"\bomg\b", r"\bffs\b",
    r"\bstop\b", r"\bno[\.,!]", r"\bnope\b", r"\bwrong\b",
    r"\bnot that\b", r"\bnot this\b", r"\bnot what\b",
    r"\brevert\b", r"\bundo\b", r"\brollback\b",
    r"\btry again\b", r"\bfix this\b", r"\bfix it\b",
    r"\bi said\b", r"\bi meant\b", r"\bi mean\b", r"\bmy meaning\b",
    r"\bdon'?t\b", r"\bdidn'?t\b", r"\bshouldn'?t\b",
    r"\bstill\b", r"\bagain\b", r"\balready\b",
    r"\bnot work\b", r"\bdoesn'?t work\b", r"\bnot right\b",
]


def scan(data):
    matches = Counter()
    examples = {}

    for path, proj in data["projects"].items():
        for session in proj["sessions"]:
            for msg in session["messages"]:
                if msg["role"] != "user":
                    continue
                text = msg["content"]
                if text.startswith("<"):
                    continue

                lower = text.lower()
                for pattern in CANDIDATE_PATTERNS:
                    if re.search(pattern, lower):
                        keyword = pattern.replace(r"\b", "").replace(r"[\.,!]", "")
                        matches[keyword] += 1
                        if keyword not in examples:
                            examples[keyword] = text[:150].replace("\n", " ")

    print("=== Frustration/correction keywords found ===\n")
    for keyword, count in matches.most_common():
        print(f"  {count:3d}x  {keyword}")
        print(f"        e.g. {examples[keyword]}")
        print()


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        import tempfile, os
        path = os.path.join(tempfile.gettempdir(), "replay_data.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    scan(data)


if __name__ == "__main__":
    main()
