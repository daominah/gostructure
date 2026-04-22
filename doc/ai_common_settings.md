# AI Common Settings

## Tools

### Cursor

Cursor is an IDE built around AI models.
It supports chat, inline edits, and agentic workflows directly inside the editor,
which makes it easy to get started for devs new to AI agents.

Good for beginners: the setup is minimal and the AI assistance is visible at every step.

The main downside is pricing.
Cursor charges per token, and costs can grow quickly. Budget carefully if you use it frequently.

### Claude Code

Claude Code is a CLI-based AI coding agent made by Anthropic.
It runs in your terminal and can read, write, and execute code across your project.

It uses a flat subscription model with a usage limit that resets every 5 hours and every week.

Claude Code is my primary AI coding tool.

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

Rules are persistent context that the agent always includes in every session.
Use them for security boundaries, personal preferences, project conventions, etc.

- Claude Code: `.claude/CLAUDE.md` or `CLAUDE.md` in user home or project dir.
- Cursor: `.mdc` files in `.cursor/rules/` in project dir.
  User rules need to be copied manually to the IDE settings.

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
The directory can also include scripts, templates, and reference files
that the agent uses when the skill is active.

- Claude Code: place skill directories under `.claude/skills/`.
  Let the agent load it automatically when relevant (based on the description)
  or invoke with `/skill-name` in the chat.
- Cursor: can also load skills from `.claude/skills/`,
  so skills in this repo work in both tools.

Copy this repo's skills to your home directory (so they apply to all projects)
by running [install_skills_to_home.sh](../.claude/install_skills_to_home.sh).

References:

- [Open standard Agent Skills](https://agentskills.io/home)
- [Claude Code Skills](https://code.claude.com/docs/en/skills#extend-claude-with-skills)
- [Cursor Skills](https://cursor.com/docs/context/skills)

## MCP Servers

MCP (Model Context Protocol) is an open standard
for connecting AI agents to external data sources.

This reduces time spent switching between tools and manually gathering context.
With MCP, agents can read design docs in Google Drive, update tickets in Jira,
pull data from Slack, or use your own custom tooling.

Some common MCP endpoints:
[Linear](https://linear.app/docs/mcp),
[Atlassian](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/setting-up-ides/#Cursor),
[Slack](https://docs.slack.dev/ai/mcp-server), etc.

GitHub's integration works by default via the `gh` CLI, no MCP needed.
It handles git operations and creating pull requests with proper descriptions.

Cursor stores MCP server lists in `mcp.json`:

- Project scope: `.cursor/mcp.json`
- User scope: `~/.cursor/mcp.json`

Claude Code MCP servers can be added via
[claude.ai/settings/connectors](https://claude.ai/settings/connectors)
or by CLI `claude mcp add`

Added servers are stored in `~/.claude.json` (not meant for manual editing).

For project-shared servers, edit `.mcp.json` at the project root.

## Status Line (Claude Code)

Claude Code can display a status line at the bottom of the terminal.
Request it to display your preferred information. Example:

```
/statusline use this format `Model: Opus 4.6, Context: 24% used 48k/200k tokens`
```

The default statusline script uses `jq`. On Windows, install it via:

```bash
winget install jqlang.jq  # jq is automatically added to PATH after install
```

## Plugins (Claude Code)

Plugins are community-built extensions that add capabilities to Claude Code,
such as new skills, MCP servers, and hooks.

Some common plugins:

| Plugin                   | Type    | Usage                                                                               |
|--------------------------|---------|-------------------------------------------------------------------------------------|
| claude-code-setup        | Skill   | Answers questions about Claude Code features and recommends tools and automations.  |
| claude-md-management     | Skill   | Audits and improves CLAUDE.md files; appends learnings from a session.              |
| skill-creator            | Skill   | Helps create, modify, and evaluate skills.                                          |
| gopls-lsp                | Passive | Go language server for code intelligence. No need for user or Claude invocation.    |
| explanatory-output-style | Hook    | Injects a system prompt that adds educational insights about implementation choices |
| context7                 | MCP     | Retrieves up-to-date documentation for libraries via MCP.                           |
| pyright-lsp              | Passive | Python language server for code intelligence.                                       |
| typescript-lsp           | Passive | JavaScript/TypeScript language server for code intelligence.                        |
| frontend-design          | Skill   | Creates distinctive, production-grade frontend interfaces with high design quality. |

Export installed plugins as a reinstall script:

```bash
# run the following commands from the root of this repo
PLUGINS=$(jq -r '.plugins | keys[]' ~/.claude/plugins/installed_plugins.json)
echo "# Auto-generated with the script in ai_common_settings.md" > .claude/install_plugins.sh
echo "$PLUGINS" | sed 's/^/claude plugin install /' >> .claude/install_plugins.sh
```

Update all installed plugins to latest:

```bash
jq -r '.plugins | keys[]' ~/.claude/plugins/installed_plugins.json \
    | xargs -I{} claude plugin update {}
```

## Hooks (Claude Code)

Hooks are shell commands the CLI runs automatically on events
(session start, tool use, stop, and others). They make an action deterministic,
so the agent does not have to remember a CLAUDE.md rule.

Typical use case: always load short essential knowledge about the project or company
when a new Claude session starts, so the agent never misses it.

To ask the agent to set one up, the only inputs it needs are:

- **Trigger directories**: where the session must start for the hook to fire.
- **Target context**: which files or directories to inject into the session context.

Verify hooks work by the `SessionStart:startup` log on session start.

### Cost

Always-on context is not free. It eats a percent of the context window.
Be careful with trigger directories.
Prompt caching absorbs most of the repeated cost.

## Analyzing Your Usage (Claude Code)

Analyze past sessions to find friction patterns and setup gaps worth fixing.

- `/insights` (built-in): narrative HTML report, 30-day window, single machine.
  Polished and quick to skim, but suggestions tend to be generic.
- `/agent-conversation-analysis` (custom skill in this repo):
  per-task star scoring with correction counts and setup gaps.
  Cross-references commits against Claude's edits to estimate
  how much code was written manually, and merges sessions across machines,
  so the suggestions stay closer to your actual workflow.

## Other Extensions (Claude Code)

| Extension   | Description                                                                                                              |
|-------------|--------------------------------------------------------------------------------------------------------------------------|
| Subagents   | Spawn isolated child agents for focused subtasks (e.g. code review, exploration). Results report back to the main agent. |
| Agent Teams | Multiple independent sessions coordinate via a shared task list. Experimental, disabled by default.                      |
| Hooks       | Run shell commands automatically on events, e.g. auto-format after edits, block writes to protected files.               |
| Commands    | Legacy predecessor of Skills.                                                                                            |
