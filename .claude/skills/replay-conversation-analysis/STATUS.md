---
name: replay-skill-status
description: Current progress on building the replay-conversation-analysis skill
type: project
---

# Replay Conversation Analysis Skill: Status

## What's Done

- Refined `gamer-idea.md` through ~20+ iterations of user feedback
  (source of truth for the concept)
- Created `SKILL.md` combining gamer-idea.md + valuable details from tmp.md
- Deleted `tmp.md` (its value is now in SKILL.md)
- Skill is registered and appears in available skills list

## What's Next (skill-creator workflow)

- **Test cases**: 3 draft prompts ready, user hasn't confirmed yet:
  - "How am I doing with Claude? Analyze my recent sessions."
  - "Review my Claude sessions for the gostructure project
    and tell me what I can improve."
  - "I feel like I keep correcting Claude on the same things.
    Can you analyze my sessions and find patterns?"
- Run test cases (with-skill vs baseline), grade, iterate
- Consider helper scripts for data collection/processing
  (parsing JSONL, aggregating git stats)
- Description optimization (last step)

## Key Decisions Made

- A "match" = a task, may span multiple sessions
- Two task types: deliver value vs improve the system
- 6 scoring criteria with confidence tiers
  (measurable: outcome, corrections, setup gaps;
  hard to measure: manual work, mental load, time)
- Workspace sub-repo handling: resolve actual repo from cwd
- Cross-validate conversation with git, don't trust either alone
- Score 1-5 scale with heuristics and complexity adjustment

## User Preferences (from refinement)

- Casual tone: "get shit done", not "unit of work"
- Bold only on key ideas, not everywhere
- Bullet points over numbered lists
- Gaming metaphor only in the Idea section intro
- No colon in title
- "reduce repetitive manual steps" not "automate repeat tasks"
