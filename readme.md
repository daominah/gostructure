# Project Name

Project summary

## Input output detail

## Deployment

This project uses [docker-machine](https://github.com/docker/machine/releases/tag/v0.16.2)
to build and run on remote machines:
* First step, you need to get this repo on remote machines (define in [./s0_build.sh])
* Execute [./s0_build.sh] (from manager host, usually is your computer)
* Edit env config file then execute [./s2_run.sh]

## Structure

### `cmd`

Main executable: `cmd/example`

### `conf`

Environment variables for initializing the app.

### `pkg/core`
Business logic. Can be tested without external resources (database,
HTTP, websocket, message queue, file, ..)

### `pkg/driver`
Calls to external resources.
