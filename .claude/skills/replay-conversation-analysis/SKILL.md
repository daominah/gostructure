---
name: replay-conversation-analysis
description: >
  Analyze past Claude Code sessions like gaming replay analysis
  to minimize human effort. Scores sessions on outcome, corrections,
  setup gaps, manual work, mental load, and time.
  Use when the user wants to review their Claude usage,
  improve prompting effectiveness, or optimize their Claude setup.
  Also trigger when the user mentions "replay", "session analysis",
  "how am I doing with Claude", or wants to evaluate agent performance.
---

# Improve Claude Usage via Session Analysis

In gaming, replay analysis after a match is essential.
You watch what you did well and what you did badly,
so next match you reduce mistakes while perfecting what works.

Same idea applied here. A match is using Claude to complete a task.
Claude sessions are how you play that match.
Review them to minimize human effort to get shit done.

Your job is to read sessions, cross-validate with git and project setup,
score each task, and produce a report with actionable fixes.

## Data Sources

### Primary: Conversation Logs

Read JSONL files from `~/.claude/projects/`.
Each line is a JSON object with fields:
`type`, `sessionId`, `timestamp`, `message.role`, `message.content`,
`cwd`, `gitBranch`, `version`.

Use `~/.claude/history.jsonl` for cross-session user prompts
(fields: `timestamp`, `sessionId`, project path).

Use `~/.claude/sessions/` for session metadata
(fields: `pid`, `sessionId`, `cwd`, `startedAt`).

### Secondary: Git History

For each project directory found in session logs, run:

```bash
# Commits in the analysis period
git -C <project-dir> log --oneline --stat --since="<start>"

# Detect reverts, amends, fixups
git -C <project-dir> log --oneline --grep="revert\|fixup\|amend"

# File churn: files modified repeatedly
git -C <project-dir> log --diff-filter=M --name-only --since="<start>" \
  | sort | uniq -c | sort -rn | head -20
```

**Workspace handling**: the project `~/workspace/` is a meta-repo.
Git log at workspace root is noise.
Resolve the actual sub-repo from each session's `cwd` field
and run git commands there instead.

### Tertiary: Project Setup

- `CLAUDE.md` files (global `~/.claude/CLAUDE.md` and per-project)
- Skills in `.claude/skills/`
- Memory files in `.claude/` directories
- Skill invocations appear as `<command-name>` tags
  within conversation messages

### Optional: External Tickets

If MCP tools are available (Linear, Jira, etc.),
fetch linked tickets for richer task context.

## Grouping Sessions into Tasks

A task might span multiple sessions.
Group sessions that share the same goal by looking at:

- Similar `cwd` and `gitBranch` across sessions
- Overlapping time windows
- Related user prompts in `history.jsonl`
- Same ticket references

Two kinds of tasks:

- **Deliver value**: fix a ticket, ship a feature, etc.
- **Improve the system**: create a skill, set up an environment,
  reduce repetitive manual steps

## Scoring Criteria

Rate each task on these criteria.
Harder-to-measure criteria get lower weight.
Report uncertainty when data is insufficient.

### Measurable (higher weight)

- **Outcome**: task completion.
  If not completed, visible progress toward completion.
- **Corrections**: number of times the agent had to be asked
  to fix or change its output.
  Look for phrases like "no", "that's wrong", "I meant",
  "try again", "revert", "not what I asked".
- **Setup gaps**: amount of context the user copied in manually,
  plus explanations about where things are or how to access them.
  These indicate missing CLAUDE.md entries or skills.

### Hard to measure (lower weight, flag uncertainty)

- **Manual work**: amount of editing or finishing done manually
  after the agent responded.
  Infer from git commits without Co-Authored-By,
  or file changes outside session time windows.
- **Mental load**: amount of attention, review,
  and decision-making required.
  Infer from clarification loops, long pauses, complex back-and-forth.
- **Time**: weak signal since the user might walk away mid-task.
  Use only as a tiebreaker.

### Scoring Scale (1-5)

