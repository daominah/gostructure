---
name: slack-messaging
description: Reads, scans, and drafts Slack messages. Use when the user asks to send, draft, check, or scan Slack, including implicit reads like "what am I working on" or "who is waiting on me".
---

# Slack

This skill covers two directions: writing to Slack, and reading from Slack.

## Prerequisites

All Slack read and write operations go through the Slack MCP.
If the Slack MCP is not installed, returns authentication or permission errors,
or is temporarily unavailable, **stop and prompt the user** to set it up or reconnect.

**User ID identification.**
Mention scans and `from:` / `to:` filters all depend on the user's Slack user ID
(format `U01AB2CDEF3`). Before any scan, confirm the ID is known:

- Check the Slack MCP search-tool descriptions:
  they embed the line "Current logged in user's user_id is U01AB2CDEF3"
  (with the real ID in place of the placeholder shown).
- If still unknown, **stop and ask the user** to copy their ID from Slack:
  `Profile` > `⋮` (near `View as`) > `Copy member ID`.

Never guess the user ID.
A wrong ID returns silent empty results indistinguishable from "no mentions".

**Slack MCP capability gap.**
The Slack MCP has **no Threads / Activity / Mentions panel reader**;
scans reconstruct that native sidebar view through search queries, which is lossy.

## Sending

For any Slack send/reply/post request, **always create a draft first**
(using the Slack draft message tool, so the user sees the draft in their Slack app).

After drafting, share the direct Slack channel clickable link,
then ask the user whether they want the AI to send it or will send it themselves.

## Reading and scanning

For any "what am I working on", "who is waiting on me", "any update from X",
"scan my Slack", "catch me up", or similar Slack-data question,
scan **each signal below in parallel** as its own search query.
The exact filter syntax is for the agent to construct.

Time range: infer from the query type.

- Recency scan ("catch me up", "what am I working on", "scan my Slack"):
  default to the last 7 days.
- Specific lookup ("any update from X", "that thread about Y",
  "what did I promise to Z"): no time filter; let Slack rank by relevance.

Signals to scan:

- Messages the user sent.
  Establishes what the user has been doing and what promises or follow-ups are open.
- DMs the user received. Often carry direct asks and blockers.
- Channel `@`-mentions of the user.
  Pings from teammates or external contacts in non-DM channels.
  **Critical and easy to miss**: see "Mention search syntax" below
  for the exact query forms.
  Primary form is `<@U01AB2CDEF3>` (matches the rendered tag substring).
  `to:me` never surfaces channel mentions (matches DM recipients only).
- Activity the user has engaged with:
  - **Thread replies** are surfaced by the `from:<@U01AB2CDEF3>` query
    (Slack search returns both top-level posts and thread replies).
    A thread reply usually means a conversation is in progress.
  - **Emoji reactions** are **not** queryable in bulk:
    Slack exposes only `hasmy::emoji:` (per-emoji),
    with no "any reaction by me" form.
    Enumerate the user's common reactions as parallel queries,
    ordered by usage frequency
    (so an early stop under budget still covers the bulk):
    `:eyes:`, `:white_check_mark:`, `:blobthanks:`, `:ok_hand:`, `:+1:`, `:raised_hands:`.
    `:+1:` and `:thumbsup:` are aliases (same results); pick one.
    A reaction often means "I am taking a look" or a soft self-flag to revisit later.

### Time filter syntax

Slack exposes two time filters with **different inclusivity semantics**.
Choose deliberately, especially for "yesterday" / "last 24h" queries:

- **MCP-level `after` parameter** (Unix timestamp): **inclusive**.
  Supports hour-level precision; matches the requested instant onward.
  **Preferred** for any window that hinges on a specific day or hour boundary.
- **Query-modifier `after:YYYY-MM-DD`**: **exclusive** of the named date.
  `after:2026-05-21` means "from 2026-05-22 onward",
  so messages sent on May 21 itself are silently dropped.
  To include a date, pass `after:DATE_MINUS_ONE`, or use `on:DATE`.

Failure mode this prevents: a "last 24h" scan with `after:<yesterday>`
returns 0 results, the agent reports "nothing for you",
and the user's actual yesterday-replies are missed.

### Mention search syntax

