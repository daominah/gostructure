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

# Writing Style

Avoid dashes in the middle of sentences. Prefer rephrasing or using colons instead.

Bad: "This is a feature - it does something"
Good: "This is a feature: it does something"
Good: "This is a feature that does something"

# Markdown Writing Style

I prefer the Markdown can be read without rendering too,
my editor usually can show a line with 80 characters (max 100 characters)
so try to break the line (in raw Markdown, does matter in rendered Markdown)
at around 80 characters.
Breaking line when a sentence ends or a comma that end a part of meaning
is better than just break by character count.

Table can be an exception, don't need to add line break for raw Markdown.

This markdown file is also a good example of how to write markdown in this style.
The previous lines can be written in a single line,
but I break them into multiple lines to make it easier to read and edit without rendering.
