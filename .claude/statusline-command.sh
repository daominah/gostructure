#!/bin/bash
# Status line script for Claude Code.
# Wired up in ~/.claude/settings.json under the "statusLine" key:
#   { "statusLine": { "type": "command", "command": "bash ~/.claude/statusline-command.sh" } }
# Output format: "Opus 4.7, 240k/1000k ctx, repo-name[branch]"

input=$(cat)

model=$(echo "$input" | jq -r '.model.display_name // .model.id // "unknown"')
used_pct=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
ctx_size=$(echo "$input" | jq -r '.context_window.context_window_size // empty')
cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // empty')
# Resolve relative cwd (Claude Code on Windows sends ".") to absolute path
if [ -n "$cwd" ] && [[ "$cwd" != /* ]] && [[ "$cwd" != [A-Za-z]:* ]]; then
  cwd=$(cd "$cwd" 2>/dev/null && pwd) || cwd=""
fi
# Convert Windows path (C:\...) to Unix path (/c/...) so bash tools work correctly
if command -v cygpath >/dev/null 2>&1 && [[ "$cwd" == [A-Za-z]:* ]]; then
  cwd=$(cygpath -u "$cwd" 2>/dev/null) || true
fi

if [ -n "$used_pct" ] && [ -n "$ctx_size" ]; then
  size_k=$(( ctx_size / 1000 ))
  used_k=$(( used_pct * size_k / 100 ))
  ctx="${used_k}k/${size_k}k"
else
  ctx="-"
fi

# Find the nearest ancestor of start_dir that contains any of the given markers,
# walking up through parents until cap_dir (inclusive).
# At each level the markers are checked in the given order;
# the first match returns immediately,
# so the innermost ancestor with any marker wins (cross-marker priority does not span levels).
# Echoes "<dir>|<marker>" on hit, or nothing.
#
# Args: start_dir cap_dir marker1 [marker2 ...]
walk_up_for_markers() {
  local dir="$1" cap="$2"
  shift 2
  while :; do
    for m in "$@"; do
      if [ -e "$dir/$m" ]; then
        printf '%s|%s\n' "$dir" "$m"
        return
      fi
    done
    if [ "$dir" = "$cap" ]; then
      return
    fi
    local parent
    parent=$(dirname "$dir")
    if [ "$parent" = "$dir" ]; then
      return
    fi
    dir="$parent"
  done
}

# Project detection: from the most-recently-modified file under cwd,
# walk up looking first for .git across all ancestor levels (capped at cwd).
# Only if no .git is found,
# walk up again for go.mod / requirements.txt / package.json.
# Fallback to cwd's basename.
right=""
if [ -n "$cwd" ]; then
  # GNU find (Linux/Git Bash) supports -printf; BSD find (macOS) does not
  if find /dev/null -printf '' 2>/dev/null; then
    recent=$(
      find "$cwd" -maxdepth 6 \
        \( -name .git -o -name node_modules -o -name .venv -o -name __pycache__ \
           -o -name vendor -o -name dist -o -name build -o -name target -o -name .next \) -prune \
        -o -type f -printf '%T@ %p\n' 2>/dev/null \
      | sort -rn | head -1 | cut -d' ' -f2-
    )
  else
    recent=$(
      find "$cwd" -maxdepth 6 \
        \( -name .git -o -name node_modules -o -name .venv -o -name __pycache__ \
           -o -name vendor -o -name dist -o -name build -o -name target -o -name .next \) -prune \
        -o -type f -print0 2>/dev/null \
      | xargs -0 stat -f '%m %N' 2>/dev/null \
      | sort -rn | head -1 | cut -d' ' -f2-
    )
  fi
  start_dir="$cwd"
  if [ -n "$recent" ]; then
    start_dir=$(dirname "$recent")
  fi
  hit=$(walk_up_for_markers "$start_dir" "$cwd" .git)
  if [ -z "$hit" ]; then
    hit=$(walk_up_for_markers "$start_dir" "$cwd" go.mod requirements.txt package.json)
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
