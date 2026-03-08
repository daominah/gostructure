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
- Summary: describing what the change does and how it meets the review criteria.
- Blockers: issues that must be resolved before merging.
  Only present when verdict is REQUEST_CHANGES.
- Suggestions: improvements worth tracking as follow-ups.
  Not blocking: the PR still solves the business need without them.
- Nitpicks: minor observations that do not affect
  correctness or functionality.

Omit Blockers, Suggestions, and Nitpicks if they have no items.

## Review Criteria

### Code Meets Business Need

- The PR must link to its problem source: ticket (Linear/Jira), Slack thread, plan, etc.
  If no source is linked, the PR description must state the problem being solved.
  If neither is provided, flag as blocker and ask to provide one.
- Verify the sources (ticket, report message, plan) are clear,
  self-consistent, and consistent with each other.
- For bugs: check whether we know how to reproduce it, how the root cause was confirmed,
  and whether a test reproduces the bug. If not: blocker.
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
  Check callers of modified functions and shared state for unintended side effects.
- Purely additive changes can still degrade performance.
  Check new queries for table scans, missing indexes, and queries inside loops.
  Check for unbounded resource growth, such as goroutines, channels, maps, or slices.
  Check for code that causes excessive load on external infrastructure.
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
- Check that user inputs are sanitized before use in queries,
  file paths, shell commands, and rendered output.
- Check if the change exposes sensitive data in API responses or error messages.

### Code Quality

- Label nitpicks clearly so the author knows what is blocking vs optional.
- Use descriptive names for wide-scope identifiers.
  Short names only for variables used within a few nearby lines.
- Handle errors early and return immediately to keep the main path simple and avoid nesting.
- If a function returns an error, always check it. Ignore it only explicitly.
- Function signatures should clearly show inputs, outputs, and side effects.
  No hidden mutations of inputs or global state.
- Define interfaces where they are used
  so the interface consumer depends only on the required behavior,
  not the implementation package.
- Control concurrency: every goroutine must have a clear lifetime and termination condition.
- Comments should explain intent and non-obvious behavior, not just repeat the function name.
- Persist inputs and outputs for external service interactions for debugging and auditing.
  Estimate storage growth and required capacity.
- Check retryable operations are idempotent and produce the same result if retried.
- Improve the codebase where you touch it.
  Keep cleanup in separate commits from feature work for easier review and revert.

### Process Feedback

If the review finds serious problems,
such as vague requirements that led to solving the wrong need,
contradictory source materials, or the wrong approach,
add recommendations to prevent similar issues in future work:

- Requirements should be clear and agreed on before coding starts.
- The solution approach should be confirmed before implementation.
- This prevents misalignment earlier in future work.
