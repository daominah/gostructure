---
name: slack-messaging
description: Reads, scans, and drafts Slack messages. Use when the user asks to send, draft, check, or scan Slack, including implicit reads like "what am I working on" or "who is waiting on me".
---

# Slack

This skill covers two directions: writing to Slack, and reading from Slack.

## Prerequisites

All Slack read and write operations go through the Slack MCP server.
If the MCP is not installed, returns auth or permission errors, or is
temporarily unavailable, **stop and prompt the user** to set it up or reconnect.

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
  **Critical and easy to miss**:
  a "DM recipient" filter does not match mentions in channels,
  so a from + to scan alone leaves these invisible.
  A separate query that matches mentions regardless of channel type is required.
- Activity the user has engaged with: thread replies and emoji reactions.
  Higher chance of needing follow-up than untouched messages.
  A thread reply usually means a conversation is in progress;
  an emoji can mean "I am taking a look" or a soft self-flag to revisit later.

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

Slack search returns **at most 20 results per call** (a hard MCP cap).
A response of exactly 20 means the result is truncated.
Pagination is **non-negotiable**:
every signal that hits the cap must be either paginated to end-of-results
or narrowed (by channel, date, or `-from:` filter) until it returns under the cap.
Writing "I did not paginate" in the summary is **not** a substitute.
That shifts the cost onto the user,
who cannot tell whether the missed window contained a real ping.

The whole reason this skill exists is the failure mode
where a single `@`-mention sitting near the cap edge gets missed.
Treat any truncation as a real gap until proven otherwise,
even when the first batch looks comprehensive.

For deep-dive into a single thread, switch from search to the thread-read tool,
which returns the full thread content with a much higher per-call limit.

### Output format

After gathering all signals, present findings grouped by urgency:

- **Open asks**: someone is waiting on the user (direct question, unacknowledged request).
- **Follow-ups**: user has an open promise or unresolved thread to revisit.
- **FYI**: low-priority pings, reactions, passive mentions with no action needed.

Omit empty groups. Within each group, list items newest-first.
