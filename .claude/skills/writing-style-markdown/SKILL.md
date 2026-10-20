---
name: writing-style-markdown
description: Markdown writing style conventions. Use when writing or editing Markdown files or variants (e.g. *.md, *.mdc).
---

# Markdown Writing Style

## Lists: Use Bullet Points by Default

Prefer bullet points over numbered lists (easier to edit and reorder).

Use numbered lists only when:

- You must reference a specific step later.
- Explicit numbering is required for clarity.

### No Dense Paragraphs

When a text holds several points, write them as a list, not one dense text wall.
Small separate points are easier to take in.

**Avoid:**

```
The export works for CSV and JSON, the file size limit is 50 MB, and the export
link expires after 7 days, which support should mention to customers.
```

**Prefer:**

```
- The export works for CSV and JSON.
- The file size limit is 50 MB.
- The export link expires after 7 days: support should mention it to customers.
```

## Bold: Key Phrases for Skimming

In a list of points (findings, review items, results),
bold the phrase that carries each point,
so a reader who only skims the bold text still gets the message.
Bold a phrase, not a whole sentence.

```
- **The export link expires after 7 days**, so old links in emails stop working.
- **Large files fail silently** above 50 MB: no error is shown.
```

## Quotes: No Blockquote Syntax

Do not use `> ` blockquotes: they clutter raw Markdown.

Quote a short text inline with double quotes:
`Alice, our CTO: "we should cache the results for one hour."`

For a longer quote, write one lead-in line naming the source and saying it is verbatim,
then copy the text without quotation marks.
Make the end obvious: the list ends, or the next heading starts.

```
Feature request from Alice, our CTO, 2026-01-15, copied verbatim:

- Users can export their data as CSV.
- The export finishes within one minute for 10,000 rows.
```

## Breaking Lines at Semantic Boundaries

### Goal

Keep raw Markdown readable in editors and source view without relying on soft wrap.
Assume a typical view width of about 80 to 100 characters.

### Rules

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

### Example

The following paragraph has **good** line breaks at semantic boundaries:

```
The VAPID key pair we generate proves that the push request comes from your server.
Each push request is signed with the private key,
the push service verifies the signature before delivering.
```

The next paragraph produces the same rendered output,
but the line breaks strictly enforce the 80-character limit,
which is **less readable** in raw Markdown:

```
The VAPID key pair we generate proves that the push request comes from your
server. Each push request is signed with the private key, the push service
verifies the signature before delivering.
```

**Avoid** writing everything on one long line:

```
The VAPID key pair we generate proves that the push request comes from your server. Each push request is signed with the private key, the push service verifies the signature before delivering.
```

## Diagrams: Use Mermaid by Default

Always use Mermaid syntax for diagrams.

Prefer sequence diagrams when they fit the purpose instead of other diagram types.

Put a diagram in a Markdown file, never in a chat reply:
a terminal does not render Mermaid, so the reader only sees the source.
In chat, use a list or a table instead, and point to the file that holds the diagram.

Example:

```mermaid
sequenceDiagram
    Client ->> Server: Request
    Server -->> Client: Response
```

### Before vs After: Side by Side with Subgraphs

When comparing two states (before vs after a fix, current vs proposed design),
prefer one flowchart with a `subgraph` per state, side by side:

```mermaid
flowchart LR
    subgraph OLD["Before, manual deploy"]
        direction TB
        B1["push code"] --> B2["operator runs deploy script"]
        B2 --> B3["service updated"]
    end
    subgraph NEW["After, auto deploy"]
        direction TB
        A1["push code"] --> A2["pipeline builds and deploys"]
        A2 --> A3["service updated"]
    end
    OLD ~~~ NEW
```

This forgoes the sequence diagram (there is no side-by-side equivalent for it),
trading the explicit time axis for the at-a-glance comparison.

### Avoid Common Syntax Errors

In `sequenceDiagram` Note text and message labels, avoid `;`, `:`, `#`, and `|`.
These are parser tokens and cause parse errors mid-text.
Use `.` or `,` instead, or rephrase to drop the character.

Also avoid bare `<` and `>` in note and message text;
the parser reads them as the start of an HTML tag.
This includes placeholders like `<id>` or `<src>`,
and comparison operators like `<=` or `>`.
For placeholders, use curly braces: `{id}`, `{src}`.
For comparisons, use Unicode operators directly: `≤`, `≥`, `≠`.
For strict `<` or `>`, spell out as "greater than" or "less than".

Use `<br>` instead of `<br/>` inside notes; some renderers reject the self-closing form.

In `flowchart` node labels, double-quote any label containing punctuation:

```mermaid
flowchart TD
    A["text with: colons; semicolons"] --> B["another label"]
```