Slack renders `@`-mentions in the message body as `<@U01AB2CDEF3|Display Name>`.
The whole rendered string is searchable as substring content,
which is what mention scans rely on.

Run these as parallel queries, then dedupe by `message_ts`:

- **Primary: `<@U01AB2CDEF3>`** (the rendered tag substring).
  Highest precision: returns only true tagged `@`-mentions, no plain-text noise.
- **Supplementary: `"Display Name"`** (e.g. `"Tung Dao"`).
  Matches the rendered tag and also plain-text references to the full name
  (e.g. bot reports listing "Tung Dao: reviewed 3 PRs today").
  Use to catch references where the writer typed the name without tagging.
- **Optional: bare first name** (e.g. `Tung`).
  Catches informal references where the writer did not tag and did not type
  the full name. Noisiest; filter false positives manually.
  Skip unless the workspace has a culture of dropping `@`-tags.

Avoid these forms:

- `@Name` as a bare keyword: behavior is inconsistent,
  mixes channel mentions with body-text noise.
- `to:me`: matches DM recipients only, never channel `@`-mentions in shared
  channels. Returns plenty of DM results that masquerade as "found something".

The raw user ID is also used for programmatic identification:
author-field matching in API responses,
and constructing `from:` / `to:` filters
(e.g. `from:<@U01AB2CDEF3>` to filter by author).

### Treat zero results as suspect

A `0 results` response on a mention scan is **as suspicious as a 20-result cap**.
Common causes of false-empty: wrong syntax form (e.g. `to:me`),
off-by-one date filter (see "Time filter syntax"),
or a DM-only channel-type scope.
An empty result usually means a query issue, not absence of mentions.

Before concluding "no pings exist":

- Retry with at least one alternate syntax form from the section above.
- If still zero, state in the output that the scan was empty,
  and that the reconstruction is lossy because the Slack MCP has no
  Threads / Activity panel reader,
  so the user can sanity-check against their native sidebar.

Never report "nothing for you" with full confidence after a single query.

### Filter automation noise

Slack search defaults to `include_bots=false`, but plenty of automation posts
(Google Calendar invites, GitHub Slack-app pings, Slack `Reminder`, etc.)
come from accounts that are not flagged as bots,
so they still surface and crowd the 20-result cap.
They are not actionable work.

If automation pings inflate a result set,
exclude the noisy account with a `-from:` filter (e.g. `-from:<@calendar-account>`)
and re-issue the query, so each 20-result batch is actual signal instead of noise.
Pagination (below) then applies to the cleaner stream as normal.

### Pagination

Slack search returns **at most 20 results per call** (hard Slack MCP cap).
A response of exactly 20 means the result is truncated.
Keep fetching via the cursor in `pagination_info` until one of:

- The response returns under 20 items,
  or `pagination_info` reports no further pages.
- The hard ceiling fires: **16 pages per query** (~320 results).
  Report the partial result and recommend a narrower follow-up.

If a single query keeps hitting the cap, narrow by channel, date,
or `-from:` filter and re-issue. The narrower stream ends naturally.

For deep-dive into a single thread, switch from search to the thread-read tool.

### Auto-expand thread context

A scanned message is only useful if both:

- what the thread is about, and
- what the user committed to, owes, or is waiting on,

are clear from the message text alone.

If either is unclear (short replies like "ok" / "I can" / emoji-only;
longer messages that reference unseen context like "I left 4 blockers";
pasted code or JSON answers with no surrounding question),
fetch the thread parent with `slack_read_thread`
and present parent + reply together
(e.g. "Tung committed to help Asker close out the X request").
Do not surface a hanging fragment to the user.

### Resolve asks against current state

If a signal contains a link to an actionable artifact
(PR, ticket, design doc), check its current state with whatever tool is
available before treating it as an open ask.
Drop or downgrade the ask if the user has already done what was requested,
or if the artifact is closed.

### Output format

After gathering all signals, present findings grouped by urgency:

- **Need to reply**: someone is waiting on a response from the user (direct question, unacknowledged request).
- **Need to schedule**: open commitment the user owes (work to do, thread to revisit).
- **Wait for their reply**: user's last message is an outgoing ask with no reply yet.
- **FYI**: low-priority pings, reactions, passive mentions with no action needed.

Omit empty groups. Within each group, list items newest-first.
