 #!/bin/bash
set -euo pipefail

# Install the portable parts of this repository's Claude Code setup for Codex.
#
# In scope:
#   - CLAUDE.md -> ~/.codex/AGENTS.md
#   - skills/*  -> ~/.codex/skills/*
#
# Claude-only settings, plugins, hooks, and status-line scripts are deliberately excluded
# because Codex configures those through its own config.toml and hooks.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

copy_file() {
    local src="$1" dst="$2" label="$3"

    if [[ -e "$dst" ]] && cmp -s "$src" "$dst"; then
        echo "unchanged $label (already identical)"
        return
    fi

    if [[ -e "$dst" ]]; then
        action="OVERWROTE"
    else
        action="CREATED"
    fi
    mkdir -p "$(dirname "$dst")"
    cp -p "$src" "$dst"
    echo "$action $label"
}

echo "----------------"
copy_file "$SCRIPT_DIR/CLAUDE.md" "$CODEX_HOME/AGENTS.md" "AGENTS.md"

echo "----------------"
for skill_dir in "$SCRIPT_DIR"/skills/*/; do
    [[ -d "$skill_dir" ]] || continue

    skill_name="$(basename "$skill_dir")"
    case "$skill_name" in
        *-workspace|agent-conversation-analysis|sql-schema-placeholder)
            continue
            ;;
    esac

    target="$CODEX_HOME/skills/$skill_name"
    if [[ -d "$target" ]] && diff -rq "$skill_dir" "$target" >/dev/null 2>&1; then
        echo "unchanged skill: $skill_name (already identical)"
        continue
    fi

    if [[ -d "$target" ]]; then
        action="OVERWROTE"
    else
        action="CREATED"
    fi
    mkdir -p "$target"
    cp -r "$skill_dir". "$target/"
    echo "$action skill: $skill_name"
done

echo "----------------"
echo "Done."
