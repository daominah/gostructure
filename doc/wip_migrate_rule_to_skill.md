# WIP: Migrate Cursor Rules to Agent Skills

## Status: Completed

## Goal

Reduce preloaded agent context by converting Cursor rules to the generic
[Agent Skills](https://agentskills.io) format. Only skill names and descriptions
are preloaded; full skill bodies are loaded on demand when relevant.

Add equivalent Claude Code support under `.claude/`.

## Key Finding

The [Cursor docs](https://cursor.com/docs/context/skills) state:

> For compatibility, Cursor also loads skills from Claude and Codex directories:
> `.claude/skills/`, `.codex/skills/`, `~/.claude/skills/`, and `~/.codex/skills/`.

So skills stored in `.claude/skills/` work for both Cursor and Claude Code.
No duplication or symlinks required.

## Skill File Format

Generic [agentskills.io](https://agentskills.io) format. Only `name` and
`description` in frontmatter (no tool-specific fields).

```markdown
---
name: skill-name
description: What it does. Use when <trigger scenario>.
---

# Title

...instructions...
```

## Final Directory Layout

```
.cursor/
  rules/
    forbid-read-ssh.mdc                    ← alwaysApply:true (security, never skip)
    ask-before-implement-unless-explicit.mdc ← alwaysApply:true (Cursor only, no Claude equiv)

.claude/
  CLAUDE.md        ← forbid-read-ssh rule as always-present instruction for Claude Code
  skills/
    commit-messages/SKILL.md
    go-personal-convention/SKILL.md
    go-project-structure/SKILL.md
    slack-messaging/SKILL.md
    sql-formatting/SKILL.md
    test-comments/SKILL.md
    writing-style-markdown/SKILL.md
    writing-style/SKILL.md
```

## Rules That Stayed as Cursor-Only Rules

- `forbid-read-ssh`: Security rule, must always be active. Also mirrored in
  `.claude/CLAUDE.md` for Claude Code.
- `ask-before-implement-unless-explicit`: Equivalent to Claude Code's default
  permission mode (ask before file edits and shell commands). No Claude Code
  equivalent needed. Renamed from `always-confirm-before-implementing` and
  reworded to clarify: ask only when request is a question or ambiguous, not
  unconditionally.

## Skills Migrated (8 rules)

| Skill | Description |
|---|---|
| `commit-messages` | No AI attribution in git commits; keep messages concise and focused on business logic. Use when creating git commits. |
| `go-personal-convention` | Personal Go conventions. Use when writing or reviewing Go code. |
| `go-project-structure` | Go project directory layout and package conventions. Use when creating, organizing, or refactoring Go files, packages, features, or functions. |
| `slack-messaging` | Always draft Slack messages first, share the channel link, then ask the user whether to send. Use when asked to send, post, or reply in Slack. |
| `sql-formatting` | SQL formatting and style rules. Use when writing or editing SQL queries or migrations. |
| `test-comments` | GIVEN/WHEN/THEN comment format for unit tests. Use when writing, editing, or reviewing unit tests. |
| `writing-style-markdown` | Markdown writing style conventions. Use when writing or editing Markdown files or variants (e.g. .mdc). |
| `writing-style` | Writing style: avoid mid-sentence dashes, use straight quotes. Use when writing any prose, documentation, messages, or code comments. |
