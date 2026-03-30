---
name: adding-feature-ticket
description: End-to-end workflow for adding a new feature, from ticket through design, implementation, PR, and deployment. Use when the user asks to implement, add, or build a feature from Linear or Slack.
---

# Implementing a Feature Ticket

End-to-end workflow for handling a feature ticket:
from Linear/Slack requirement through design, implementation, pull request (PR),
code review, deployment to production, and announcement to stakeholders.

**Every step applies regardless of change size.** A small change still needs
context gathering, a failing test, a STOP for review, then implementation.
Do not skip or compress steps. For features that modify existing behavior,
ensure Step 5 tests also cover the existing behavior as a regression baseline.

"Linear", "Slack", "GitHub", and "ArgoCD" in this workflow refer to
the project tracker, team chat, code hosting, and deployment tool respectively.
Replace with the user's available tools.

## Working doc

At the start, create `<ticket>-<short-description>.md` in the current working directory.
This file captures context, clarifications, and design throughout the workflow.
Structure it as:

1. **Context** (Step 1): business need, approach from ticket
2. **Clarifications** (Step 2): findings from code, answers from team
3. **High-level design** (Step 3): components, connections, decisions, edge cases
4. **Checklist**: list all steps and mark each as it completes

## Step 1: Understand the requirements

- Read the Linear issue, Slack thread, or spec linked by the requester.
- **Search beyond the ticket to understand what the client actually needs.**
  Don't only read what's linked. Search Slack for the ticket ID, project name,
  and customer name. Check for a dedicated deal/project channel. Read recent threads.
- **Cross-check ticket vs. conversations.** Compare the ticket scope against
  what's actually discussed in Slack and calls. Flag mismatches: is the ticket
  what the customer is actually asking for, or has the need shifted?
- **Surface related tickets.** If Slack or the ticket references other tickets,
  note them. Assess whether they overlap, block, or should be prioritized first.
- Identify the business need and the proposed approach.
  If they seem inconsistent, add that to the vague list in Step 2.

## Step 2: Clarify what the ticket leaves vague

- Search for project documentation or agent context files (doc, memory, etc.)
  with related feature overviews and diagrams. If found, load as guidance.
- Read existing code in the affected area to understand current behavior.
  If the ticket references an existing pattern,
  read that code to understand what it does and how the new work differs.
- List everything the ticket leaves vague. For each item:
  - Try to answer it from the codebase first.
  - If the code answers it, document the finding.
  - If not, collect it for the user.
- Add findings and open questions to the working doc.
- Iterate with the user: review the doc, remove irrelevant questions,
  smooth wording. Collect new clarifications from the reporter
  or teammates (Slack threads, calls, etc.) and update the doc.
- Once the what and why are clear, post the notes to the ticket
  (Linear comment) so the team has the context alongside the ticket.

## Step 3: High-level design

This is the key artifact the user reviews carefully.

- Propose a design covering:
  - What components to build (new service, new endpoint, new cron, etc.)
  - How they connect to existing system
  - Key design decisions and trade-offs
  - Edge cases
  - Risks and mitigations:
    - Backward compatibility: could new response fields or behavior
      break existing clients that parse the response?
    - Performance: does this touch a hot path or high-volume endpoint?
      Will it add DB queries, external calls, or CPU work that needs
      caching, batching, or async handling?
    - Error handling strategy: if the new code fails, should the original
      operation still succeed? Should failures be silent or blocking?
- Keep it high-level: no specific files or line numbers yet.
- Persist the design in the working doc.
- Get user approval before moving to the detailed plan.

## Step 4: Detailed implementation plan

The user may skim or edit this, but not as carefully as the high-level design.

- Break the approved design into concrete steps:
  - Which files to create or modify
  - New functions, endpoints, DB queries, migrations, config
  - Execution order (what depends on what)
- Append the plan to the end of the working doc with a note:
  "This section has not been reviewed with the same rigor as the high-level design.
  Verify details before relying on them."

## Step 5: Create branch and write tests first (red)

> **Common mistake**: Do NOT write implementation logic in this step.
> Only create the minimal stub (function signature with a no-op body)
> needed for the test to compile. The real implementation belongs in Step 7.

