---
name: code-and-pr-review
description: Review code change and pull request (PR) for correctness, impact, and safety.
  Use when implementing a feature, fixing a bug, reviewing a PR,
  or reviewing code changes before committing.
---

# Code Changes and Pull Request Review Checklist

## Code Meets Business Need

The business intent comes from a ticket (Linear/Jira), a Slack message, or a spec/plan.
The PR must link to these sources so the reviewer can verify:

**Is the business intent clear?**

- Is each source clear and internally consistent
  (e.g. ticket title, description, and acceptance criteria match)?
- Are the sources consistent with each other (ticket, Slack message, spec/plan)?
- What is the user experiencing vs what should they experience?
- Who is affected and how urgently?
- For bugs: can we reproduce it? Is it a symptom of a deeper issue?
- If anything is vague or contradictory, clarify with the requester first.

**Technical clarity:**

- What is the root cause or the right solution approach?
- What is the fix/change scope? Are there side effects?
- If a plan or spec exists, does it match the business request? Flag gaps first.

Avoid the anti-pattern: code first, discover unclear requirements in review, then major rework.

## Building It the Right Way

- A pull request (PR) should be small so it can be reviewed quickly and merged safely.
- Confirm existing callers and dependent code still work:
  do not silently change behavior that other code relies on.
- Improve the codebase where you touch it,
  but keep improvements in separate commits from feature work.

## Code Works as Expected

- Every new or modified function must have a test covering its primary behavior.
- Tests follow the GIVEN/WHEN/THEN comment format (see `test-comments` skill).
- One behavior per test case.
  No dead test code, unused helpers, or copy-pasted blocks.

## End-User Verifiability

- How can the end user confirm this change works in production or staging?
- If there is no observable output (UI, API response, log line, metric), add one.
- Prefer something the user can trigger and check without reading code.

## Logging and Monitoring for Long-Running Features

- Background jobs, queues, workers, and scheduled tasks must log:
  - Start and end of each run
  - Key counts (items processed, errors, skipped)
  - Any unexpected states or retries
- Expose metrics or a status endpoint if the feature runs continuously.
- Do not silently swallow errors. Log them with enough context to debug.
