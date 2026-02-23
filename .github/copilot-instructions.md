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

Do not include AI co-author trailers (e.g. `Co-authored-by: Cursor`).

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

Follow this layout when adding or organizing code.

## Directory Layout

| Directory     | Purpose                                                                             |
|---------------|-------------------------------------------------------------------------------------|
| `cmd/{app}/`  | Wires dependencies and starts the app                                               |
| `pkg/logic/`  | Business logic, interfaces, domain schemas. Testable without external dependencies. |
| `pkg/driver/` | Implementations of logic interfaces (database, HTTP, etc.).                         |
| `pkg/base/`   | Shared utilities (logger, uuid, helpers, ...)                                       |
| `config/`     | Configuration files (e.g. `.env.example`)                                           |
| `web/`        | Frontend assets (HTML, JS)                                                          |
| `doc/`        | Design docs, user guides, API specs                                                 |

## Package Conventions

**`pkg/logic/`**

- `interface.go`: Defines interfaces for infrastructure and external dependencies.
- `interface_mock.go`: Mock implementations used to simulate external dependencies in tests.  
  (We use the `MockSomething` naming convention for both stubs and mocks.)
- `schema.go`: Defines domain data structures (models).
- `app.go`: The `App` struct holds dependencies; its methods implement business logic.
- This package must be testable without external setup.
- It must not import any driver packages.
- Depends on interfaces, not concrete implementations.

**`pkg/driver/`**

- Implements interfaces from `pkg/logic`.
- One subpackage per external concern:
  `database/`, `httpsvr/`, `external_provider/`, ...
- The `database/` package additionally contains SQL migrations.

**`pkg/base/`**

- Pure utilities with no business logic.
- Must not depend on `logic` or `driver`.

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

Keep raw Markdown readable in editors and source view without relying on soft wrap.
Assume a typical view width of about 80 to 100 characters.

Break lines in raw Markdown at around 80 characters (maximum 100).
Rendered Markdown is not affected by line breaks in the source.

Prefer breaking lines at semantic boundaries, such as the end of a sentence
or after a logical clause, for example after a comma that ends a phrase,
rather than strictly by character count.

It is acceptable to exceed 80 characters slightly
if a natural break point is close and readability is preserved.

Tables are an exception and do not require manual line breaks.

This file itself is an example of this writing style.
Some lines could be written as a single line,
but they are intentionally broken to improve readability in raw form.

# Writing Style

Avoid dashes in the middle of sentences. Prefer rephrasing or using colons instead.

Bad: "This is a feature - it does something"
Good: "This is a feature: it does something"
Good: "This is a feature that does something"