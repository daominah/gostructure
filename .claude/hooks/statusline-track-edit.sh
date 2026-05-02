#!/bin/bash
# PostToolUse hook for Edit/Write/MultiEdit.
# Records the edited file path into a per-session state file
# so statusline-command.sh can show repo[branch] for *this* session
# instead of whichever sub-repo had the most recent global write.
# Wired up in ~/.claude/settings.json under hooks.PostToolUse.

input=$(cat)

session_id=$(echo "$input" | jq -r '.session_id // empty')
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

if [ -z "$session_id" ] || [ -z "$file_path" ]; then
  exit 0
fi

state_dir="${HOME}/.claude/statuslinewd"
mkdir -p "$state_dir"
printf '%s\n' "$file_path" > "${state_dir}/${session_id}.path"
