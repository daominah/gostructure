---
name: Migrate Rules to Skills
overview: Migrate all Cursor rules to the generic Agent Skills format (.cursor/skills/ and .claude/skills/), add Claude Code equivalent config, and write a WIP doc for session continuity.
todos:
  - id: write-wip-doc
    content: Write doc/wip_migrate_rule_to_skill.md with the full plan and skill descriptions
    status: completed
  - id: reword-always-confirm-rule
    content: Rename always-confirm-before-implementing.mdc to ask-before-implement-unless-explicit.mdc and simplify wording (keep alwaysApply:true)
    status: completed
  - id: migrate-8-rules
    content: Create .claude/skills/<name>/SKILL.md for each of the 8 rules, then delete original .mdc files
    status: completed
  - id: keep-ssh-rule
    content: Keep .cursor/rules/forbid-read-ssh.mdc as alwaysApply:true (no change)
    status: completed
  - id: create-claude-dir
    content: Create .claude/CLAUDE.md with the ssh security rule
    status: completed
isProject: false
---

# Migrate Rules to Agent Skills

## Goal

- Convert all `.cursor/rules/*.mdc` files to `SKILL.md` format so only descriptions
  are preloaded; full content is loaded on demand.
- Add equivalent Claude Code config under `.claude/`.
- Use only generic [agentskills.io](https://agentskills.io) frontmatter fields:
  `name` and `description`. No tool-specific fields.
- Write progress doc to [`doc/wip_migrate_rule_to_skill.md`](doc/wip_migrate_rule_to_skill.md).

## Key finding: No symlink needed

The [Cursor docs](https://cursor.com/docs/context/skills) state:

> For compatibility, Cursor also loads skills from Claude and Codex directories:
> `.claude/skills/`, `.codex/skills/`, `~/.claude/skills/`, and `~/.codex/skills/`.

So storing skills in `.claude/skills/` is enough for both Cursor and Claude Code.
No duplication or symlinks required.

## Directory Layout After Migration

```
.cursor/
  rules/
    forbid-read-ssh.mdc                    ← keep alwaysApply:true (security rule)
    ask-before-implement-unless-explicit.mdc ← rename + reword, keep alwaysApply:true

.claude/
  CLAUDE.md               ← contains forbid-read-ssh rule (always-present for Claude Code)
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

## Rules staying as Cursor-only alwaysApply rules

- `forbid-read-ssh`: security rule, must always be active, no change
- `ask-before-implement-unless-explicit`: equivalent to Claude's default permission mode
  (ask before editing files/running commands). Keep as `alwaysApply:true` in Cursor,
  but simplify the wording. The "ALWAYS ask" phrasing is misleading; the real intent is:
  ask when the request is a question or ambiguous, skip confirmation when the user
  clearly wants implementation.

Proposed reworded rule body:

```
Before making code changes, check whether the user is asking for implementation:

- If the request is a question ("how to...", "what is...", "is it possible...") or
  is ambiguous: provide information first, then ask if they want implementation.
- If the request clearly asks for implementation ("implement", "fix", "add", "do it",
  etc.): proceed without asking for confirmation.
```

## Skills: 8 rules to migrate (auto-corrected descriptions for review)

| Skill name | Proposed description |
|---|---|
| `commit-messages` | No AI attribution in git commits; keep messages concise and focused on business logic. Use when creating git commits. |
| `go-personal-convention` | Personal Go conventions. Use when writing or reviewing Go code. |
| `go-project-structure` | Go project directory layout and package conventions. Use when creating, organizing, or refactoring Go files, packages, features, or functions. |
| `slack-messaging` | Always draft Slack messages first, share the channel link, then ask the user whether to send. Use when asked to send, post, or reply in Slack. |
| `sql-formatting` | SQL formatting and style rules. Use when writing or editing SQL queries or migrations. |
| `test-comments` | GIVEN/WHEN/THEN comment format for unit tests. Use when writing, editing, or reviewing unit tests. |
| `writing-style-markdown` | Markdown writing style conventions. Use when writing or editing Markdown files or variants (e.g. .mdc). |
| `writing-style` | Writing style: avoid mid-sentence dashes, use straight quotes. Use when writing any prose, documentation, messages, or code comments. |

`forbid-read-ssh` and `ask-before-implement-unless-explicit` are **not** converted to skills.

## Skill File Format (generic, no tool-specific fields)

```yaml
---
name: commit-messages
description: Use when writing or reviewing git commit messages or pull request descriptions.
---

# Commit Messages
...body copied verbatim from the .mdc file...
```

## Steps

- Rename `.cursor/rules/always-confirm-before-implementing.mdc` to
  `ask-before-implement-unless-explicit.mdc` and reword it (keep `alwaysApply:true`)
- For each of the 8 rules: create `.claude/skills/<name>/SKILL.md` with corrected
  description and verbatim body, then delete the original `.mdc` file
- Keep `.cursor/rules/forbid-read-ssh.mdc` as-is
- Create `.claude/CLAUDE.md` with the ssh security rule as always-present instruction
- Write [`doc/wip_migrate_rule_to_skill.md`](doc/wip_migrate_rule_to_skill.md)

