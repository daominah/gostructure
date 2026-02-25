# Automatically Output Markdown Code

If I ask to correct the grammar of something that looks like Markdown code,
output the result as Markdown code, so I can copy it.

# Markdown Writing Style

## Goal

Keep raw Markdown readable in editors and source view without relying on soft wrap.
Assume a typical width of 80 to 100 characters.

## Rules

This rule is for the raw Markdown source, not the rendered output.

Break lines at around 80 characters. Slightly exceeding 80 is fine, but cap at 100.

Prefer breaking at semantic boundaries, such as the end of a sentence
or after a logical clause, rather than strictly by character count.

Tables are an exception and do not require manual line breaks.

Avoid long single line paragraphs.

## Example

**Good** line breaks at semantic boundaries:

The VAPID key pair proves that the push request comes from your server.
Each push request is signed with the private key,
and the push service verifies the signature before delivering.

**Less ideal** strict 80 character wrapping:

The VAPID key pair proves that the push request comes from your
server. Each push request is signed with the private key; the push
service verifies the signature before delivering.

Avoid writing everything on one long line.

## Writing Style

Avoid dashes in the middle of sentences. Prefer rephrasing or using colons.

Bad: "This is a feature - it does something"  
Good: "This is a feature: it does something"  
Good: "This is a feature that does something"
