# ProjectName

ProjectName is just a project template.

## Deployment

Execute [build_run.sh](build_run.sh) to build and run a local docker container.

## API detail

APIs request response format.

Maybe a URL to OpenAPI Swagger.

## Code structure

This project structure is inspired by <https://github.com/golang-standards/project-layout>.
Some directories name are changed because I don't like plural as dir name.

### `cmd`

Main executable: `cmd/main_example/main.go`

### `config`

Environment variables for initializing the app.

### `internal/core`

This app core business logic. Can be tested locally without external connections.

### `internal/driver`

This directory contains packages that implement interface with concrete
connection (database, HTTP client, HTTP server, websocket, message queue,
file storage, ..).

### `pkg`

Package can be reused in other projects.

### `web`

Web application user interface.
