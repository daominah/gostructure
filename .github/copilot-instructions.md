# Always Confirm Before Implementing

**CRITICAL**: Before making any code changes or implementations:

1. **ALWAYS ask for confirmation** before changing code,
   unless the user's prompt/question clearly indicates they want implementation
2. When user asks "how to do ...", "what is...", "is it possible...":
   provide information/explanation first, then ask if they want implementation
3. User's prompt/question clearly indicates they want implementation usually has
   some words like "implement", "fix", "add", "change", "do it", ...
   but not limited to these words.

# Commit Messages

Prefer concise commit messages without a lot of bullet points about code changes.
Keep messages focused and to the point of main business logic changes.

Do not include AI co-author trailers or footers of any kind,
such as `Co-authored-by: Cursor` or "Made with Cursor".

# Go Error Formatting

When returning errors in Go, use the format:

```go
fmt.Errorf("previous line or function call that caused the error: %w", err)

// example:
testData, err := os.ReadFile("file_test.html")
if err != nil {
    return fmt.Errorf("error os.ReadFile: %w", err)
}
```

This ensures error wrapping with context about what operation caused the error,
reading the log is enough to know what line of code caused the error.

# Go Project Structure

Follow this layout when adding or organizing code for Go services and applications.

## Directory Layout

| Directory     | Purpose                                                                                  |
|---------------|------------------------------------------------------------------------------------------|
| `cmd/{app}/`  | Loads config from env, wires dependencies, starts the app                                |
| `pkg/model/`  | Domain data structures and related errors (for cross-package error matching).            |
| `pkg/logic/`  | Business logic, interfaces. Testable without external dependencies.                      |
| `pkg/driver/` | Implements interfaces for external interactions (HTTP, database, third-party APIs, etc.) |
| `pkg/base/`   | Shared pure utilities with no business logic (logger, uuid, ...)                         |
| `config/`     | Configuration files. `.env.example` lists env vars to configure.                         |
| `web/`        | Optional simple UI if needed. Served with the API. JS calls API by relative paths.       |
| `doc/`        | Design docs, user guides, tech specs, algorithms, API specs                              |

## Conventions

### `cmd/`

Contains the main service executable and any optional one-off scripts,
one subdirectory each.

The subdirectory name determines the default binary name from `go build`,
so use a meaningful name rather than something generic like `main`.

Multi-word executable names use hyphens, following common CLI conventions,
for example `script-import-data`.

Source file names use `snake_case`, following Go conventions,
for example `script_import_data.go`.

### `pkg/model/`

- Keep everything in a single `model.go` file, or split into one file per entity if it grows
  too large (e.g. `product.go` containing the `Product` struct and its related errors).

### `pkg/logic/`

- `interface.go`: Defines interfaces for infrastructure and external dependencies.
- `interface_mock.go`: Mock implementations for tests or interfaces not yet implemented
  (use `MockSomething` naming for both stubs and mocks).
- `app.go`: The `App` struct holds dependencies; its methods implement business logic.
- Must be testable without external setup.
- Must not import any `driver` packages.
- Depends on interfaces, not concrete implementations.

### `pkg/driver/`

- Implements the interfaces defined in `pkg/logic/interface.go`.
- One subpackage per external concern:
  `database/`, `httpsvr/`, `external_provider/`, etc.
- `database/` also contains SQL migrations.

# SQL Formatting Rules

When writing or formatting SQL code, follow these style guidelines:

## General Formatting

- Use spaces around parentheses in CREATE statements:
  `CREATE INDEX idx_name ON table_name (col1, col2)` not
  `CREATE INDEX idx_name ON table_name(col1, col2)`
- Align column definitions in CREATE TABLE statements for readability
- Use consistent indentation (4 spaces)

## Index Definitions

- Format with spaces around parentheses and proper indentation:
  ```sql
  CREATE INDEX idx_name ON table_name (col1, col2)
      WHERE condition;
  ```

## Trigger Definitions

- Split trigger clauses across multiple lines:
  ```sql
  CREATE TRIGGER trigger_name
      AFTER INSERT
      ON table_name
      FOR EACH ROW
  EXECUTE FUNCTION function_name();
  ```

## UPDATE Statements

- Align SET clauses vertically:
  ```sql
  UPDATE table_name
  SET col1   = value1,
      col2   = value2,
      col3   = value3
  WHERE condition;
  ```

## ON CONFLICT Clauses

- Format multi-line for readability:
  ```sql
  ON CONFLICT (batch_id) DO UPDATE SET queued_count = batch_stats.queued_count + 1,
                                       is_completed = FALSE;
  ```

## SQL Comments

- Keep comments concise and informative
- Align comment formatting with code structure

# Unit Test Comments

Use the GIVEN/WHEN/THEN format for unit test comments:

- **GIVEN**: Setup/preconditions/base data
- **WHEN**: Action/function being tested
- **THEN**: Expected result/verification

This format makes tests more readable and clearly structures the test flow.

# Markdown Writing Style

## Goal

Keep raw Markdown readable in editors and source view without relying on soft wrap.
Assume a typical view width of about 80 to 100 characters.

## Rules to achieve the goal

The target is the raw Markdown source, not rendered output in a browser or Markdown viewer.

Generally break lines in raw Markdown at around 80 characters.

Prefer breaking lines at semantic boundaries, such as the end of a sentence
or after a logical clause, for example after a comma that ends a phrase,
rather than strictly by character count.

Prefer breaking lines at semantic boundaries; it is acceptable to exceed 80 characters slightly
(as long as the length does not exceed 100 characters).
This is more readable than strictly breaking by character count.

Tables are an exception and do not require manual line breaks.

## Example for line breaks at semantic boundaries

For example, the next paragraph has **good** line breaks at semantic boundaries:

The VAPID key pair we generate proves that the push request comes from your server.
Each push request is signed with the private key,
the push service verifies the signature before delivering.

The following paragraph will produce the same rendered output,
but the line breaks are chosen to strictly enforce the 80-character limit (**not as good**),
which is not as readable in the raw Markdown:

The VAPID key pair we generate proves that the push request comes from your
server. Each push request is signed with the private key; the push service
verifies the signature before delivering.

And absolutely avoid **bad** (all in one long line):

The VAPID key pair we generate proves that the push request comes from your server. Each push request is signed with the private key; the push service verifies the signature before delivering.

# Writing Style

Avoid dashes in the middle of sentences. Prefer rephrasing or using colons instead.

Bad: "This is a feature - it does something"
Good: "This is a feature: it does something"
Good: "This is a feature that does something"