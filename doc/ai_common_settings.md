# AI Common Settings

## Tools

### Cursor

Cursor is an IDE built around AI models.
It supports chat, inline edits, and agentic workflows directly inside the editor,
which makes it easy to get started for devs new to AI Agents.

Good for beginners: the setup is minimal and the AI assistance is visible at every step.

The main downside is pricing.
Cursor charges per token, and costs can grow quickly. Budget carefully if you use it frequently.

### Claude Code

Claude Code is a CLI-based AI coding agent made by Anthropic.
It runs in your terminal and can read, write, and execute code across your project.

It uses a flat subscription model, there is a usage limit that resets every few hours (and every week).

Currently transitioning to Claude Code as the primary AI coding tool.

### GitHub Copilot

GitHub Copilot provides AI-powered code completion inside your editor.
It suggests lines or blocks of code as you type in IDEs.
It uses a fast model and small context window, not suitable for complicated tasks.

## Configuring

Both Cursor and Claude Code support rules, skills, and settings that shape the agent's behavior.
These can be scoped to a user's home directory (affecting all projects)
or to a specific project directory.
This repo includes configurations that can be applied to either tool.

## Rules

Rules are always-on instructions the agent follows in every session.
Use them for non-negotiable constraints: security boundaries, workflow policies, ...

- **Cursor**: place `.mdc` files in `.cursor/rules/`.
  Rules are injected into every chat automatically.
- **Claude Code**: place instructions in `.claude/CLAUDE.md` or `CLAUDE.md` at project root.

## Skills

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
  Let the agent load it automatically when relevant (based on the description)
  or invoke with `/skill-name` in the chat.
- **Cursor**: also can load skills from `.claude/skills/`,
  so skills in this repo work in both tools.

References:

- [Open standard Agent Skills](https://agentskills.io/home)
- [Claude Code Skills](https://code.claude.com/docs/en/skills#extend-claude-with-skills)
- [Cursor Skills](https://cursor.com/docs/context/skills)

## MCP Servers

MCP (Model Context Protocol) is an open standard for connecting AI agents to external data sources.

This reduces time spent switching between tools and manually gathering context.
With MCP, agents can read design docs in Google Drive, update tickets in Jira,
pull data from Slack, or use your own custom tooling.

Some common MCP endpoints:
[Linear](https://linear.app/docs/mcp),
[Atlassian](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/setting-up-ides/#Cursor),
[Slack](https://docs.slack.dev/ai/mcp-server), etc.

(GitHub integration works by default via the `gh` CLI, no MCP needed.
It handles git operations, creating pull requests with proper descriptions.)

**Cursor** stores MCP server lists in `mcp.json`:

- Project scope: `.cursor/mcp.json`
- User scope: `~/.cursor/mcp.json`

**Claude Code** MCP servers can be added via
[claude.ai/settings/connectors](https://claude.ai/settings/connectors)
or by CLI `claude mcp add <name> -- <command> [args...]`

Added servers are stored in `~/.claude.json` (not meant for manual editing).

For project-shared servers, edit `.mcp.json` at the project root.

```
