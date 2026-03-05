---
name: test-comments
description: GIVEN/WHEN/THEN comment format for unit tests. Use when writing, editing, or reviewing unit tests.
---

# Unit Test Comments

Use the GIVEN/WHEN/THEN comment format in unit tests
so a reviewer can understand what the test does by reading only the comments.

- **GIVEN** (optional): Setup/preconditions/base data
- **WHEN**: Action/function being tested
- **THEN**: Expected result/verification

```
// WHEN hashing the plain password
hash, err := HashPassword(password)
// THEN the hash matches the original password
ok := VerifyPassword(hash, password)
```
