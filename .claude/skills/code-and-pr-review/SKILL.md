---
name: code-and-pr-review
description: Review code changes and PRs for correctness, impact, and safety. Use when implementing a feature, fixing a bug, or reviewing code changes before committing or creating a pull request.
---

# Code and PR Review Checklist

Before finishing a code change, verify each point in order of priority:

## 1. Code Meets Business Need

The business intent comes from a ticket (Jira/Linear), a Slack message, or a spec/plan. Before writing any code, the reviewer (or author) should check:

**Is the business intent clear?**
- Is the ticket description consistent — does the title, description, and acceptance criteria all say the same thing?
- What is the user experiencing vs what should they experience?
- Who is affected and how urgently?
- For bugs: can we reproduce it? Is it a symptom of a deeper issue?
- If anything is vague or contradictory, clarify with the requester before proceeding.

**Technical clarity:**
- What is the root cause or the right solution approach?
- What is the fix/change scope? Are there side effects?
- If a plan or spec exists, confirm it matches the original business request — flag gaps before proceeding.

Avoid the anti-pattern: code first, discover unclear requirements in review, then major rework.

## 2. Building It the Right Way

- PRs should be small so they can be reviewed quickly and merged safely.
- Identify functions/methods that were added or changed.
- Confirm existing callers and dependent code still work — do not remove or silently change behavior that other code relies on.
- Improve the codebase where you touch it, but keep improvements in separate commits from feature work.

## 3. Code Works as Expected

- Every new or modified function must have at least one test covering its primary behavior.
- Tests follow the GIVEN/WHEN/THEN comment format (see `test-comments` skill).
- Tests must have a clear, single purpose — one behavior per test case. No dead test code, unused helpers, or copy-pasted test blocks.

## 4. End-User Verifiability

- Ask: how can the end user confirm this change works in production or staging?
- If there is no observable output (UI, API response, log line, metric), add one.
- Prefer something the user can trigger and check themselves without reading code.

## 5. Logging and Monitoring for Long-Running Features

- Background jobs, queues, workers, and scheduled tasks must log:
  - Start and end of each run
  - Key counts (items processed, errors, skipped)
  - Any unexpected states or retries
- Expose metrics or a status endpoint if the feature runs continuously.
- Do not silently swallow errors — at minimum log them with enough context to debug.
