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
ensure tests also cover the existing behavior as a regression baseline.

"Linear", "Slack", "GitHub", and "ArgoCD" in this workflow refer to
the project tracker, team chat, code hosting, and deployment tool respectively.
Replace with the user's available tools.

## Working doc

At the start, create `<ticket>-<short-description>.md` in the current working directory.
It carries the request, our findings, and the design through the workflow.

Order it for a reader who has not seen the ticket, from the highest level down.
Use only the sections that have content; delete the rest instead of leaving a placeholder.

- **Original**: the request in the requester's own words.
  - **The request** (Step 1): the ticket text, then the requester's own wording
    from email, chat, and calls, quoted verbatim in their language,
    with speaker, date, and link.
    Do not paraphrase the requester here: the doc owner reads this section
    to check the ask itself, not our summary of it.
- **High**: our reading of it and where the decision stands.
  - **Our reading** (Steps 1 and 2): what we take the request to mean, labelled as ours;
    where the decision stands: who decided what, when, and what is still open.
- **Lower**: what the code and production already do, then what follows from it.
  - **Findings** (Step 2): what the code, production data, and the team answered.
    Each fact appears once with its number and source. Prefer a table for counts and routes.
    Shorten wording, never facts: the working doc is the full record,
    the Linear and Slack surfaces are the short ones.
  - **Open questions** (Step 2): what nothing answered, for the user to decide.
  - **Spike results** (Step 3): what was tested, what was confirmed or rejected.
  - **High-level design** (Step 4): approach comparison, chosen design, trade-offs.
- **Appendix** last: sources, related tickets, decision history, checklist.
  - **Appendix**: sources and related tickets, decision history as dated one-line entries,
    then the step checklist. Name each step and mark it complete at the end of that step.

## Step 1: Understand the requirements

For a solo project with no tracker,
follow "Steps 1-2 alternative: understand and clarify the requirement" below
in place of this step.

- Read the Linear issue, Slack thread, or spec linked by the requester.
- If the ticket cites an email, read the original.
  The ticket text is a paraphrase, often written or polished by an AI,
  so the requester's wording can be lost or shifted in the retelling.
  Look in the ticket attachments and the customer relationship management tool (e.g. HubSpot).
  If it is attached but cannot be opened, or was never attached,
  ask the user for it explicitly, and say in "The request" that the original is missing
  until it arrives, rather than trusting the summary.
- **Search beyond the ticket to understand what the client actually needs.**
  Don't only read what's linked. Search Slack for the ticket ID, project name,
  and customer name. Check for a dedicated deal/project channel. Read recent threads.
- Check meeting recordings/transcripts (Fathom, Gemini notes, etc.)
  related to the ticket. Meeting discussions often contain decisions and context
  not captured in tickets or Slack threads.
- **Cross-check ticket vs. conversations.** Compare the ticket scope against
  what's actually discussed in Slack and calls. Flag mismatches: is the ticket
  what the customer is actually asking for, or has the need shifted?
  If the goal has shifted, capture the shift explicitly in the working doc
  (what the ticket says vs. what the team actually decided) and update
  "Our reading" with the new goal before proceeding.
- Surface related tickets. If Slack or the ticket references other tickets,
  note them. Assess whether they overlap, block, or should be prioritized first.
- Note deadlines, explicit and implicit: a date in the ticket, a promise made
  in chat or a call, the next meeting with the requester, the end of the cycle,
  a departure of someone involved. Record each with its source in "Our reading".
  If none was found, write that down too, so the reader knows it was looked for.
- Identify the business need and the proposed approach.
  If they seem inconsistent, add that to the vague list in Step 2.

## Step 2: Clarify what the ticket leaves vague

For a solo project with no tracker,
follow "Steps 1-2 alternative: understand and clarify the requirement" below
in place of this step.

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

## Steps 1-2 alternative: understand and clarify the requirement

