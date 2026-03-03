# Cursor Settings Notes

## MCP Servers

MCP (Model Context Protocol) allows AI agents to securely access external tools and data.

MCP servers are configured in `.cursor/mcp.json` in the project root,
or in `~/.cursor/mcp.json` to apply globally across all projects on your machine.

Some common provider-hosted MCP endpoints:

- **linear**: task and issue tracking via [Linear](https://linear.app/docs/mcp)
- **atlassian**: Jira and Confluence via [Atlassian](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/setting-up-ides/#Cursor)
- **slack**: search and messaging via [Slack](https://docs.slack.dev/ai/mcp-server)

Custom MCP servers can also be run locally by pointing `command` to any executable.

```
		"my-mcp": {
			"command": "/path/to/my-mcp-server",
			"args": [
				"--port",
				"8080"
			]
		}
```

## External Model API Keys

Instead of consuming Cursor credits, you can use your own subscription
from [supported model providers](https://cursor.com/docs/settings/api-keys).

`Cursor Settings` > `Models` > `API Keys`

Note that when I use my Anthropic API Key, in Agent models selection,
I only see some old claude-3 models, TODO: how to select the latest claude-4 models?

## Agent Allowlists

The Command Allowlist and Fetch Domain Allowlist are stored in an internal
SQLite database, not in `settings.json`.
The only supported way to add entries is one by one through the Cursor UI:

`File` > `Preferences` > `Cursor Settings` > `Agents`

### Command Allowlist

```text
cat
cd
echo
git add
git branch
git diff
git log
git status
go
goimports
grep
head
jq
ls
mkdir
sleep
tail
wc
which
```

### Fetch Domain Allowlist

Wildcards like `*.example.com` cover all subdomains.

```text
*.atlassian.com
*.cursor.com
developers.facebook.com
*.github.com
*.githubusercontent.com
*.go.dev
*.google.com
linear.app
*.npmjs.com
open.shopee.com
partner.tiktokshop.com
*.slack.com
*.slack.dev
stackoverflow.com
```
