---
name: shortening-to-concise
description: Shorten a piece of output while keeping every important point, by cutting unnecessary detail and phrasing that does not contribute. Use whenever the user signals the output is too long or padded ("shorten", "shorter", "too long", "too verbose", "trim", "cut this down", "make it concise", "wall of text", "tighten this"), and proactively before posting a review, ticket description, or Slack draft that has grown into a wall of text. With no explicit target, act on your own latest response.
---

# Shortening to Concise

## Goal

What stays is the decision or action the reader takes, plus the context it depends on.
Cut the rest: detail that changes no decision,
anything the reader already has,
and phrasing that carries nothing, or carries a little in many words.

The bar, in the user's own words: "shorten without losing meaning",
"focus on blockers and important suggestions, drop nits", "high level",
"concept level, no detail code refs", "a few sentences", "not a wall of text".
Match that register.

## Target and scope

- No target named: act on your own most recent response in this conversation.
- A file path or a quoted block named: act on that.
- A named surface ("the review", "the ticket desc", "my Slack draft"):
  act on the current draft of that surface.
- Keep applying these rules in whatever the work produces,
  not only in a target the user named separately,
  so an ask bundled with a work instruction still shapes the result
  ("be concise, and proceed to the end of the checklist without prompting me").

## What to cut

These are the recurring offenders. For each, the reason is the same:
the reader does not act on it. Cut aggressively but keep meaning.

### Cut filler phrases

Openers that acknowledge without content: "You're right", "Good point",
"Good catch", "Good instinct", "Exactly right", "Good call".
Mid-sentence lead-ins that delay the fact: "worth noting", "essentially",
"in short", "basically".
Closers that offer nothing specific: "say the word", "anything else", "happy to".
Keep the correction or answer that was wrapped in them,
e.g. "You're right, and the honest answer is that I took the cheap way out"
becomes "The honest answer: I took the cheap way out",
and "Also worth noting: the PR is no longer a draft"
becomes "The PR is no longer a draft".

### Cut editorial praise

In a review or summary, do not grade the author or praise the artifact.
"The problem source is well linked and the PR description is unusually rigorous"
tells the reader nothing they must act on.
State blockers and suggestions; skip the commentary on quality.

### Cut nits once the review already has blockers

They compete for attention with the work that must actually be done.
Keep them only when there is nothing bigger to report.
e.g. a review whose blocker is a callback leak that makes the metric unusable
does not also need "one nit: the gauge panel still excludes the newest org".

### Cut internal detail the reader will not act on

Drop function names, field names, struct names, internal counters, and code defaults
from high-level summaries and tickets
unless the reader will look at that exact symbol.
e.g. in a throughput design note, the production and documented rate limits matter;
the local code default of 5 does not.

### Cut code citations when nothing is being fixed there

A citation pins the exact spot,
so name a code location only when there is something to act on there
(a bug, a change, a decision).
This counts backticked symbol names, not just `file.go:88` line references:
threading `RowCountGuard` and `Guards` through a sentence
reads as code citing to someone who only wants the decision.

### Cut redundant restatement

Remove any sentence that only repeats a fact the reader already has from the same block.
The usual shape is the same fact re-announced with only the lead-in changed:
"Also worth stating precisely: 376,604 is passes updated;
the population that could actually receive something is the ~69k with an active target"
repeated later as
"Note 376,604 is passes updated;
the audience that could actually receive something is the ~69k with an active target",
identical numbers and all; keep one.
A fact appearing twice is not redundant by itself;
the test is whether the second occurrence adds anything.
A point in a high-level diagram expanded later by a detail section
is layering, keep both.
A design note that explains the same store-and-forward mechanic three times
at the same depth (the race bullet, the syncer bullet, again in the diagram)
is restatement, keep one.

### Cut process and local scaffolding

In output meant for a teammate (PR comment, Slack, ticket),
strip how the work was done: "round 1 / round 2", the skill used,
self-review notes, local test runs.
The reader wants the result, not the process.

### Cut reference clutter

A reference sends the reader somewhere for more detail,
so keep only the ones whose detail they actually want:
ticket numbers, links, document and dashboard names, "per the thread" pointers.
Mention a ticket once if the reader needs it;
do not thread ticket numbers and past-ticket asides through the prose.
Dropping a reference that carries no weight is right;
swapping the substance out for a reference is not:
see "Keep the substance self-contained" below.

