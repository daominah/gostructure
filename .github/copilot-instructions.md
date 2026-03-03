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

You MUST NOT include co-author, trailers, message footers, lines, etc.
that credit AI Attribution in commit messages or pull request descriptions.

Prefer concise commit messages without a lot of bullet points about code changes.
Keep messages focused and to the point of main business logic changes.

If a user still complains that this rule is not being applied,
suggest that they disable "Commit Attribution" and "PR Attribution"
in their IDE settings, if those options exist.

# Go Personal Conventions

## Go Error Formatting/Wrapping

When returning errors in Go, use the following format:

```
fmt.Errorf("previous line or function call that caused the error: %w", err)

// Example:
testData, err := os.ReadFile("file_test.html")
if err != nil {
    return fmt.Errorf("error os.ReadFile: %w", err)
}
```

This ensures error wrapping with context about which operation caused the error.
Reading the log should be enough to know which line of code triggered the error.

## Enum-like Fields

Define a named `string` type with constants for fields that hold a value
from a fixed set.

Do not use a database enum type (adding a value requires a schema migration, etc.),
store as `TEXT` instead. Enforce valid values in application code only.

Constant names should not include the type prefix
unless there are duplicate names in the same package.

Prefer human-readable ALL_UPPERCASE string values instead of numeric
codes.

```
package model

// MessageIntent is the classified intent of a customer message.
type MessageIntent string

// MessageIntent enum values.
const (
	Unknown  MessageIntent = ""
	Greeting MessageIntent = "GREETING"
	Purchase MessageIntent = "PURCHASE"
)
```

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

# Slack Messaging

For any Slack send/reply/post request, **always create a draft first**.
After drafting, share the direct Slack channel link, then ask the user
whether they want the AI to send it or prefer to send it themselves in the Slack app.

# SQL Formatting Rules

- Use spaces around parentheses
- Use consistent indentation (4 spaces)
- If a clause is broken across lines, indent subordinate parts one additional level
- Align columns and assignments within the same clause
- Avoid vague or abbreviated column names.
- If a column name may be unclear, clarify its meaning with a comment
  (based on the definition in documentation or related code).

## Example

```
CREATE TABLE users
(
    id    INTEGER PRIMARY KEY,
    email TEXT    NOT NULL,
    ts    INTEGER NOT NULL -- created timestamp
);

UPDATE users
SET email = 'alice@example.com',
    name  = 'Alice'
WHERE id = 1
    AND active = TRUE;

INSERT INTO users (email)
VALUES ('alice@example.com')
ON CONFLICT (email)
    DO UPDATE
    SET email = excluded.email;
```

# Unit Test Comments

Use the GIVEN/WHEN/THEN format for unit test comments:

- **GIVEN**: Setup/preconditions/base data
- **WHEN**: Action/function being tested
- **THEN**: Expected result/verification

This format makes tests more readable and clearly structures the test flow.

# Markdown Writing Style

## Lists: Prefer Bullet Points by Default

Prefer bullet points over numbered lists.

Bullet points are easier to edit and reorder.
Numbered lists are harder to modify because inserting items
requires renumbering and indentation can become awkward.

Use numbered lists only when:

- You must reference a specific step later.
- Explicit numbering is required for clarity.

## Breaking Lines at Semantic Boundaries

### Goal

Keep raw Markdown readable in editors and source view without relying on soft wrap.
Assume a typical view width of about 80 to 100 characters.

### Rules

The target is the raw Markdown source, not rendered output in a browser or Markdown viewer.

Generally break lines in raw Markdown at around 80 characters.

Prefer breaking lines at semantic boundaries; it is acceptable to exceed 80 characters slightly
(as long as the length does not exceed 100 characters).
This is more readable than strictly breaking by character count.

Tables are an exception and do not require manual line breaks.

### Example

The following paragraph has **good** line breaks at semantic boundaries:

The VAPID key pair we generate proves that the push request comes from your server.
Each push request is signed with the private key,
the push service verifies the signature before delivering.

The next paragraph produces the same rendered output,
but the line breaks strictly enforce the 80-character limit,
which is less readable in raw Markdown:

The VAPID key pair we generate proves that the push request comes from your
server. Each push request is signed with the private key, the push service
verifies the signature before delivering.

Avoid writing everything on one long line:

The VAPID key pair we generate proves that the push request comes from your server. Each push request is signed with the private key, the push service verifies the signature before delivering.

# Writing Style

Avoid dashes such as - or — in the middle of sentences.
Prefer rephrasing or using colons instead.

Using a hyphen to connect common compound words is allowed.

Example:

Bad: "This is a feature - it does something"

Bad: "This is a feature — it does something"

Good: "This is a feature: it does something"

Good: "This is a feature that does something"

Allowed: "The real-time processing logic runs on the back-end server."