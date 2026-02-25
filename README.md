# gostructure

A template repository for starting a new Go service.

Business logic code is separated from infrastructure,
making the system easier to test and change if needed.
It also includes common boilerplate files you will likely need.

Inspired by Clean Architecture and golang-standards/project-layout

## How to start a new project

1. Copy this directory, rename it to your new project name, then remove the `.git` folder.
2. Update the module path in `go.mod` and all import statements across the codebase
   (use Replace in All Files or a similar IDE feature).
3. Rename `cmd/main` to something meaningful (e.g. `cmd/shop-assistant`)
   and update the Dockerfile build path and any scripts that reference it.
4. If you use Docker or config, update project-specific names (e.g. database name, container names).

## Code Structure

See [.cursor/rules/go-project-structure.mdc](.cursor/rules/go-project-structure.mdc).
The structure rules can be used as configuration for AI code generation.

As we’re now in the AI era, I’ve been learning how to use AI more
effectively and have documented what I’ve learned here:

[How to Use AI Effectively](README_use_ai_effectively.md)

## Deployment

### Local Development

Environment variables are loaded from `config/.env` or `config/.env.example`.
See `config/.env.example` for configuration details.

Run all services except the main app with docker compose,
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