- Create a new branch named `<ticket>-<short-description>`,
  including the ticket number for traceability.
- Write a **new, dedicated test function** (not assertions inside an existing test).
  Name it clearly so it is easy to find and run in isolation.
- Since the feature doesn't exist yet, the function/endpoint may not exist either.
  Use the **stub approach**: create the function signature with a
  no-op body (return zero values or error). Write tests against the stub.
  Tests compile but fail because the stub does nothing useful.
- A good test covers:
  - Existing response fields or behavior still work (regression check)
  - New fields/behavior are present
  - New values are valid (not just non-empty)
- Run the tests and confirm they fail **because the feature is missing**,
  not because of wrong environment setup.
- Present the failing output to the **user for review**.

### STOP: wait for user before continuing

## Step 6: Commit, push, and open draft PR

- Commit with message "add red tests for <ticket>-<short-description>".
- Push the branch to the remote. Verify the CI test fails with the same
  error as local. If results differ, go back to Step 5.
- Open a **draft PR** with the high-level design from Step 3 in the description
  and a test plan checklist. This gives teammates early visibility
  so they can comment, suggest, or help.
- Linear: add a comment with the draft PR link.
- Slack: share the draft PR link in the feature thread.

## Step 7: Implement the feature (green)

> Only begin this step after the failing tests are committed and pushed in Step 6.

- Implement the feature following the plan from Step 4.
- Run the failing tests again and confirm they pass.
- Run related tests to check for regressions.
- Verify the implementation matches risk mitigations decided in Step 3
  (e.g., "we said we'd batch these queries; did we?").
- Flag any new risks that emerged during coding but were not anticipated in the design.
  If found, discuss mitigations with the user before continuing.
- If the implementation reveals design gaps, update the plan
  and get user approval before continuing.

## Step 8: Document

- If the repo has a shared context directory (found in Step 2)
  and the feature adds complex logic, add or update a doc there.
- When the code deviates from the common approach,
  add a comment explaining why (often a business rule or edge case).
- If the feature introduces config (env vars, Vault keys, DB settings),
  document what needs to be set per environment.
- Consider what would prevent similar gaps in the future
  (e.g. missing API fields, untestable code, misleading docs).
  If the answer points to something beyond this feature, create a follow-up ticket.

## Step 9: Commit the implementation and mark PR ready for review

- Commit with a concise message focused on business logic.
- Push and mark the draft PR as ready for review.

## Step 10: Self-review the PR

- Self-review the PR diff for correctness, regressions, and code quality.
- Fix any blockers or suggestions before requesting external review.

## Step 11: Request review

- Slack: call the message draft tool to create a reply in the feature thread
  noting the PR is ready for review. Ask if the user wants you to send it.

## Step 12: Address review feedback

- Read reviewer comments and decide on each item with the user:
  whether to fix, defer, or explain why it is not actionable.
- Apply fixes, commit, push, and reply to the PR comment addressing each point.
- Ask the user if they want to request re-review on Slack.

> **Steps 13-17 are user-driven. The agent guides but does not act directly.**

## Step 13: Deploy branch to development environment and verify

- Deploy the feature branch to the dev environment using ArgoCD.
- Verify the feature works as expected.

## Step 14: Demo and collect feedback

- Demo the feature on the dev environment to stakeholders
  (requester, product, affected users).
  Walk through the key behavior from the user's perspective.
- Collect feedback and note any follow-up requests.
- If feedback requires changes, create follow-up tickets
  rather than reopening this one (unless the change is trivial).
- Only proceed to merge after stakeholders confirm the feature works as expected.

## Step 15: Merge and create release tag

- Merge the PR after approval and successful demo.
- Create a release tag on the merged commit.

## Step 16: Deploy to production

- Follow the project's production deployment process.
- Run smoke tests or sanity checks if available.
- Verify the feature works in production.

## Step 17: Announce

- Slack: draft a reply in the feature thread with the release version
  and confirm the feature is live.
- Linear: append an implementation summary to the issue description
  (design decisions, PR link, release version, deployment status,
  config changes needed) and move the issue to "Done".
