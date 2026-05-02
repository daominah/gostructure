#!/bin/bash
set -euo pipefail

# This script mirrors this project's .claude/ tree to ~/.claude/, overwriting
# existing files of the same name. It is one-way (repo -> home), idempotent
# (re-running only re-copies files whose content actually changed), and safe
# to run repeatedly after each config edit.
#
# In scope:
#   - CLAUDE.md
#   - statusline-command.sh
#   - hooks/*
#   - skills/*           (minus a small exclusion list of unfinished/local-only skills)
#   - home_settings.json : its top-level keys overwrite the matching keys in
#                          ~/.claude/settings.json; other keys in home are preserved.

# Absolute path of this script's directory, regardless of where the script is run from
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Idempotent file copy: skip when src and dst already match byte-for-byte,
# otherwise copy preserving mode/timestamps and report what happened.
copy_file() {
    local src="$1" dst="$2" label="$3"
    if [[ -e "$dst" ]] && diff -q "$src" "$dst" > /dev/null 2>&1; then
        echo "unchanged $label (already identical)"
        return
    fi
    mkdir -p "$(dirname "$dst")"
    cp -p "$src" "$dst"
    echo "OVERWROTE $label"
}

echo "----------------"
# Copy CLAUDE.md
copy_file "$SCRIPT_DIR/CLAUDE.md" "$HOME/.claude/CLAUDE.md" "CLAUDE.md"

# Copy statusline-command.sh
copy_file "$SCRIPT_DIR/statusline-command.sh" "$HOME/.claude/statusline-command.sh" "statusline-command.sh"

# Copy each hook script
if [[ -d "$SCRIPT_DIR/hooks" ]]; then
    echo "----------------"
    for hook in "$SCRIPT_DIR"/hooks/*; do
        [[ -f "$hook" ]] || continue
        name="$(basename "$hook")"
        copy_file "$hook" "$HOME/.claude/hooks/$name" "hook: $name"
    done
fi

echo "----------------"
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
    # Trailing /. copies contents including dotfiles; bare /* glob skips them.
    cp -r "$skill_dir." "$target/"
    echo "$action skill: $skill_name"
done

echo "----------------"
# Merge home_settings.json into ~/.claude/settings.json:
# top-level keys in home_settings.json overwrite those in home,
# other top-level keys in home are preserved (e.g. model, effortLevel).
home_settings_src="$SCRIPT_DIR/home_settings.json"
home_settings_dst="$HOME/.claude/settings.json"
if [[ -f "$home_settings_src" ]]; then
    [[ -f "$home_settings_dst" ]] || echo '{}' > "$home_settings_dst"
    # Per-key status: ADDED if key didn't exist in home, OVERWROTE if value
    # differed, unchanged if it already matched.
    jq -nr \
        --slurpfile src "$home_settings_src" \
        --slurpfile dst "$home_settings_dst" \
        '$src[0] | to_entries[] |
         .key as $k |
         if ($dst[0] | has($k) | not) then "ADDED settings.\($k)"
         elif ($dst[0][$k] == .value)  then "unchanged settings.\($k) (already identical)"
         else "OVERWROTE settings.\($k)" end'
    # Write the merged content back (only if it actually changed).
    new_content="$(jq -s '.[0] + .[1]' "$home_settings_dst" "$home_settings_src")"
    old_content="$(jq . "$home_settings_dst")"
    if [[ "$new_content" != "$old_content" ]]; then
        printf '%s\n' "$new_content" > "$home_settings_dst"
    fi
fi

echo "----------------"
echo "Done."
