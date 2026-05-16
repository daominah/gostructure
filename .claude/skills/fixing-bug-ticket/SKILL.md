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

## Working doc

At the start, create `<ticket>-<short-description>.md` in the current working directory.
This file captures the report, root cause, plan, and checklist throughout the workflow.
Structure it as:

1. **Report** (Step 1): affected services, steps to reproduce, scope
2. **Root cause** (Step 2): findings from reproduction and code trace
3. **Plan** (Step 3): files to change, test strategy, verification steps
4. **Checklist**: list all steps below; mark each complete at the end of every step.

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
- Persist the plan in the working doc.
- Get user approval before proceeding.

## Step 4: Create branch and open draft PR with working doc

The PR is the container all subsequent commits land into.
Opening it now (before any code) lets teammates review the plan and
gives the user a single URL to track from any machine.

- Create a new branch named `<ticket>-<short-description>`,
  including the ticket number for traceability.
- Commit the working doc as the first commit.
- Push the branch.
- Open a **draft PR** with the plan summarized in the description
  (and the working doc linked or quoted) plus a test plan checklist.
- Linear: add a comment with the draft PR link.
- Slack: share the draft PR link in the bug thread.

## Step 5: Write a failing test (red)

> **Common mistake**: Do NOT touch any file other than the test file.
> Do NOT modify the function under test or write any fix in this step.
> The goal is a red test only. Any fix belongs in Step 7.

- Write a test that calls the existing code and asserts the correct behavior.
- Run the test and confirm it fails, proving the bug exists.
- Ensure the test fails because of the bug, not because of wrong environment setup:
  - Run existing related tests to confirm they still pass.
  - No unexpected error in test output.
- Present the failing output to the **user for review**.

## Step 6: Commit and push the failing test

### STOP: wait for user before continuing

- Commit with message "add red test for <ticket>-<short-description>".
- Push the branch to the remote. Verify the CI test fails with the same error as local.
  If results differ, go back to Step 5: likely a local environment issue.

## Step 7: Apply the fix (green)

> Only begin this step after the failing test is committed and pushed in Step 6.

- Make the minimal code change that fixes the root cause.
- Run the failing test again and confirm it passes.
- Run related tests to check for regressions.

## Step 8: Document and reflect

- If the repo has a shared context directory (found in step 2)
  and the fix touches complex logic, add or update a doc there.
- When the code deviates from the common approach,
  add a comment explaining why (often a business rule or edge case).
- Consider why this bug happened and what would prevent similar ones.
  If the answer points to something beyond this fix
  (e.g. untestable code structure, bad UI/UX, misleading docs, ineffective alerting),
  create a follow-up ticket.

## Step 9: Commit the fix and mark PR ready for review

- Follow the `commit-messages` skill: concise message focused on business logic,
  no AI attribution.
- Push the fix commit.
- Mark the draft PR as ready for review.
  Update the PR description with the final summary and test plan checklist.

## Step 10: Self-review the PR

- Use the `reviewing-code-and-pr` skill to review the fix
- Fix any blockers or suggestions before requesting external review.

## Step 11: Update Linear and Slack

- Linear: add a comment summarizing the fix
  (the PR link is already in the thread from Step 4),
  then move the issue to "In Review".
- Slack: call the message draft tool to create a reply in the bug thread
  noting the PR is ready for review. Ask if the user wants you to send it.

## Step 12: Address review feedback

- Read reviewer comments and decide on each item with the user:
  whether to fix, defer, or explain why it is not actionable.
- Apply fixes, commit, push, and reply to the PR comment addressing each point.
- Ask the user if they want to request re-review on Slack.

**Steps 13-15 are user-driven. The agent guides but does not act directly.**

## Step 13: Merge and create release tag

- Merge the PR after approval.
- Create a release tag on the merged commit.

## Step 14: Deploy to development environment and verify the fix

- Deploy using ArgoCD: Update affected services to the new release tag.
- Manually verify the bug is fixed in the development environment.

## Step 15: Deploy to production

- Follow the project's production deployment process.
- Run smoke tests or sanity checks if available.
- Verify the bug is fixed in production.

## Step 16: Announce the fix

- Slack: draft a reply in the bug thread with the release version
  and request the reporter to check if the fix works as expected.
- Linear: append a resolution summary (root cause, PR link, release version, deployment status)
  to the issue description. Move the issue to "Done".
- Schedule a post-mortem if the bug was severe.
