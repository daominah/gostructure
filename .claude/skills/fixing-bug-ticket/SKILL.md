---
name: fixing-bug-ticket
description: End-to-end bug-ticket workflow from report through fix, PR, and status updates. Use when the user mentions a bug or wants to investigate one, whether from Slack, Linear, a ticket number (e.g. MMP-xxx), or an error log.
---

# Fixing a Bug Ticket

End-to-end workflow for handling a bug ticket:
from Slack/Linear report through root cause analysis, fix, pull request (PR), code review,
deployment to production, and verification by the reporter.

"Linear", "Slack", "GitHub", and "ArgoCD" in this workflow refer to
the project tracker, team chat, code hosting, and deployment tool respectively.
Replace with the user's available tools.

## Workflow checklist

At the start, create a checklist file in the current working directory
named `<ticket>-<short-description>-checklist.md`.
List all steps below and mark each as it completes.

## Step 1: Understand the report

- Read the Slack thread or Linear issue linked by the reporter.
- Identify the affected services, steps to reproduce.
- If the bug may span multiple repositories, check project docs for
  related repos. If unclear, ask the user.

## Step 2: Reproduce and confirm root cause

- Search for concise project documentation or agent context files (doc, memory, etc.)
  with feature overviews and diagrams. If found, load as guidance.
- Trace the code path related to the bug report.
- Suggest possible causes.
- Based on the reported symptoms, suggest what additional information
  would help confirm the root cause (e.g. metrics, dashboards, logs,
  error traces, resource usage). Ask the user to provide.
- If a database query would help investigate the issue,
  look for an available SQL skill or DDL dump file.
  If neither is found, ask the user to provide. If the user skips, move on.
- Summarize the root cause for the user before proceeding.
- If the root cause is unclear, ask the user for help or insight.

## Step 3: Plan the fix

- Propose a plan covering:
  - Root cause explanation
  - Files to change
  - Test strategy (failing test first, then fix)
  - Verification steps
- Get user approval before coding.

## Step 4: Create branch and write a failing test (red)

> **Common mistake**: Do NOT touch any file other than the test file.
> Do NOT modify the function under test or write any fix in this step.
> The goal is a red test only. Any fix belongs in Step 6.

- Create a new branch named `<ticket>-<short-description>`,
  including the ticket number for traceability.
- Write a test that calls the existing code and asserts the correct behavior.
- Run the test and confirm it fails, proving the bug exists.
- Ensure the test fails because of the bug, not because of wrong environment setup:
  - Run existing related tests to confirm they still pass.
  - No unexpected error in test output.
- Present the failing output to the **user for review**.

## Step 5: Commit and push the failing test

### STOP: wait for user before continuing

- Commit with message "add red test for <ticket>-<short-description>".
- Push the branch to the remote. Verify the CI test fails with the same error as local.
  If results differ, go back to Step 4: likely a local environment issue.

## Step 6: Apply the fix (green)

> Only begin this step after the failing test is committed and pushed in Step 5.

- Make the minimal code change that fixes the root cause.
- Run the failing test again and confirm it passes.
- Run related tests to check for regressions.

## Step 7: Document and reflect

- If the repo has a shared context directory (found in step 2)
  and the fix touches complex logic, add or update a doc there.
- When the code deviates from the common approach,
  add a comment explaining why (often a business rule or edge case).
- Consider why this bug happened and what would prevent similar ones.
  If the answer points to something beyond this fix
  (e.g. untestable code structure, bad UI/UX, misleading docs, ineffective alerting),
  create a follow-up ticket.

## Step 8: Commit the fix and open PR

- Follow the `commit-messages` skill: concise message focused on business logic,
  no AI attribution.
- Push and open a PR with a summary and a test plan checklist.

## Step 9: Self-review the PR

- Use the `reviewing-code-and-pr` skill to review the fix
- Fix any blockers or suggestions before requesting external review.

## Step 10: Update Linear and Slack

- Linear: add a comment with the PR link summarizing the fix,
  then move the issue to "In Review".
- Slack: call the message draft tool to create a reply in the bug thread
  with the PR link. Ask if the user wants you to send it.

## Step 11: Address review feedback

- Read reviewer comments and decide on each item with the user:
  whether to fix, defer, or explain why it is not actionable.
- Apply fixes, commit, push, and reply to the PR comment addressing each point.
- Ask the user if they want to request re-review on Slack.

**Steps 12-14 are user-driven. The agent guides but does not act directly.**

## Step 12: Merge and create release tag

- Merge the PR after approval.
- Create a release tag on the merged commit.

## Step 13: Deploy to development environment and verify the fix

- Deploy using ArgoCD: Update affected services to the new release tag.
- Manually verify the bug is fixed in the development environment.

## Step 14: Deploy to production

- Follow the project's production deployment process.
- Run smoke tests or sanity checks if available.
- Verify the bug is fixed in production.

## Step 15: Announce the fix

- Slack: draft a reply in the bug thread with the release version
  and request the reporter to check if the fix works as expected.
- Linear: append a resolution summary (root cause, PR link, release version, deployment status)
  to the issue description. Move the issue to "Done".
- Schedule a post-mortem if the bug was severe.
