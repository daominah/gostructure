# Improve Claude Usage via Session Analysis

## Idea

In gaming, **replay analysis** after a match is essential.
You watch what you did well and what you did badly,
so next match you reduce mistakes while perfecting what works.

Same idea applied here. A match is using Claude to complete a task.
**Claude sessions** are how you play that match.
Review them to **minimize human effort** to get shit done.

## Scoring

A task might span multiple sessions. Two kinds of tasks:

- Deliver value: fix a ticket, ship a feature, etc.
- Improve the system: create a skill, set up an environment,
  reduce repetitive manual steps

Agent usage evaluation criteria
(harder to measure = lower weight, report uncertainty):

- Outcome: task completion.
  If not completed, visible progress toward completion.
- Corrections: number of times the agent had to be asked
  to fix or change its output.
- Setup gaps: amount of context copied in,
  plus explanations about where things are or how to access them.
- Manual work: amount of editing or finishing done manually
  after the agent responded. (hard to measure)
- Mental load: amount of attention, review,
  and decision-making required. (hard to measure)
- Time: weak signal since the user might walk away mid-task.
  (hard to measure)

Overall score averages across all tasks.

## Input

- Everything under `~/.claude/` (logs, history, setup, memories)
- Related repos, with git and project scope Claude setup.
- External tickets (optional, via MCP)

## Output

Markdown report containing:

- Overall score and distribution across tasks
- Per-project setup assessment
- Per-task scoring with evaluation criteria breakdown
- Cross-validated findings (conversation vs git vs manual edits)
- Recurring patterns across 2+ tasks
- Actionable fixes: exact CLAUDE.md lines to add,
  skills to create, workflow changes

## Review note

This file is not referenced from SKILL.md.
However, it is the source-of-truth design rationale used to generate this skill,
so it is intentionally kept.
