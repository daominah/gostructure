---
name: pr-description
description: Pull Request description template. Use when the PR is complex.
---

# Pull Request Description

## Basic structure

- `## Context`
  Why this PR is needed:
  the problem being solved or the business need.
  Include a ticket, conversation, or meeting link when one exists.
- `## Changes`
  What this PR changes:
  behavior and public surfaces for non-engineers,
  high-level code structure for engineers and future-self
  (new package, new function, refactor, etc.).
- `## Test plan`
  Checklist of verifications that materially apply to this PR.
  Common items: automated tests, manual verification,
  post-deploy verification (shipped version, prd behavior or metrics).
  Include only items that are highly relevant; skip the rest.

## Optional sections when relevant

- `## Out of scope`
  Items that seem needed but are intentionally not covered,
  or known follow-ups that are not blockers and can be addressed later.
- `## Related`
  Use when this PR has a cross-repo pair,
  sibling PRs in the same ticket,
  or links to related docs or specs.
- `## Risks`
  Explicit callout when changes affect critical features or customers.
- `## Rollout plan`
  Manual setup steps that CI cannot run,
  such as feature flag toggling, account provisioning, or rollback procedure.

## Example

````markdown
## Context

TICKET-456: users who forget their password must email support to reset it,
which is slow and creates support load.
Add a self-serve password-reset flow over email.

## Changes

- New `password_reset_tokens` table:
  one-time, single-use tokens with expiry.
- Endpoint to request a reset (`POST /auth/password-reset/request`):
  takes an email and sends a reset link.
  Returns the same response for known and unknown addresses
  so attackers cannot enumerate registered emails.
  Rate-limited per source address.
- Endpoint to confirm a reset (`POST /auth/password-reset/confirm`):
  swaps a valid token for a new password.
  Rejects expired, already-used, or weak-password attempts.
- Token lifetime is 1 hour, configurable.

## Test plan

- [x] Automated tests cover the happy path, expired token, reused token,
  unknown email, and weak password.
- [x] Manual on dev: requested a reset, received the email,
  clicked the link, set a new password, signed in.
- [ ] Demo to Mr. Stakeholder; gather feedback.

## Related

- Frontend PR: github.com/org/web-app/pull/123.
- Plan doc: `doc/2026-05-01-password-reset-bdd.md`.
````