For a solo project with no tracker, the repo itself is the source of truth,
and this mostly changes Steps 1-2.
The requirement usually arrives as a code question or a terse one-line ask, not a spec.
Read the repo top-down before asking anything:

- Find where the project states its high-level, close-to-business goals
  (an overview doc, a README section, etc.). If it is not obvious,
  tell the user where you think they live and confirm before relying on it.
- Locate the ask against those goals: which goal does it serve,
  or is it a new or changed goal?
- Trust order: high-level goals and key decisions are the most reliable.
  Long detailed spec docs may be stale or AI-generated and can conflict with the high-level docs,
  so verify them against the goals and the actual code rather than taking them at face value.
- Also read the decision records,
  the agent context file (e.g. CLAUDE.md) for open follow-ups,
  and the affected code and real logs. Grep before asserting.
- Surface the gap between the terse ask and what the goals, decisions,
  and code already imply. State it before proposing a design.
- Clarify the vague points with the user. When a point has distinct viable
  options, use the `brainstorming` skill: it handles the multiple-choice
  options with trade-offs and the answer-some / defer / re-frame loop.
- Cross-check the ask against the goals, decisions, and code.
  If it reopens or adds a goal, update the goals doc;
  record any reopened design decision alongside the existing decision records.
- Mechanical substitutions for the later steps: name the branch and doc
  `<short-description>` (no ticket prefix, doc slug same as branch slug);
  keep the draft PR but skip the Linear/Slack steps,
  marking them `(skipped: no ticket)` in the checklist;
  deploy with the project's own script, keep merge and tag user-driven,
  and replace the stakeholder demo with a local smoke test marked "not signed off".

## Step 3: Spike or demo (optional)

Sometimes the team needs to validate assumptions before committing to a design.
This step is optional: skip it when the approach is well understood.

**When to spike:**

- Uncertainty about whether a technology or API works as expected
- Need to see the UX firsthand before designing the integration

**How to spike:**