| Score | Label         | Meaning |
|-------|---------------|---------|
| 5     | Autonomous    | One-shot or near-perfect. Clean git, no corrections. |
| 4     | Guided        | Minor tweaks. Mostly smooth, clean outcome. |
| 3     | Collaborative | Notable back-and-forth, justified by complexity. |
| 2     | Corrective    | Multiple corrections, rework, or messy git history. |
| 1     | Struggling    | Repeated failures, user took over, or abandoned. |

### Scoring Heuristics

- 0 corrections + clean commits + task completed: 5
- 1 correction or minor clarifications + good outcome: 4
- 2-3 corrections or high file churn but solid final result: 3
- 4+ corrections, reverts in git, or significant rework: 2
- Abandoned, restarted, user manually fixed, revert-heavy: 1

Always adjust for task complexity:
a multi-file refactor scoring 3 is fine;
a typo fix scoring 3 means something went wrong.

### Cross-Validation

Do not trust conversation or git alone.

- Smooth conversation + git reverts = score should drop
- Messy conversation + clean commits = score may rise
- High file churn relative to net lines changed = thrashing

### Efficiency Signals (good)

- Low user-to-total message ratio
- Few tool calls per task
- First-attempt success
- Clean commit history

### Friction Signals (bad)

- Correction loops
- User manually pasting context Claude could have fetched
- Clarification loops before Claude acts
- Same file rewritten multiple times
- Reverts or fixup commits
- High churn relative to net lines changed

## Ask the User When Helpful

Before producing the report,
check if additional context would improve the analysis:

- "Session X had 6 corrections:
  was this a complex refactor or a simple task?"
- "Git shows 3 revert commits after session Y:
  were those related to Claude's output or separate work?"
- "There's no CLAUDE.md in project Z: intentional?"

Only ask when it meaningfully changes the analysis. Use judgment.

## Output Format

Produce a Markdown report:

```
# Claude Replay Analysis

**Generated**: {date}
**Projects analyzed**: {count}
**Sessions analyzed**: {count}

## Summary

| Metric | Value |
|--------|-------|
| Average task score | {x.x}/5 |
| Tasks scored 4-5 (smooth) | {n} ({%}) |
| Tasks scored 1-2 (friction) | {n} ({%}) |
| Most common friction pattern | {pattern} |
| Top improvement opportunity | {suggestion} |
| Setup coverage | {assessment of CLAUDE.md + skills} |

## Project: {name}

**Setup**: CLAUDE.md {exists/missing}, {n} skills configured
**Git summary**: {commits} commits, {reverts} reverts/amends

### Task: {summary}

- **Score**: {1-5}, {label}
  (uncertainty: {low/medium/high} for hard-to-measure criteria)
- **Sessions**: {count}, {session IDs or timestamps}
- **Outcome**: {completed/partial/abandoned}
- **Corrections**: {count}
- **Setup gaps**: {count of manual context injections}
- **Git**: {commits} commits, {net lines} net lines,
  {churn ratio} churn ratio
- **What went well**: {brief}
- **Friction**: {brief, or "None"}
- **Root cause**: {why: bad prompt, missing context,
  missing skill, task ambiguity}
- **Fix**: {specific actionable suggestion}

(repeat per task, newest first)

## Patterns & Recommendations

### Recurring friction
(only patterns from 2+ tasks)
- {pattern}: seen in {n} tasks. Root cause: {why}. Fix: {how}

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
```

## Rules

- Be honest and direct. Bad scores are useful feedback.
- Keep per-task summaries terse: one line per field.
- Focus on what the user can change:
  prompts, setup, skills, CLAUDE.md, workflow habits.
- Cross-validate conversation with git. Don't trust either alone.
- Mark tasks "Unscored" if too short or ambiguous to evaluate.
- In Patterns & Recommendations,
  only surface patterns from 2+ tasks.
- When suggesting CLAUDE.md additions,
  write the actual line to add, not a vague description.
- When suggesting skills,
  explain what repeated pattern it would eliminate.
- Report uncertainty on hard-to-measure criteria explicitly.
- The overall score averages across all tasks.
