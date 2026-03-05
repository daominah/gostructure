# AI Usage Practices

## Common AI Tools

### Cursor

Cursor is an IDE built around AI models.
It supports chat, inline edits, and agentic workflows directly inside the editor,
which makes it easy to get started for devs new to AI Agents.

Good for beginners: the setup is minimal and the AI assistance is visible at every step.

The main downside is pricing.
Cursor charges per token, and costs can grow quickly
when you use it heavily or run long agentic tasks.
Budget carefully if you use it frequently.

### Claude Code

Claude Code is a CLI-based AI coding agent made by Anthropic.
It runs in your terminal and can read, write, and execute code across your project.

It uses a flat subscription model,
there is a usage limit that resets every few hours (and every week).

Currently transitioning to Claude Code as the primary AI coding tool.

### GitHub Copilot

GitHub Copilot provides AI-powered code completion inside your editor.
It suggests lines or blocks of code as you type in IDEs.
It uses a fast model and small context window, not suitable to complicated tasks.

## Basic concepts

## Configuring AI Agents

Both Cursor and Claude Code support rules, skills, and settings
that shape the agent's behavior.
These can be scoped to a user's home directory (affecting all projects)
or to a specific project directory.
This repo includes configurations that can be applied to either tool.

### Rules

Rules are always-on instructions the agent follows in every session.
Use them for non-negotiable constraints: security boundaries, workflow policies, ...

- **Cursor**: place `.mdc` files in `.cursor/rules/`.
  Rules are injected into every chat automatically.
- **Claude Code**: place instructions in `.claude/CLAUDE.md` or `CLAUDE.md` at project root.

### Skills

Skills are reusable instruction packages that teach agents how to perform specific tasks
(e.g. codebase visualization, Excel processing, coding conventions, etc.).

Unlike rules, which are always loaded into every session,
only each skill's **name** and **description** are loaded into context,
while full instructions are loaded on demand
when the agent decides, based on the description, that a skill is relevant.

Long rules can be converted into skills to save context window space.

A skill is a directory containing a `SKILL.md` (required)
with a name, description, and prompt body.
The directory can also include scripts, templates and reference files
that the agent uses when the skill is active.

- **Claude Code**: place skill directories under `.claude/skills/`.
  Let the agent load it automatically when relevant
  or invoke with `/skill-name` in the chat.
- **Cursor**: also can load skills from `.claude/skills/`,
  so skills in this repo work in both tools.

References:

- [Open standard Agent Skills](https://agentskills.io/home)
- [Claude Code Skills](https://code.claude.com/docs/en/skills#extend-claude-with-skills)
- [Cursor Skills](https://cursor.com/docs/context/skills)

### Settings

**Cursor** stores most settings in `.cursor/` at the project root or in `~/.cursor/` globally.
See `.cursor/readme_cursor_settings.md` for details on:

- **MCP servers** (`.cursor/mcp.json`):
  connect the agent to external tools like Linear, Jira, or Slack
- **External API keys**: use your own model provider subscription instead of Cursor credits
- **Agent allowlists**: commands and fetch domains the agent is permitted to use without prompting

**Claude Code** is configured via `~/.claude/` globally and `.claude/` per project.
Project-level `CLAUDE.md` is the main entry point for per-repo instructions.

MCP servers for Claude Code use three scopes:

| Scope             | Stored in                   | Shared?            | Use case                                       |
|-------------------|-----------------------------|--------------------|------------------------------------------------|
| `local` (default) | `~/.claude.json`            | No                 | Personal servers for a specific project        |
| `user`            | `~/.claude.json`            | No                 | Personal servers available across all projects |
| `project`         | `.mcp.json` at project root | Yes, commit to git | Team-shared servers                            |

`~/.claude.json` is not meant for manual editing (it also stores OAuth sessions, caches, and other state).
For `local` and `user` scopes, use the CLI to add servers:

```bash
claude mcp add <name> -- <command> [args...]                 # local scope (default)
claude mcp add --scope user <name> -- <command> [args...]    # user scope
claude mcp add --scope project <name> -- <command> [args...]  # writes to .mcp.json
claude mcp list                                               # list configured servers
claude mcp remove <name>                                      # remove a server
```

For `project` scope, you can also edit `.mcp.json` directly at the project root.
Note: `.mcp.json` must be at the project root, not inside `.claude/`.

```json
{
	"mcpServers": {
		"linear": {
			"command": "npx",
			"args": [
				"-y",
				"@linear/mcp-server"
			],
			"env": {
				"LINEAR_API_KEY": "${LINEAR_API_KEY}"
			}
		}
	}
}
```

Environment variable expansion (`${VAR}` and `${VAR:-default}`) is supported in `.mcp.json`,
so the team can share the file while each member supplies their own API keys via shell env.

For general Claude Code settings (permissions, env vars, hooks), edit these files directly:

| File                          | Scope           | Purpose                                       |
|-------------------------------|-----------------|-----------------------------------------------|
| `~/.claude/settings.json`     | User global     | Permissions, env vars, hooks for all projects |
| `.claude/settings.json`       | Project, shared | Team-wide settings, committed to git          |
| `.claude/settings.local.json` | Project local   | Personal overrides, gitignored                |
