---
name: go-personal-convention
description: Personal Go conventions. Use when writing or reviewing Go code.
---

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

## Bool Naming

Prefix bool variables and fields with `Is` or `is`.

```
var IsActive  bool  // Exported field or variable
type Something struct {
    isDeleted bool  // Unexported field or variable
}
```

## Enum-like Fields

In Go, define a named `string` type with constants for
fields that hold a value from a fixed set.

In the database, store these fields as `TEXT` rather than a database enum type
(adding an enum value requires a schema migration, etc.).
Enforce valid values in application code only.

Constant names should not include the type prefix
unless there are duplicate names in the same package.

Prefer human-readable ALL_UPPERCASE string values instead of numeric codes.

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

## JSON Struct Tags

The default Go field name (PascalCase) is fine.
Only add json camelCase tags for external API contracts.

```
// Internal: no json tag needed
type Config struct {
    IsEnabled bool
}

// External API: json tags required
type APIResponse struct {
    IsEnabled bool `json:"isEnabled"`
}
```

## File Structure for Executables

In a one-off Go script (`package main`),
place adjustable config at the top so a reader can find and tweak it immediately,
then `func main()` so the business flow is visible just below,
and move internal state to the bottom where it doesn't push the interesting parts down.

Suggested top-to-bottom order:

1. Package and imports.
2. The script's config. Use a `const (...)` block, plus a `var (...)` block
   next to it for values Go can't declare as `const` (maps, slices, structs).
   Examples: API keys, target IDs, URLs, limits, sizes, feature flags,
   small lookup maps you might edit before a run.
   Open the block with a one-line header comment, e.g.
   "// Inputs (edit for each run):" or
   "// Adjustable knobs for X (edit before running):".
   Add an inline or preceding comment for any value whose meaning is non-obvious.
   Prefer `const`/`var` over the `flag` package: it's convenient to
   edit and re-run.
3. `func main()`: the business flow.
4. Helpers used by `main` in call order (pipeline funcs, setup/teardown).
5. Debug and profiling globals (e.g. `flag.String("cpuprofile", ...)`).
   Each global gets a doc comment explaining what it is and why.
6. Internal data globals: lookup tables, caches,
   and the helpers that mutate them.
   Each global gets a doc comment explaining what it is and why.
7. Type declarations (structs, named types).

Note: long-running services don't fit this layout. They load config from
environment variables instead of a `const` block.
