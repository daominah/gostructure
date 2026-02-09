# gostructure

This gostructure is my template repository for starting a new Go service, with an optional web UI.
It is inspired by Clean Architecture and golang-standards/project-layout.

To start a new project, copy this directory, rename it to your new project name,
then go into the directory and remove the .git folder.

## Deployment

### Running with Docker

#### Local Development

For local development, you can run the database with docker compose,
then run the application directly:

```bash
# Start only the database service
docker compose up -d database

# Run the application locally
go run ./cmd/main
```

Environment variables are loaded from `config/.env` or `config/.env.example`.
See `config/.env.example` for configuration details.

#### Production

Build and start both the database and application:

```bash
docker compose build
docker compose up -d
```

The application will be available at `http://localhost:20808`.

## Code Structure

### `cmd`

Main executable: `cmd/main/main.go`

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
