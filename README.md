# Project name

Project summary (╯°□°）╯︵ ┻━┻

## Input output detail

## Deployment

Execute [build_run.sh](build_run.sh) to build and run a local docker container. 

## Code structure

### `cmd`

Main executable: `cmd/example`

### `conf`

Environment variables for initializing the app.

### `pkg/core`

Business logic. Can be tested without external resources (database,
HTTP, websocket, message queue, file, ..).

### `pkg/driver`

Calls to external resources.
