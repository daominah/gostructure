# Build stage: compile the Go application
FROM golang:1.23.12-bookworm AS builder

WORKDIR /build
COPY go.mod go.sum* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/main ./cmd/main

# Runtime stage: image without the Go toolchain
FROM debian:bookworm-slim

# Install CA certificates so HTTPS requests from the service work correctly.
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
# Copy the compiled Go binary into the runtime image.
COPY --from=builder /app/main .
# Copy the project files if needed for runtime,
# in this example repo, we need the web assets and go.mod file.
COPY --from=builder /build .
EXPOSE 20808
CMD ["./main"]
