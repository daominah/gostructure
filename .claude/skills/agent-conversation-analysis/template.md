# Agent Conversation Analysis

**Generated**: {date} (all timestamps are UTC+7)

## Summary

**Projects**: {count}, **Tasks**: {count}, **Sessions**: {count}.

| Metric                       | Value                              |
|------------------------------|------------------------------------|
| Average task score           | {x.x} out of 5                     |
| Smooth tasks (scored 4-5)    | {n} ({%})                          |
| Struggled tasks (scored 1-2) | {n} ({%})                          |
| Most common friction pattern | {pattern}                          |
| Top improvement opportunity  | {suggestion}                       |
| Setup coverage               | {assessment of CLAUDE.md + skills} |

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

### Extension usage

| Extension | Type                                               | Sessions | Times used | Projects       |
|-----------|----------------------------------------------------|----------|------------|----------------|
| {name}    | {CustomSkill / PluginSkill / MCP / Passive / Hook} | {n}      | {n}        | {project list} |

(populate from `setup_usage` in the JSON: `skills_triggered` and `mcp_tools_called`.
Classify type by source: user `.claude/skills/` = CustomSkill,
plugin cache = PluginSkill, MCP tool = MCP.
Passive plugins and hooks are not yet tracked, note this gap.
Sort by sessions descending. Omit built-in commands like exit, model, compact, context.)

### Tasks Overview

| Project   | Task                           | Score          | Manual corrections | Setup gaps | First message    | Last message    | Duration      |
|-----------|--------------------------------|----------------|--------------------|------------|------------------|-----------------|---------------|
| {project} | [{task summary}](#task-{slug}) | {progress bar} | {n}                | {n}        | {first msg time} | {last msg time} | {e.g. 6h, 3d} |

(one row per task, newest first, no duplicates, score as: ★★★★★ ★★★★☆ ★★★☆☆ ★★☆☆☆ ★☆☆☆☆)
For struggled tasks (scored 1-2), prefix ⚠️ to the task name in the same row.
Task name is a markdown link to the corresponding `#### Task:` heading
using the auto-generated anchor (e.g. `[MMP-142 bug fix](#task-mmp-142-bug-fix)`).

## Task Details

(all per-project task breakdowns go here, at the end of the report)

### Project: {name}

**Setup used**: {n} skills triggered, {n} MCP tools called.
**Git summary**: {commits} commits.

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
