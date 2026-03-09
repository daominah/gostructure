---
name: test-comments
description: GIVEN/WHEN/THEN comment format for tests. Use when writing, editing, or reviewing tests.
---

# Test Comments

Use the GIVEN/WHEN/THEN comment format in tests.
Comments describe business behavior, not implementation,
so even non-technical stakeholders can understand them.

- **GIVEN** (optional): Setup or preconditions
- **WHEN**: Action being tested
- **THEN**: Expected result

```
// GIVEN the system has the hash of a user's plain password
hash, err := HashPassword("s3cret")
require.NoError(t, err)

// WHEN the user logs in with the correct password
ok := VerifyPassword(hash, "s3cret")

// THEN the system confirms the password is correct
require.True(t, ok)
```
