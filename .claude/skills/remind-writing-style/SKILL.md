---
name: remind-writing-style
description: Cleanup pass that rewrites recently edited docs, Markdown, and code comments to follow the user's personal writing-style rules.
disable-model-invocation: true
---

# Remind Writing Style

The writing rules already exist, scattered across `CLAUDE.md` and several skills.
Agents forget them for no particular reason:
while coding, while writing a doc that was the whole task,
or while dropping a comment into a config or shell script.
So this skill is a deliberate second pass:
after the work is done, re-read what was just written and make it conform.
It does not invent new rules. It mirrors the existing ones in one place
so the fix does not require opening five other files.

The rule blocks below are copied verbatim from their source.
Each block cites that source, which stays authoritative if the two ever diverge.

The user triggers this on purpose, usually after glancing at the output
and suspecting the style slipped. Bias toward acting:
find the violations, fix them in place, then report what changed.

## Scope

Check every file in scope:

- By default, what the agent added or edited in the current session:
  - Markdown and documentation files, including design, plan,
    architecture-decision, spec, findings, and readme docs.
  - Comments in any touched file: source code, but also config and scripts
    like `.env`, `.sh`, YAML, Dockerfile, SQL, and HTML comments.
- If the user names specific files or directories, check those instead.

Only inspect the writing itself.
Do not touch code logic, identifiers, or test assertions.
Skip generated and vendored files and prose the user wrote by hand.

## How to run

1. List the files in scope.
2. For each file, apply the rule sections that match its type,
   and fix the violations in place.
3. Summarize per file what changed, one line for files already clean
   so the user knows they were checked.

The failures that recur most, worth extra attention:
semantic-boundary line breaks forgotten in code comments, in any language
(mine are mostly Go, Python, and JavaScript).

## Rules for every file

Verbatim from `CLAUDE.md` "Writing Style":

- Avoid dashes (`-` or `—`) in the middle of sentences;
  rephrase or use colons instead.
  Compound words are allowed: "real-time", "back-end".
- Use standard straight quotes (`'` and `"`) instead of curly quotes.
- When the user asks to correct grammar (e.g. "grammar?", "smooth?"),
  apply only the minimal change without rephrasing the rest of the sentence.
- Use bold only to insist on a specific approach over a common alternative
  or to warn about pitfalls the reader might skip past.
- Never introduce abbreviations (unless the user used that abbreviation first)
  on any writing surface (including docs, commits, PRs, conversations, etc.).
  Full words help the reader skip the mental step of mapping them to actual terms.

Verbatim from `CLAUDE.md` "Naming":

When naming variables, sections, or concepts:
prefer short, code-style terms over verbose descriptions,
but use full words instead of abbreviations.
Ask for confirmation before choosing names if the context is ambiguous.

## Rules for comments (code, config, scripts)

Everything in "every file", plus this verbatim from `CLAUDE.md` "Code Comments":

Code comments should explain intent and non-obvious behavior.
Avoid generating comments that just restate the function or variable name.

Break comment lines at semantic boundaries,
following skill `writing-style-markdown` section
"Breaking Lines at Semantic Boundaries" (apply the same rule to comment text instead of markdown).

## Rules for test comments

Everything in "every file" and "comments", plus the following verbatim from skill `test-comments`.

Use the GIVEN/WHEN/THEN comment format in tests.
Comments describe business behavior, not implementation,
so even non-technical stakeholders can understand them.

- **GIVEN** (optional): Setup or preconditions.
- **WHEN**: Action being tested.
- **THEN**: Expected result.

```
// GIVEN the system has the hash of a user's plain password
hash, err := HashPassword("s3cret")
require.NoError(t, err)

// WHEN the user logs in with the correct password
ok := VerifyPassword(hash, "s3cret")

// THEN the system confirms the password is correct
require.True(t, ok)
```

## Rules for Markdown and documentation files

Everything in "every file", plus the following verbatim from skill `writing-style-markdown`.

**Lists: Use Bullet Points by Default**

Prefer bullet points over numbered lists (easier to edit and reorder).

Use numbered lists only when:

- You must reference a specific step later.
- Explicit numbering is required for clarity.

**Breaking Lines at Semantic Boundaries**

Goal: keep raw Markdown readable in editors and source view without relying on
soft wrap. Assume a typical view width of about 80 to 100 characters.

The target is the raw Markdown source, not rendered output in a browser or Markdown viewer.

Generally break lines in raw Markdown at around 80 characters.

Prefer breaking at semantic boundaries to strictly breaking by character count.
Lines may exceed 80 characters but must not exceed 100.

Do not split a short sentence or separate a parenthetical from its phrase
just to stay under 80 characters. Keep the semantic unit on one line.

Exceptions:

- Markdown table.
- Code block.
- Agent Skill frontmatter.

The following paragraph has **good** line breaks at semantic boundaries:

```
The VAPID key pair we generate proves that the push request comes from your server.
Each push request is signed with the private key,
the push service verifies the signature before delivering.
```

**Avoid** writing everything on one long line:

```
The VAPID key pair we generate proves that the push request comes from your server. Each push request is signed with the private key, the push service verifies the signature before delivering.
```

**Diagrams: Use Mermaid by Default**

Always use Mermaid syntax for diagrams.
Prefer sequence diagrams when they fit the purpose instead of other diagram types.
In `sequenceDiagram` Note text and message labels, avoid `;`, `:`, `#`, and `|`.
Also avoid bare `<` and `>` in note and message text.
For placeholders, use curly braces: `{id}`, `{src}`.
For comparisons, use Unicode operators directly: `≤`, `≥`, `≠`.
For strict `<` or `>`, spell out as "greater than" or "less than".
Use `<br>` instead of `<br/>` inside notes.
