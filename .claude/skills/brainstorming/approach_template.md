# Approach Template

For simple decisions (naming, config choices, simple preferences),
skip the per-approach Pros/Cons tables and use only the summary
comparison table with a recommendation paragraph.

For complex decisions (architecture, infrastructure, data modeling),
use the full template below for each approach:

```
**Name** (recommended)
Describe what this approach does conversationally.
Scale the detail to the complexity: a sentence for something obvious,
a short paragraph for something nuanced.

| Pros | Cons |
|------|------|
| ...  | ...  |

Ground each point in what you learned from the codebase:
existing patterns, current dependencies, known constraints,
and where the project is heading if a roadmap or docs exist.

**When to prefer**: one sentence on the scenario
where this approach is the best fit.
```

After all approaches, add a summary comparison table:

```
| Criterion | Approach A | Approach B | Approach C |
|-----------|------------|------------|------------|
| ...       | ...        | ...        | ...        |
```

Pick criteria that highlight the meaningful differences between approaches
(e.g., implementation effort, durability, operational complexity).

## Rules

- Mark exactly one approach as "recommended".
- After the summary table, add a short paragraph
  explaining why the recommended one fits this specific situation.
- If the existing codebase has patterns that go against conventional knowledge,
  bad practices, or obvious drawbacks related to this decision,
  add one final approach that addresses the root issue through refactoring.
  Label it clearly so the user knows it requires changing existing code.
  This refactoring approach does not count toward the 2-3 limit.
