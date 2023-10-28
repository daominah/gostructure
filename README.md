# Project name

Project summary (╯°□°）╯︵ ┻━┻

## Input output detail

## Deployment

Execute [build_run.sh](build_run.sh) to build and run a local docker container. 

## Code structure

This project structure is inspired by <https://github.com/golang-standards/project-layout>.

### `cmd`

Main executable: `cmd/example`

### `configs`

Environment variables for initializing the app.

### `internal/core`

This app core business logic. Can be tested locally without external connections.

### `internal/driver`

This directory contains packages that implement interface with concrete
connection (database, HTTP client, HTTP server, websocket, message queue,
file storage, ..).

### `web`

User interface.
