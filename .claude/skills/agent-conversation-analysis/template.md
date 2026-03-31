# Agent Conversation Analysis

**Generated**: {date}, **Projects**: {count}, **Tasks**: {count}, **Sessions**: {count}

## Summary

| Metric                       | Value                              |
|------------------------------|------------------------------------|
| Average task score           | {x.x} out of 5                     |
| Smooth tasks (scored 4-5)    | {n} ({%})                          |
| Struggled tasks (scored 1-2) | {n} ({%})                          |
| Most common friction pattern | {pattern}                          |
| Top improvement opportunity  | {suggestion}                       |
| Setup coverage               | {assessment of CLAUDE.md + skills} |

### Tasks Overview

| Project   | Task           | Score          | Manual corrections | Setup gaps | Time range     |
|-----------|----------------|----------------|--------------------|------------|----------------|
| {project} | [{task summary}](#task-{slug}) | {progress bar} | {n}                | {n}        | {first} → {last} |

(one row per task, newest first, no duplicates, score as: ★★★★★ ★★★★☆ ★★★☆☆ ★★☆☆☆ ★☆☆☆☆)
For struggled tasks (scored 1-2), prefix ⚠️ to the task name in the same row.
Task name is a markdown link to the corresponding `#### Task:` heading
using the auto-generated anchor (e.g. `[MMP-142 bug fix](#task-mmp-142-bug-fix)`).

## Scoring Methodology

| Criterion          | How measured                                                                                                                                 | Weight          |
|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------|-----------------|
| Outcome            | Task completed, partially done, or abandoned                                                                                                 | High            |
| Manual corrections | Keyword detection in user messages ("no", "try again", "revert", "wtf", "shit", etc.) indicating user redirected AI or expressed frustration | High            |
| Setup gaps         | User pasting context, explaining locations, repeating corrections across sessions                                                            | High            |
| Manual work        | Committed git diff lines not found in AI Write/Edit outputs, plus stale-read Edit failures                                                   | Low (uncertain) |
| Mental load        | Inferred from clarification loops, long pauses, complex back-and-forth                                                                       | Low (uncertain) |
| Time               | Session duration, used only as tiebreaker since user may walk away                                                                           | Low             |

Scale: ★★★★★ (autonomous) to ★☆☆☆☆ (struggling).
Adjusted for task complexity.

## Patterns & Recommendations

### Recurring friction

(only patterns from 2+ tasks)

- {pattern}: seen in {n} tasks. Root cause: {why}. Suggestion: {how}

### What you're doing well

- {pattern}: seen in {n} tasks

### CLAUDE.md improvements

(write exact lines to add, not vague descriptions)

- Add: "{specific line or section}"

### Skills to create

(explain what repeated pattern it would eliminate)

- Skill: "{name}": {what it does and why}

### Setup hygiene

- {observations about setup, workflow, habits}

## Task Details

(all per-project task breakdowns go here, at the end of the report)

### Project: {name}

**Setup used**: {n} skills triggered, {n} MCP tools called
**Git summary**: {commits} commits, {amends} amends/fixups

#### Task: {summary}

- **Score**: {1-5}, {label}
  (uncertainty: {low/medium/high} for hard-to-measure criteria)
- **Sessions**: {count}, {first message time} → {last message time}
- **Outcome**: {completed/partial/abandoned}
- **Manual corrections** (user redirecting AI): {count}
- **Setup gaps**: {count of manual context injections}
- **Git**: {commits} commits, {net lines} net lines, {churn ratio} churn ratio
- **What went well**: {brief}
- **Friction**: {brief, or "None"}
- **Root cause**: {why: bad prompt, missing context, missing skill, task ambiguity}
- **Suggestion**: {specific actionable suggestion}

(repeat per task, newest first)
