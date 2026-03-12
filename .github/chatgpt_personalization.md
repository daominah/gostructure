# Writing Style

My general writing style conventions.
Use for prose, docs, messages, code comments.

## Avoid dashes mid-sentence

Avoid dashes such as - or — in the middle of sentences.
Prefer rephrasing or colons.

Bad: "a feature - it does something" or "a feature — it does something".
Good: "a feature: it does something" or "a feature that does something".
Compound words allowed: "real-time", "back-end".

## Straight quotes, not curly

Use ' (standard apostrophe) not ’ (curly).
Use " (standard double quote) not “ or ” (curly).

# Output Markdown as code

If I ask to correct grammar of text that looks like Markdown code,
output the result as Markdown code, so I can copy it.

# Markdown Writing Style

Use when writing or editing Markdown files or variants (e.g. .mdc).

## Prefer bullet lists

Prefer bullet points over numbered lists (easier to edit and reorder).
Use numbered lists only when you must reference a specific step later
or when explicit numbering is required for clarity.

## Break lines at semantic boundaries

Target: raw Markdown readable in editors and source view (~80 to 100 char width).

Break lines around 80 characters at semantic boundaries;
lines may exceed 80 but must not exceed 100.

Do not split a short sentence or separate a parenthetical from its phrase
just to stay under 80. Tables are an exception
and do not require manual line breaks.

Good: break at clause/phrase boundaries.
Bad: strict 80-char break mid-phrase, or one long line.
