# AI Usage Practices

## Common AI Tools

### Cursor

Cursor is an IDE built around AI models. It supports chat, inline edits, and agentic workflows
directly inside the editor, which makes it easy to get started for devs new to AI Agents.

Good for beginners: the setup is minimal and the AI assistance is visible at every step.

The main downside is pricing. Cursor charges per token, and costs can grow quickly
when you use it heavily or run long agentic tasks. Budget carefully if you use it frequently.

### Claude Code

Claude Code is a CLI-based AI coding agent made by Anthropic.
It runs in your terminal and can read, write, and execute code across your project.

It uses a flat subscription model, here is a usage limit that resets every few hours (and every week).

Currently transitioning to Claude Code as the primary AI coding tool.

### GitHub Copilot

GitHub Copilot provides AI-powered code completion inside your editor.
It suggests lines or blocks of code as you type in IDEs.
It uses a fast model and small context window, not suitable to complicated tasks.

## Basic concepts

## Configuring AI Agents

Both Cursor and Claude Code support rules, skills, and settings that shape how the agent behaves
in your project. This repo includes configurations for both tools.

### Rules

Rules are always-on instructions the agent follows in every session.
Use them for non-negotiable constraints: coding conventions, security boundaries, workflow policies.

- **Cursor**: place `.mdc` files in `.cursor/rules/`. Rules with `alwaysApply: true` are injected
  into every chat automatically.
- **Claude Code**: place instructions in `.claude/CLAUDE.md`. The agent reads this file at the
  start of every session.

Rules in this repo:

| Rule                                   | Applies to          | Purpose                                                                       |
|----------------------------------------|---------------------|-------------------------------------------------------------------------------|
| `ask-before-implement-unless-explicit` | Cursor              | Ask for a plan before writing code unless the user explicitly says to proceed |
| `forbid-read-ssh`                      | Cursor, Claude Code | Never access `.ssh` directories at any path                                   |

### Skills

Skills are on-demand prompts the agent loads when you invoke them by name.
Use them for repeatable tasks where you want consistent behavior without repeating instructions.

- **Claude Code**: place skill directories under `.claude/skills/`. Each skill has a `SKILL.md`
  with a name, description, and prompt body. Invoke with `/skill-name` in the chat.
- **Cursor**: skills are not natively supported; use rules or chat snippets instead.

Skills in this repo:

| Skill                    | Purpose                                                              |
|--------------------------|----------------------------------------------------------------------|
| `commit-messages`        | Concise commit messages focused on business logic, no AI attribution |
| `go-personal-convention` | Personal Go style conventions                                        |
| `go-project-structure`   | Go directory layout and package conventions                          |
| `slack-messaging`        | Draft Slack messages and confirm before sending                      |
| `sql-formatting`         | SQL formatting and style                                             |
| `test-comments`          | GIVEN/WHEN/THEN comment format for unit tests                        |
| `writing-style`          | Prose style: no mid-sentence dashes, straight quotes                 |
| `writing-style-markdown` | Markdown conventions                                                 |

### Settings

**Cursor** stores most settings in `.cursor/` at the project root or in `~/.cursor/` globally.
See `.cursor/readme_cursor_settings.md` for details on:

- **MCP servers** (`.cursor/mcp.json`): connect the agent to external tools like Linear, Jira, or Slack
- **External API keys**: use your own model provider subscription instead of Cursor credits
- **Agent allowlists**: commands and fetch domains the agent is permitted to use without prompting

**Claude Code** is configured via `~/.claude/` globally and `.claude/` per project.
Project-level `CLAUDE.md` is the main entry point for per-repo instructions.
