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

## Skill reviewer note

This file is not referenced from SKILL.md.
However, it is the source-of-truth design rationale used to generate this skill,
so it is intentionally kept.

## Tuning Correction Detection

The `CORRECTION_PHRASES` list in `collect_sessions.py` decides what counts
as a user correction. To update it with data (not guesses), follow this flow:

### Step 1: Dump user messages

```bash
python3 scripts/dev_dump_user_messages.py [--claude-dirs ~/.claude ~/other/.claude]
```

Outputs `tmp_dump_user_messages_<timestamp>.md` with all user messages
grouped by first word, frequency, and length.
Each message includes the preceding agent's context:
tools used, first meaningful line, and last meaningful line.
This context is critical for judging whether a message is a real correction.
Also includes Section 0: bash aliases (false positives to ignore).
Truncated at 256 chars per message.

### Step 2: LLM suggests regex patterns

Feed the full dump to an LLM.
If the dump exceeds 2MB, filter to specific first-word groups
or use `--claude-dirs` with fewer directories to reduce size.
Ask it to suggest regex patterns that detect user corrections,
using agent context to verify each match is a real correction.

The LLM outputs `tmp_likely_correction_phrases_<timestamp>.md` with:

- Regex patterns (Python `re` syntax, case-insensitive)
- 2-3 example matches with agent context
- Estimated false positive rate
- Two explicit choices per pattern: `[ ] ACCEPT` and `[ ] REJECT`
  (so unchecked items are clearly missed, not skipped)

### Step 3: Human reviews suggestions

Open the suggestion file. For each pattern, check one of ACCEPT or REJECT.
Edit patterns if needed (e.g. adjust regex, change anchoring).

### Step 4: Update collect_sessions.py

Apply accepted patterns:

- Regex patterns go in `CORRECTION_REGEXES` (compiled with `re.I`)
- Plain substring phrases stay in `CORRECTION_PHRASES`
- `is_correction()` checks regexes first, then falls back to substrings

Run the test suite to verify:

- Old false positives are now excluded
- New patterns catch expected messages
- Existing true positives still match

### Notes

- Run step 1 with `--claude-dirs` to include session data copied from other machines.
- `tmp_*` files are gitignored and timestamped for comparison.
- The dump script auto-detects bash aliases to flag false positives.
- Start-anchored regexes (`^pattern`) have lower false positive rates
  than substring checks because mid-sentence matches are usually not corrections.

## Measuring Extension Usage

Report a usage summary table for all Claude Code extensions
(custom skills, plugin skills, MCP servers, passive plugins, hooks)
so the user can see which provide value and which are dead weight.
Passive plugins and hooks are not yet trackable from session data.

## Reducing Report Variance Across Runs

Running the skill on different machines (or even re-running on the same machine)
produces reports that differ in task grouping, scores, and surfaced patterns.

SKILL.md addresses this with weighted grouping signals
and corrections-per-session scoring thresholds.
Comparing reports from different runs helps find findings each missed.
