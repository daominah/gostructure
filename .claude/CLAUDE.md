# Writing Style

- Avoid dashes (`-` or `—`) in the middle of sentences;
  rephrase or use colons instead.
  Compound words are allowed: "real-time", "back-end".
- Use standard straight quotes (`'` and `"`) instead of curly quotes.
- When the user asks to correct grammar (e.g. "grammar?", "smooth?"),
  apply only the minimal change without rephrasing the rest of the sentence.
- Use bold only to insist on a specific approach over a common alternative
  or to warn about pitfalls the reader might skip past.

# Git Commit

- Before committing, check the staged changes for secrets (API keys, tokens, passwords, etc.)
  and warn the user if any are found.
- ALWAYS invoke skill `commit-messages` before ANY git commit,
  including short user requests: "commit", "git commit", "commit push", "git commit push", etc.

# Markdown

**Always load** skill `writing-style-markdown` before writing or editing any `.md` file,
including README, CLAUDE.md, SKILL.md, ticket and feature design docs,
plans, checklists, review reports, findings, and spec docs.
This applies even when the file is referenced implicitly without a `.md` extension,
and when the user asks for a diagram (defaults to Mermaid embedded in a markdown file).

# Go

**Always load** skills `go-personal-convention` and `go-project-structure`
before doing anything related to Go code.

# Python

Place all imports at the top of the file.

# Frontend

**Always load** skill `frontend-code-style`
before doing anything related to HTML, JavaScript, or CSS.

# Naming

When naming variables, sections, or concepts:
prefer short, code-style terms over verbose descriptions,
but use full words instead of abbreviations.
Ask for confirmation before choosing names if the context is ambiguous.

This applies to conversation too: never introduce abbreviations
for project names, company names, or concepts unless the user
used that abbreviation first. Use the full name for easier understanding.

# Session Hygiene

When a task appears complete (commit done, PR created, investigation answered),
or when the user asks a question that seems unrelated to the current topic,
suggest starting a new session for the next topic.

# Testing

Do not weaken or remove test assertions when the error looks like an environment issue;
ask the user to fix the environment setup instead.

# Checkpoints

When a skill instruction says STOP or "wait for confirmation",
do not proceed to the next step until the user explicitly approves.

# Multi-part Response

When presenting multiple issues, inconsistencies, problems, or questions for review,
list them all first as a summary, then go through each one individually.
When discussing each item (including when asking whether to proceed to it)
reprint its full detail so the user does not need to scroll up to the summary.
Wait for the user's response before moving to the next.

# Code Comments

Code comments should explain intent and non-obvious behavior.
Avoid generating comments that just restate the function or variable name.

For test comments, load skill `test-comments`.

# Answering Questions About Code

When answering any "where is X" / "how does Y work" / "which file handles Z" question,
cite concrete paths as `file_path:line_number` alongside the explanation.

# Bash

- Use `#!/bin/bash` as the shebang line, not `#!/usr/bin/env bash`.
