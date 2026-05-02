#!/bin/bash
# Status line script for Claude Code.
# Wired up in ~/.claude/settings.json under the "statusLine" key:
#   { "statusLine": { "type": "command", "command": "bash ~/.claude/statusline-command.sh" } }
# Output format: "Opus 4.7, 240k/1000k ctx, repo-name[branch]"

# Read stdin (the JSON payload Claude Code pipes in on every status line refresh:
# model, cwd, session_id, context_window, ...) into $input
input=$(cat)

# Strip any " (...)" suffix from model name, e.g. "Opus 4.7 (1M context)" -> "Opus 4.7".
model=$(echo "$input" | jq -r '.model.display_name // .model.id // "unknown"' | sed -E 's/ *\([^)]*\)//g')
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
ctx_size=$(echo "$input" | jq -r '.context_window.context_window_size // empty')
cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // empty')
session_id=$(echo "$input" | jq -r '.session_id // empty')
# Resolve relative cwd (Claude Code on Windows sends ".") to absolute path
if [ -n "$cwd" ] && [[ "$cwd" != /* ]] && [[ "$cwd" != [A-Za-z]:* ]]; then
  cwd=$(cd "$cwd" 2>/dev/null && pwd) || cwd=""
fi
# Convert Windows path (C:\...) to Unix path (/c/...) so bash tools work correctly
if command -v cygpath >/dev/null 2>&1 && [[ "$cwd" == [A-Za-z]:* ]]; then
  cwd=$(cygpath -u "$cwd" 2>/dev/null) || true
fi

if [ -n "$ctx_size" ]; then
  size_k=$(( ctx_size / 1000 ))
  if [ -n "$used_pct" ]; then
    used_k=$(( used_pct * size_k / 100 ))
    ctx="${used_k}k/${size_k}k"
  else
    # Fresh session: Claude Code hasn't reported usage yet.
    # Show "?" rather than fake-0 (the auto-loaded baseline is non-zero).
    ctx="?/${size_k}k"
  fi
else
  ctx="-"
fi

# Find the nearest ancestor of start_dir that contains any of the given markers.
# At each level the markers are checked in the given order;
# the first match returns immediately,
# so the innermost ancestor with any marker wins (cross-marker priority does not span levels).
# Echoes "<dir>|<marker>" on hit, or nothing.
#
# Args: start_dir marker1 [marker2 ...]
walk_up_for_markers() {
  local dir="$1"
  shift
  while :; do
    for m in "$@"; do
      if [ -e "$dir/$m" ]; then
        printf '%s|%s\n' "$dir" "$m"
        return
      fi
    done
    local parent
    parent=$(dirname "$dir")
    if [ "$parent" = "$dir" ]; then
      return
    fi
    dir="$parent"
  done
}

# Project detection: walk up for a repo marker, starting from the session's
# last edited file (recorded by hooks/statusline-track-edit.sh into
# ~/.claude/statuslinewd/<session_id>.path) if available, otherwise from cwd.
# Walk up for .git, then go.mod / requirements.txt / package.json.
# Final fallback: basename of cwd.
right=""
if [ -n "$cwd" ]; then
  session_path=""
  if [ -n "$session_id" ]; then
    state_file="${HOME}/.claude/statuslinewd/${session_id}.path"
    if [ -r "$state_file" ]; then
      candidate=$(head -1 "$state_file")
      # Only trust the recorded path if it's still under cwd; otherwise this
      # session has edited a file in a different tree and the path would
      # mislead the walk-up.
      case "$candidate" in
        "$cwd"/*|"$cwd") session_path="$candidate" ;;
      esac
    fi
  fi
  if [ -n "$session_path" ]; then
    start_dir=$(dirname "$session_path")
  else
    start_dir="$cwd"
  fi
  hit=$(walk_up_for_markers "$start_dir" .git)
  if [ -z "$hit" ]; then
    hit=$(walk_up_for_markers "$start_dir" go.mod requirements.txt package.json)
  fi
  if [ -n "$hit" ]; then
    project_dir="${hit%|*}"
    project_marker="${hit##*|}"
    proj=$(basename "$project_dir")
    if [ "$project_marker" = ".git" ]; then
      branch=$(git -C "$project_dir" symbolic-ref --short HEAD 2>/dev/null || git -C "$project_dir" rev-parse --short HEAD 2>/dev/null)
      if [ -n "$branch" ]; then
        right="${proj}[${branch}]"
      else
        right="$proj"
      fi
    else
      right="$proj"
    fi
  else
    right=$(basename "$cwd")
  fi
fi

if [ -n "$right" ]; then
  printf "%s, %s ctx, %s" "$model" "$ctx" "$right"
else
  printf "%s, %s ctx" "$model" "$ctx"
fi
