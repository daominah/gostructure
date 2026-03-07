---
name: review-code-and-pr
description: Review code change and pull request (PR) for correctness, impact, and safety.
  Use when implementing a feature, fixing a bug, reviewing a PR,
  or reviewing code changes before committing.
---

# Code Changes and Pull Request Review Checklist

## Code Meets Business Need

- The PR must link to its ticket, Slack thread, plan, etc. if available.
- Verify the PR describes the client pain point or use case being solved.
- Verify the sources (ticket, Slack, plan) are clear,
  self-consistent, and consistent with each other.
- For bugs: how do we reproduce it? How do we confirm the root cause?
  Is there a test that reproduces the bug?
  Optional: symptom of a deeper issue? Check similar past bugs.

## Code Works as Intended

- Every new, modified, or affected function must have a test proving it works.
- For bug fixes: a test that reproduces the bug and passes after the fix.
- For new features: tests must cover the main use case.
  Edge cases are optional but encouraged.
- Test comments use GIVEN (precondition) / WHEN (action) / THEN (result)
  to describe business behavior, readable by non-technical stakeholders.

## Do Not Break Existing Behavior

- Existing tests may not cover all behaviors.
  Check for changes that could break untested code paths.
- Additive changes can still degrade performance.
  Check for slow queries, missing indexes, or unnecessary load on shared resources.
- If the PR is too large to review confidently,
  note it as process feedback to prefer smaller PRs in future work.

## Observable Output

- Check that the change has observable output the user can verify,
  for example through the UI or a public API response.
- Long-running functions or background jobs provide a way to inspect
  progress through metrics, a dashboard, a status endpoint, logs, or database records.
- Support for cancellation is a nice to have.

## Security Considerations

- Check for hardcoded secrets, credentials, or real customer data in the code.
- Review risks from user inputs: is validation sufficient?
- Check if the change exposes sensitive data in API responses or error messages.

## Code Quality

- Code should be easy to read, change, and debug by someone who didn't write it.
- Improve the codebase where you touch it.
  Keep cleanup in separate commits from feature work for easier review and revert.
- Label nitpicks clearly so the author knows what is blocking vs optional.

## Process Feedback

If the review finds serious problems
(vague requirements, contradictory sources, wrong approach),
comment as process feedback:

- Requirements should be clear and agreed on before coding starts.
- Solution approach should be confirmed before implementation.
- This prevents misalignment earlier in future work.

# Human Reviewer Mindset (AI can ignore)

- Code review is a chance to share knowledge about the code and the product.
- The reviewer should be able to explain the change to others after reviewing.
- If the PR solves the business need and improves the codebase,
  approve it even if minor improvements remain. Track those as follow-ups.
