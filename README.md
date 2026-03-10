# gostructure

A template repository for starting a new Go service.

Business logic code is separated from infrastructure,
making the system easier to test and change if needed.
It also includes common boilerplate files you will likely need.

Inspired by Clean Architecture and golang-standards/project-layout.

## Code Structure

See [go-project-structure](.claude/skills/go-project-structure/SKILL.md).

## Working with AI Agents

- [Mindset and guidelines for using AI effectively](doc/ai_usage_mindset.md)
- [Agent workflow and basic concepts](doc/ai_usage_practices.md)
- [Tool-specific settings: rules, skills, MCP](doc/ai_common_settings.md)

## How to start a new project

- Copy this directory, rename it to your new project name,
  then remove the `.git` folder.
- Update the module path in `go.mod` and all import statements
  (use Replace in All Files or a similar IDE feature).
- Rename `cmd/main` to something meaningful (e.g. `cmd/shop-assistant`)
  and update the Dockerfile build path and any scripts that reference it.
- If you use Docker or config,
  update project-specific names (e.g. database name, container names).

## Deployment

### Local Development

Environment variables are loaded from `config/.env` or `config/.env.example`.
See `config/.env.example` for configuration details.

Run all services except the main application with docker compose,
then run the application directly with Go (or debug mode in your IDE).

```bash
# Start all services except the main application
docker compose up -d --scale application=0

# Run the application locally
go run ./cmd/main
```

To start fresh and remove all existing persistent data:

```bash
docker compose down -v
# then compose up
```

### Production

Build and run all services including the main application.
The application will be available at `http://host:20808`.
For production, use a secret management solution (e.g. Bitwarden Secrets Manager).
