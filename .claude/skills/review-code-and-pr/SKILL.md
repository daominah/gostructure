---
name: review-code-and-pr
description: Review code changes and pull requests for business fit,
  implementation approach, regressions, observability, security, and code quality.
  Use when reviewing uncommitted local code changes,
  reviewing the latest commit against the previous commit,
  or reviewing a pull request.
---

## Output Format

Output the review with these sections in order:

- Verdict: APPROVE or REQUEST_CHANGES.
- Summary: one paragraph describing what the change does
  and whether it meets the business need.
- Blockers: issues that must be resolved before merging.
  Only present when verdict is REQUEST_CHANGES.
- Suggestions: improvements worth tracking as follow-ups.
  Not blocking: the PR still solves the business need without them.
- Nitpicks: minor observations that do not affect
  correctness or functionality.

Omit Blockers, Suggestions, and Nitpicks if they have no items.

## Review Criteria

### Code Meets Business Need

- The PR must link to its ticket (Linear/Jira), Slack thread, plan, etc.
  if not linked:
- Verify the PR describes the client pain point or use case being solved.
- Verify the sources (ticket, report message, plan) are clear,
  self-consistent, and consistent with each other.
- For bugs: how do we reproduce it? How do we confirm the root cause?
  Is there a test that reproduces the bug?
  Optional: symptom of a deeper issue? Check similar past bugs.

### Code Works as Intended

- Every new, modified, or affected function must have a test proving it works.
- For bug fixes: a test that reproduces the bug and passes after the fix.
- For new features: tests must cover the main use case.
  Edge cases are optional but encouraged.
- Test comments use GIVEN (precondition) / WHEN (action) / THEN (result)
  to describe business behavior, readable by non-technical stakeholders.

### Do Not Break Existing Behavior

- Existing tests may not cover all behaviors.
  Check for changes that could break untested code paths.
- Purely additive changes can still degrade performance.
  Check for slow queries, missing indexes, or unnecessary load on shared resources.
- If the PR is too large to review confidently,
  note it as process feedback to prefer smaller PRs in future work.

### Observable Output

- Check that the change has observable output the user can verify,
  for example through the UI or a public API response.
- Long-running functions or background jobs provide a way to inspect
  progress through metrics, a dashboard, a status endpoint, logs, or database records.
- Support for cancellation is a nice to have.

### Security Considerations

- Check for hardcoded secrets, credentials, or real customer data in the code.
- Review risks from user inputs: is validation sufficient?
- Check if the change exposes sensitive data in API responses or error messages.

### Code Quality

- Code should be easy to read, change, and debug by someone who didn't write it.
- Improve the codebase where you touch it.
  Keep cleanup in separate commits from feature work for easier review and revert.
- Label nitpicks clearly so the author knows what is blocking vs optional.

### Process Feedback

If the review finds serious problems,
such as vague requirements that led to solving the wrong need,
contradictory source materials, or the wrong approach,
add recommendations to prevent similar issues in future work:

- Requirements should be clear and agreed on before coding starts.
- The solution approach should be confirmed before implementation.
- This prevents misalignment earlier in future work.