### Tighten loose phrasing

Collapse a sentence down to the words its point actually needs:
strip the lead-up, qualifiers, and echo of the question, and say the thing directly.
Lead with the answer, then only the reasoning that changes a decision.
e.g. "To answer 'how does it filter before the drain,'
the key is that the eligibility check is the same check as today, just moved"
tightens to "The eligibility check is the same as today,
just moved from per-row on the drain into the fan-out query itself":
the reader asked the question, so echoing it back and announcing "the key is"
spends half the sentence before saying anything.
But keep an echo that carries information:
a multi-part question needs each answer labelled with the part it addresses,
and a question resting on a wrong premise needs the premise restated to correct it
("the drain does not filter; the filtering you saw happens earlier, in the fan-out").
Cut only the echo that repeats the question back unchanged,
correcting nothing and pointing at nothing.

## What to keep (do not over-trim)

Shortening fails if it drops substance.
When unsure whether a point is important,
keep it and tighten its wording, rather than guess it away.
Losing a real point is worse than leaving a slightly long line.
Protect these:

### Keep correctness and caveats

The one condition under which the answer differs, the risk that bites, the exception.
e.g. "the cap only binds above roughly 190 cases/second"
is the line that decides whether the risk is real.
Length spent here is earned.

### Keep content the reader explicitly asked for

If they asked to "summarize the PR and its blockers", "compare side by side",
"give the steps duration breakdown", or "draft a reply",
the length is the deliverable.
Tighten the phrasing, do not amputate the content.

### Keep concrete numbers and names the reader will act on

Keep the ones that drive a decision; drop the ones that are trivia.
e.g. "1250 pushed, 0 failed" is the verdict the reader came for,
where the code default of 5 above was trivia in its summary.

### Keep the substance self-contained

The reader should understand it without opening another tab.
A bare pointer is not a shortened version of the thing it points to:
"per ENG-145", "per contract §2.3", "the fix addresses blocker 2",
or an unexplained "queues 1250 of 10074 cases" each cost the reader a lookup,
which takes more of their time than the words saved.
Say the substance in words,
then attach the reference if it still earns its place,
e.g. the verdict "nothing regressed" first,
then "full table in the working doc" for the reader who wants the per-metric numbers.

Prefer the self-contained wording even when it runs a few words longer.
When you do point to a ticket, carry its title alongside the number:
a bare "ENG-145" leaves the reader asking what that is,
where "ENG-145, cap webhook retries" costs a few words and saves the lookup.
Same for jargon and acronyms: spell the term out on first use, or cut it.

## Break up what remains

A dense block of six sentences is still a wall at 600 characters,
because the reader cannot find the one line that matters.
So after cutting, look at the shape of what is left:
if it is a run of more than a few sentences carrying several distinct points,
break it into bullets,
or into a small table when the points share a structure
(before versus after, option versus trade-off, prediction versus actual).

### Give each point a labelled bullet

Paragraph breaks are not enough.
A note made of several one-point paragraphs still makes the reader read all of them
to find the one that affects them.
So give each point its own bullet with a short label,
e.g. "What we optimized", "The effect", "Follow-ups, not tracked yet".
A chain of reasoning is not an exception:
the labels carry the "because this, so that" order just as well,
and the reader can jump straight to the consequence that lands on them.

### Leave a one-line answer as a sentence

Do not add structure where a sentence would do.
A one-line answer dressed up as a bulleted list under a heading
is worse than the sentence alone:
it reads as a form to fill in rather than an answer.

## Output

- Acting on your latest response or a quoted block:
  print the shortened version directly, nothing else.
  No preamble about what you cut.
  The user is comparing it to what they just read; let it speak for itself.
- Acting on a file: edit it in place,
  then say in one line what was removed at the category level
  (for example "cut process notes and internal code citations"),
  so the user can catch an over-trim.
- Preserve the surface's required shape.
  A review keeps its verdict and section headings;
  a ticket keeps its structure.
  Shorten within that shape, do not flatten it.
- Keep applying these rules for the rest of the conversation,
  not only in the target you were asked to shorten,
  so the user does not have to ask again next turn.