- Note the pause in the working doc (what you're testing and why)
- Build the minimal demo to answer the specific question
- Record results: screenshots, measurements, confirmed or rejected assumptions
- Resume at Step 4 with the spike findings informing the design

**What a spike is NOT:** a spike is not a prototype of the full feature.
It answers a specific question, not an attempt to build a rough version of the feature.

## Step 4: High-level design

This is the key artifact the user reviews carefully.

- **When multiple viable approaches exist**, document each with pros and cons
  in the working doc. Present the comparison to the user and get their explicit
  choice before writing up the design. Do not assume a decision was made just
  because the user discussed an approach.
- Propose a design covering:
  - What components to build (new service, new endpoint, new cron, etc.)
  - How they connect to existing system
    (include a Mermaid diagram when the design involves multiple systems or actors)
  - Key design decisions and trade-offs
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

## Step 5: Create branch and open draft PR with working doc

The PR is the container all subsequent commits land into.
Opening it now (before any code) lets teammates review the design and
gives the user a single URL to track from any machine.

- Create a new branch named `<ticket>-<short-description>`,
  including the ticket number for traceability.
- Commit the working doc (Steps 1-4 content) as the first commit.
- Push the branch.
- Open a **draft PR** with the high-level design from Step 4 in the description
  (and the working doc linked or quoted) plus a test plan checklist.
- Linear: add a comment with the draft PR link.
- Slack: share the draft PR link in the feature thread.

## Step 6: Detailed implementation plan

The user may skim or edit this, but not as carefully as the high-level design.

- Break the approved design into concrete steps:
  - Which files to create or modify
  - New functions, endpoints, DB queries, migrations, config
  - Edge cases and how to handle them
  - Execution order (what depends on what)
- Append the plan to the end of the working doc with a note:
  "This section has not been reviewed with the same rigor as the high-level design.
  Verify details before relying on them."
- Commit and push the updated working doc so the draft PR reflects the plan.

## Step 7: Write tests first (red)

> **Common mistake**: Do NOT write implementation logic in this step.
> Only create the minimal stub (function signature with a no-op body)
> needed for the test to compile. The real implementation belongs in Step 9.

- Prefer a new, dedicated test function,
  unless the change is small enough to fit naturally in an existing test.
- Since the feature doesn't exist yet, the function/endpoint may not exist either.
  Use the **stub approach**: create the function signature with a
  no-op body (return zero values or error). Write tests against the stub.
  Tests compile but fail because the stub does nothing useful.
- A good test covers:
  - Existing behavior still works (regression check)
  - New fields/behavior are present
  - New values are valid (not just non-empty)
- Run the tests and confirm they fail **because the feature is missing**,
  not because of wrong environment setup.
- Present the failing output to the **user for review**.

### STOP: wait for user before continuing

## Step 8: Commit and push red tests

- Commit with message "add red tests for <ticket>-<short-description>".
- Push the branch to the remote. Verify the CI test fails with the same
  error as local. If results differ, go back to Step 7.

## Step 9: Implement the feature (green)

> Only begin this step after the failing tests are committed and pushed in Step 8.

- Implement the feature following the plan from Step 6.
- Run the failing tests again and confirm they pass.
- Run related tests to check for regressions.
- Verify the implementation matches risk mitigations decided in Step 4
  (e.g., "we said we'd batch these queries; did we?").
- Flag any new risks that emerged during coding but were not anticipated in the design.
  If found, discuss mitigations with the user before continuing.
- If the implementation reveals design gaps, update the plan
  and get user approval before continuing.

## Step 10: Document

- If the repo has a shared context directory (found in Step 2)
  and the feature adds complex logic, add or update a doc there.
- When the code deviates from the common approach,
  add a comment explaining why (often a business rule or edge case).
- If the feature introduces config (env vars, Vault keys, DB settings),
  document what needs to be set per environment.
- Consider what would prevent similar gaps in the future
  (e.g. missing API fields, untestable code, misleading docs).
  If the answer points to something beyond this feature, create a follow-up ticket.

## Step 11: Commit the implementation and mark PR ready for review

- Commit with a concise message focused on business logic.
- Push and mark the draft PR as ready for review.
- Update the PR description with the final summary and test plan checklist.

## Step 12: Self-review the PR

- Use the `reviewing-code-and-pr` skill to review our own changes in this PR.
- Apply obvious improvements yourself without asking.
  For anything uncertain or involving trade-offs, ask the user to decide.

## Step 13: Request review

- Slack: call the message draft tool to create a reply in the feature thread
  noting the PR is ready for review. Ask if the user wants you to send it.

## Step 14: Address review feedback

- Read reviewer comments and decide on each item with the user:
  whether to fix, defer, or explain why it is not actionable.
- Apply fixes, commit, push, and reply to the PR comment addressing each point.
- Ask the user if they want to request re-review on Slack.

> **Steps 15-19 are user-driven. The agent guides but does not act directly.**

## Step 15: Deploy branch to development environment and verify

- Deploy the feature branch to the dev environment using ArgoCD.
- Verify the feature works as expected.

## Step 16: Demo and collect feedback

- Demo the feature on the dev environment to stakeholders
  (requester, product, affected users).
  Walk through the key behavior from the user's perspective.
- Collect feedback and note any follow-up requests.
- If feedback requires changes, create follow-up tickets
  rather than reopening this one (unless the change is trivial).
- Only proceed to merge after stakeholders confirm the feature works as expected.

## Step 17: Merge and create release tag

- Merge the PR after approval and successful demo.
- Create a release tag on the merged commit.

## Step 18: Deploy to production

- Follow the project's production deployment process.
- Run smoke tests or sanity checks if available.
- Verify the feature works in production.

## Step 19: Announce

- Slack: draft a reply in the feature thread with the release version
  and confirm the feature is live.
- Linear: append an implementation summary to the issue description
  (design decisions, PR link, release version, deployment status,
  config changes needed) and move the issue to "Done".
