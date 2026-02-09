#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# run this script in project root directory before commit

# optional format the whole repo
goimports -w .

# Vet examines Go source code and reports suspicious constructs
go vet ./...

# Run all unittests, include database tests, which require Docker compose to be running.
go clean -testcache
# go test -v ./...
go test ./...

echo "========================================"
echo "All tests passed!"
