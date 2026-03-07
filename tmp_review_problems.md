# Review Problems

## High Priority

### Missing `UpdateProduct` HTTP endpoint
`pkg/driver/httpsvr/api.go:12-18`
`logic.Database` interface defines `UpdateProduct`, the DB layer implements it,
but no route is wired in `NewHandlerAPI`. The feature is unreachable.

- [x] Ignore:
- [ ] Fix:

### `CreateProductHandler` accepts empty `ID`
`pkg/driver/httpsvr/product_api.go:13-34`
The import script (`cmd/script-import-data/script_import_data.go:66`) generates a UUID
when `ID` is empty. The HTTP handler does not — a `POST /api/v1/product` with no `ID`
field inserts an empty string as the primary key.
Either validate and reject it, or auto-generate a UUID.

- [ ] Ignore:
- [x] Fix: auto-generate a UUID

### Internal errors exposed in HTTP responses
`pkg/driver/httpsvr/product_api.go:27,50,65`
```go
http.Error(w, fmt.Sprintf("error CreateProduct: %v", err), http.StatusInternalServerError)
```
`err` contains DB-level details (`"db.Exec INSERT: ERROR: ..."`) returned directly to the caller.
Log the full error server-side and return a generic message to the client:
```go
log.Printf("error CreateProduct: %v", err)
http.Error(w, "internal server error", http.StatusInternalServerError)
```

- [x] Ignore:
- [ ] Fix:

### `sslmode=disable` hardcoded
`pkg/driver/database/postgresql.go:22`
```go
connStrFormat := "postgres://%s:%s@%s:%s/%s?sslmode=disable"
```
Cannot be overridden without changing code. Make it configurable via an env var for production.

- [x] Ignore:
- [ ] Fix:

## Medium Priority

### `cmd/main/` should be renamed
Per `go-project-structure` convention: use a meaningful name rather than the generic `main`.
Rename to `cmd/gostructure/` or `cmd/server/`. This also changes the default binary name
produced by `go build`.

- [x] Ignore: intentional because this repo is a template, not have a purpose/name for the main app.
- [ ] Fix:

### Error wrapping uses non-standard double `%w`
`pkg/driver/database/product.go:24,39,82`
Per `go-personal-convention`, errors should use a single `%w` with context as the prefix.
Current code:
```go
return fmt.Errorf("%w: %v, db.Exec INSERT: %w", model.ErrDuplicateProductID, product.ID, err)
return fmt.Errorf("%w: %v, db.QueryRow SELECT: %w", model.ErrProductNotFound, id, err)
return fmt.Errorf("%w: %v, db.Exec UPDATE 0 rowsAffected", model.ErrProductNotFound, product.ID)
```
Should be:
```go
return fmt.Errorf("db.Exec INSERT duplicate ID %v: %w", product.ID, model.ErrDuplicateProductID)
return fmt.Errorf("db.QueryRow SELECT id %v: %w", id, model.ErrProductNotFound)
return fmt.Errorf("db.Exec UPDATE id %v 0 rowsAffected: %w", product.ID, model.ErrProductNotFound)
```

- [ ] Ignore:
- [x] Fix: the sentinel error position is fine, just replace the last "%w" to "%v",
  so unwrap returns the correct sentinel error and msg still contains error details.

### `App` has no methods; business logic bypassed
`pkg/driver/httpsvr/api.go:14-16`, `pkg/logic/app.go`
`NewHandlerAPI` accepts `*logic.App` but passes `app.Database` directly to handlers,
bypassing the logic layer entirely. Per `go-project-structure`, `App` methods should
implement business logic. HTTP handlers should call `app.CreateProduct(...)`, not
`app.Database.CreateProduct(...)` directly.

- [ ] Ignore:
- [x] Fix: yes, add methods for App.

### `SearchProducts` returns unbounded results
`pkg/driver/database/product.go:48-68`
No `LIMIT` clause — on a large table this could return millions of rows.
Add a reasonable default limit or accept a `limit` parameter.

- [x] Ignore:
- [ ] Fix: 

### `MockDatabase` is not thread-safe
`pkg/logic/interface_mock.go:11-52`
The `products` map has no mutex. Parallel subtests calling `CreateProduct`/`GetProduct`
concurrently will race. Add a `sync.RWMutex` or document the limitation.

- [ ] Ignore:
- [x] Fix: yes, but use sync.Mutex for simple, lock on all read or write operations.

### `Dockerfile` Go version mismatch
`Dockerfile:2`
```dockerfile
FROM golang:1.23.12-bookworm AS builder
```
`go.mod` declares `go 1.26` but the builder image uses `golang:1.23`. Align them.

- [ ] Ignore:
- [x] Fix:

## Low Priority

### No input validation
`pkg/driver/httpsvr/product_api.go:13-34`
`Name` can be empty, `Price` can be negative. Add basic validation before calling the database.

- [x] Ignore:
- [ ] Fix:

### `web.go` filesystem dependency instead of `embed.FS`
`pkg/driver/httpsvr/web.go:15-27`
Requires the source tree at runtime. The Dockerfile works around this by copying the entire
build context into the runtime image, bloating it. Use `embed.FS` instead.

- [ ] Ignore:
- [x] Fix: yes, add a `web_files_embed.go` here, Dockerfile dont need source tree anymore

### `TestCustomLogger` has no assertion
`pkg/base/base_test.go:11-17`
The test only calls `log.Printf` and `t.Logf` with no assertions. It will never fail.
Either assert the output format or remove it and document it as a manual step.

- [x] Ignore:
- [ ] Fix:
