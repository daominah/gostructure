#!/bin/bash
# SessionStart hook:
# load pre-built diagram-first docs into every new session
# so an agent or a human can grasp the project's main features
# without reading the full repo.
# Triggered by ~/.claude/settings.json -> hooks.SessionStart.

CONTEXT_DOCS_DIR="$HOME/workspace/ai_memory"

# Trigger dirs: the hook fires only when $PWD equals one of these
# or is nested under one. Otherwise it exits silently.
LOAD_IF_CLAUDE_START_IN_DIRS=(
  "$HOME/workspace"
)

match=0
for trigger in "${LOAD_IF_CLAUDE_START_IN_DIRS[@]}"; do
  case "$PWD" in
    "$trigger"|"$trigger"/*) match=1; break ;;
  esac
done
[ "$match" = "1" ] || exit 0

[ -d "$CONTEXT_DOCS_DIR" ] || exit 0

content=$(
  for f in "$CONTEXT_DOCS_DIR"/*.md; do
    [ -f "$f" ] || continue
    printf '\n=== %s ===\n\n' "${f##*/}"
    cat "$f"
  done
)

[ -n "$content" ] || exit 0

bytes=$(printf '%s' "$content" | wc -c | tr -d ' ')
approx_tokens=$((bytes / 4))
# Count files from the content's "=== <name> ===" headers emitted by the loop above,
# so the count matches exactly what was loaded (no second glob, no zero-match miscount).
files=$(printf '%s' "$content" | grep -c '^=== ')
msg="loaded project-context: $files files, ~$approx_tokens tokens"

# add content into the Claude session's context window
printf '%s' "$content" | jq -Rs --arg msg "$msg" '{systemMessage: $msg, hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: .}}'
