#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# run this script in project root directory before commit

# optional format the whole repo
echo "running goimports ..."
goimports -w .
echo "end goimports"

# Vet examines Go source code and reports suspicious constructs
echo "running go vet ..."
go vet ./...
echo "end go vet"

# Run all unittests, include database tests, which require Docker compose to be running.
# go clean -testcache
echo "running go test ..."
go test -v ./...
# go test ./...
echo "end go test"

echo "========================================"
echo "All tests passed!"
