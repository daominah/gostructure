# Approach Template

For simple decisions (naming, config choices, simple preferences),
skip the per-approach Pros/Cons tables
and use only the summary comparison table with a recommendation paragraph.

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

**When to prefer**: one sentence on the scenario where this approach is the best fit.
```

Ground each Pros/Cons point in what you learned from the codebase:
existing patterns, current dependencies, known constraints,
and where the project is heading if a roadmap or docs exist.

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

## Summary table rendering

Claude Code's terminal wraps long cell content within each column
to fit Markdown tables to the terminal width.
The column count is fixed (criterion + one column per Approach),
so each cell has roughly (terminal_width / column_count) chars
before its content wraps onto a second visual line.
For a typical 80-char terminal:

- 3 columns: ~24 chars per cell before wrapping
- 4 columns: ~18 chars per cell

Aim for cells that fit on 1 line, or wrap to at most 2 lines.
Cells that wrap to 3+ lines make the row hard to scan.
The detailed reasoning belongs in each Approach's description above,
not in the summary cells.

Example naming brainstorm output (4-column table; cells fit on 1-2 visual lines in an 80-char terminal):

```
| Criterion             | Source / Destination | Upstream / Downstream | Inbound / Outbound |
|-----------------------|----------------------|-----------------------|--------------------|
| Antonym pair          | Yes                  | Yes                   | Yes                |
| Avoids SMPP collision | No (both clash)      | Yes                   | Yes                |
| Direct (no metaphor)  | Yes                  | No (river image)      | Yes                |
| Already in repo       | Old peer label       | "Downstream" used     | New term           |
| Label length          | 6 / 11 chars         | 8 / 10 chars          | 7 / 8 chars        |

Recommendation: Inbound / Outbound.
Source / Destination clashes with SMPP PDU fields (`source_addr` / `destination_addr`);
both halves of the natural antonym pair are unusable.
Between the two collision-free pairs, Inbound / Outbound reads directly
without invoking the river/pipe metaphor that Upstream / Downstream requires.
```
