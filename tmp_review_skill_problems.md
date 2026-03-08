# Remaining Problems in review-code-and-pr Skill

## Problem 8: "Long-running functions" has no time threshold

Line 62-63:

```
- Long-running functions or background jobs provide a way to inspect
  progress through metrics, a dashboard, a status endpoint, logs, or database records.
```

When does a function qualify as long-running? 1 second? 1 minute?
Add a threshold, e.g. "functions expected to run longer than 30 seconds."

## Problem 9: "nice to have" gives no decision criteria

Line 64:

```
- Support for cancellation is a nice to have.
```

The AI will consistently ignore this.
Either remove it or make it conditional,
e.g. flag missing cancellation for operations that exceed a time threshold.

## Problem 11: rationale listed as action item

Line 102:

```
- This prevents misalignment earlier in future work.
```

This is a rationale for lines 100-101, not a checklist item.
Move it above the list as context or remove it.

---

## Session Context

Problems fixed so far (from original 11):

- Problem 1: "if not linked:" broken instruction — fixed: blocker if no source and no PR description.
- Problem 2: "are clear" vague — fixed: "self-consistent and consistent with each other."
- Problem 3: "is validation sufficient?" — fixed: sanitize before use in queries, file paths, shell commands, rendered output.
- Problem 4: "easy to read" platitude — fixed: replaced with concrete Code Quality checklist from code_good.md.
- Problem 5: "break untested code paths" unbounded — fixed: check callers and shared state for side effects.
- Problem 6: "unnecessary load" no threshold — fixed: table scans, missing indexes, queries inside loops, unbounded resource growth, excessive external load.
- Problem 7: "Improve where you touch it" unbounded — kept as is per user choice, with cleanup-in-separate-commits qualifier.
- Problem 10: "Label nitpicks" redundant — kept per user choice, moved to top of Code Quality.

Workflow: loop through problems 1 by 1, suggest options (A/B/C), user picks, apply.

## Note

After fixing all problems, do a final review of the whole SKILL.md
based on how to create good agent skill instructions:
actionable, specific, checkable, no vague adjectives,
no unbounded scope, no missing thresholds.
