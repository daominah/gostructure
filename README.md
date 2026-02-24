# gostructure

This gostructure is my template repository for starting a new Go service, with an optional web UI.
It is inspired by Clean Architecture and golang-standards/project-layout.

To start a new project, copy this directory, rename it to your new project name,
then go into the directory and remove the .git folder.
Rename `cmd/main` to something meaningful (e.g. `cmd/api-server`) and update the
Dockerfile build path and any scripts that reference it.

## Deployment

### Running with Docker

#### Local Development

For local development,
you can run all services except the main app with docker compose,
then run the application directly with Go run:

```bash
# Start all services except the main application
docker compose up -d --scale application=0

# Run the application locally
go run ./cmd/main
```

Environment variables are loaded from `config/.env` or `config/.env.example`.
See `config/.env.example` for configuration details.

To start fresh and remove all existing persistent data:

```bash
docker compose down -v
# then compose up
```

#### Production

Build and run all services including the main application:

```bash
docker compose build
docker compose up -d
```

The application will be available at `http://host:20808`.

Consider using a secret management solution to securely store environment variables
and inject them into containers, such as Bitwarden Secrets Manager.

## Code Structure

### `cmd`

Main executable: `cmd/main/main.go`.

One-off scripts:

- `cmd/script-import-data`: do something one-off, manually run when needed.

### `config`

Environment variables for initializing the app. See `config/.env.example` for available options.

### `pkg/logic`

Business logic that can be tested without external resources.
Mock interfaces are used to simulate external dependencies in tests.

### `pkg/driver`

Packages that implement interfaces with concrete connections
(database, HTTP client, HTTP server, websocket, message queue, file storage, etc.).

### `pkg/base`

Reusable base packages (logger, UUID, project root dir utilities).

### `web`

Web application user interface. Intended to be served by the same process as the API.
The JavaScript code can call the API by relative paths.
