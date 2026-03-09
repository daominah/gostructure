# Review of `.claude/skills/reviewing-code-and-pr/SKILL.md`

## Overall Assessment

The skill is well-structured, comprehensive, and covers the important dimensions
of code review. The checklist-style format makes it actionable.
Below are areas that could be improved.

## Observations

### 1. No instructions on how to determine what to review

The skill is triggered for "uncommitted local code changes, reviewing the latest
commit against the previous commit, or reviewing a pull request" but never tells
the AI *how* to obtain the diff. It relies on the AI figuring out the right
`git diff`, `git show`, or `gh pr diff` command on its own. Adding explicit
instructions like "run `git diff HEAD` for uncommitted changes" or "if given a PR
number, use `gh pr diff <number>`" would make behavior more predictable.

### 2. "Code Meets Business Need" is strict for maintenance work

The rule "flag as blocker and ask to provide one" when no ticket or problem
statement is linked applies universally. For dependency bumps, linting fixes, or
refactors where the motivation is self-evident, this produces false-positive
blockers. Consider adding an exception for clearly self-explanatory maintenance
changes, or downgrade to a suggestion for those cases.

### 3. "Every new, modified, or affected function must have a test" is broad

This would flag virtually every change as a blocker if taken literally. Changing
a log line, renaming a variable, or updating a dependency doesn't need a new
test. Consider scoping this to behavioral changes: "every function whose
observable behavior changes must have a test proving the new behavior."

### 4. Go-specific tooling section is embedded in a general skill

The "Code Quality" section ends with Go-specific instructions (`go vet`,
`go fix`, `staticcheck`). If this skill is intended to be reusable across
languages, the Go-specific part should either be conditional ("For Go code...")
— which it already is — or extracted to a separate skill that composes with this
one. As-is, it works fine for a Go-focused project, but worth noting if you plan
to reuse this skill elsewhere.

### 5. No guidance on review scope or depth

The skill doesn't tell the AI how deeply to investigate. Should it read every
caller of a modified function? Should it trace data flow through multiple files?
For large PRs this matters — the AI might either skim too quickly or spend
excessive context reading the entire codebase. A brief note on expected depth
(e.g., "check direct callers one level up" or "trace through the request path")
would help.

### 6. "Persist inputs and outputs for external service interactions" is an unusual review check

This is more of an architectural guideline than something a reviewer can verify
in a diff. In practice, the AI will either skip it or flag every external call
that doesn't have audit logging, which may not be actionable for the PR at hand.
Consider moving this to a design-review or architecture checklist rather than a
per-PR code review.

### 7. Output format could specify severity/priority

The current format has Blockers, Suggestions, and Nitpicks — which is good. But
within Blockers, there's no way to signal priority. If a PR has 5 blockers, the
author doesn't know which to fix first. Consider allowing a brief priority note
or ordering blockers by severity.

### 8. Missing: check for the diff itself being correct

The skill focuses on what the code does but doesn't instruct the AI to check for
accidental inclusions — debug prints left in, unrelated files staged, merge
conflict markers, TODO comments that should have been resolved. These are common
real-world review catches.

### 9. The "Process Feedback" section may produce noise

The trigger "if the review finds serious problems" is subjective. The AI may
append process feedback to routine reviews, which dilutes the signal. Consider
making the threshold more concrete, e.g., "if the verdict is REQUEST_CHANGES
*and* the root cause is unclear requirements or wrong approach."

## Summary

The skill covers business fit, correctness, regressions, observability,
security, and code quality — a solid foundation. The main improvements are:
reducing false-positive blockers for maintenance work, scoping test requirements
to behavioral changes, adding explicit diff-acquisition instructions, and
tightening the conditions for process feedback.
