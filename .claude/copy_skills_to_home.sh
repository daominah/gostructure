#!/bin/bash
set -euo pipefail

# This script copies skills and CLAUDE.md from this project's .claude/ to ~/.claude/,
# overwriting existing skills with the same name.

# Absolute path of this script's directory, regardless of where the script is run from
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy CLAUDE.md
if diff -q "$SCRIPT_DIR/CLAUDE.md" "$HOME/.claude/CLAUDE.md" > /dev/null 2>&1; then
    echo "unchanged CLAUDE.md (already identical)"
else
    cp "$SCRIPT_DIR/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
    echo "OVERWROTE CLAUDE.md"
fi

# Copy each skill directory
for skill_dir in "$SCRIPT_DIR"/skills/*/; do
    skill_name="$(basename "$skill_dir")"

    # Skills to exclude from copying
    excluded=(
        "*-workspace"
        "agent-conversation-analysis"
        "sql-schema-placeholder"
    )
    skip=false
    for pattern in "${excluded[@]}"; do
        if [[ "$skill_name" == $pattern ]]; then
            # echo "Skipping: $skill_name"
            skip=true
            break
        fi
    done
    if $skip; then continue; fi

    target="$HOME/.claude/skills/$skill_name"
    if [[ -d "$target" ]]; then
        if diff -rq "$skill_dir" "$target" > /dev/null 2>&1; then
            echo "unchanged $skill_name (already identical)"
            continue
        fi
        action="OVERWROTE"
    else
        action="CREATED"
    fi
    mkdir -p "$target"
    cp -r "$skill_dir"* "$target/"
    echo "$action skill: $skill_name"
done

echo "Done."
