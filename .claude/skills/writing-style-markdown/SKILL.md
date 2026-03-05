---
name: writing-style-markdown
description: Markdown writing style conventions. Use when writing or editing Markdown files or variants (e.g. .mdc).
---

# Markdown Writing Style

## Lists: Prefer Bullet Points by Default

Prefer bullet points over numbered lists.

Bullet points are easier to edit and reorder.

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

```
The VAPID key pair we generate proves that the push request comes from your server.
Each push request is signed with the private key,
the push service verifies the signature before delivering.
```

The next paragraph produces the same rendered output,
but the line breaks strictly enforce the 80-character limit,
which is less readable in raw Markdown:

```
The VAPID key pair we generate proves that the push request comes from your
server. Each push request is signed with the private key, the push service
verifies the signature before delivering.
```

Avoid writing everything on one long line:

```
The VAPID key pair we generate proves that the push request comes from your server. Each push request is signed with the private key, the push service verifies the signature before delivering.
```
