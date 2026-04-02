# Writing Style

- Avoid dashes (`-` or `—`) in the middle of sentences;
  rephrase or use colons instead.
  Compound words are allowed: "real-time", "back-end".
- Use standard straight quotes (`'` and `"`) instead of curly quotes.
- When the user asks to correct grammar (e.g. "grammar?", "smooth?"),
  apply only the minimal change without rephrasing the rest of the sentence.
- Use bold only to insist on a specific approach over a common alternative                                                            
  or to warn about pitfalls the reader might skip past.

# Naming

When naming variables, sections, or concepts:
prefer short, code-style terms over verbose descriptions,
but use full words instead of abbreviations.
Ask for confirmation before choosing names if the context is ambiguous.

# Git Commit

- Before committing, check the staged changes for secrets (API keys, tokens, passwords, etc.)
  and warn the user if any are found.
- ALWAYS invoke skill `commit-messages` before ANY git commit,
  including short user requests: "commit", "git commit", "commit push", "git commit push", etc.

# Go

**Always load** skills `go-personal-convention` and `go-project-structure`
before doing anything related to Go code.

# Testing

Do not weaken or remove test assertions when the error looks like an environment issue;
ask the user to fix the environment setup instead.

# Checkpoints

When a skill instruction says STOP or "wait for confirmation",
do not proceed to the next step until the user explicitly approves.

# Session Hygiene

When a task appears complete (commit done, PR created, investigation answered),
or when the user asks a question that seems unrelated to the current topic,
suggest starting a new session for the next topic.

# Bash

- Use `#!/bin/bash` as the shebang line, not `#!/usr/bin/env bash`.
