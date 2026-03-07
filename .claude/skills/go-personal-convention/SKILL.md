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
