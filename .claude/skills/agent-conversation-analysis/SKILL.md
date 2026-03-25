---
name: agent-conversation-analysis
description: Analyzes past Claude sessions to improve usage effectiveness and reduce human effort. Use when analyzing AI-assisted workflows for improvement.
disable-model-invocation: true
---

# Claude Session Analysis

Goal: read past Claude sessions, score each task on how smoothly it went,
and produce a report with actionable fixes to reduce human effort.

## Workflow

Work through these steps in order. Check off each as you complete it.

- [ ] **Step 1: Collect data**: run `analyze.py` (see Data Collection below)
- [ ] **Step 2: Group sessions into tasks**: run `summarize.py` (see Grouping Sessions)
- [ ] **Step 3: Ask clarifying questions** if needed (see Ask the User When Helpful)
- [ ] **Step 4: Score each task** (see Scoring Criteria)
- [ ] **Step 5: Write the report** (see Output Format)

## Data Collection

The skill directory path was shown when this skill loaded
("Base directory: ..."). Use that path as `<skill-dir>`.

Detect the temp directory:

```bash
TMP=$(cygpath -m /tmp 2>/dev/null || echo /tmp)
echo "TMP=$TMP"
```

Note the printed value and use it directly (as a literal path)
in all subsequent commands. Do not re-run the detection or use
shell variables; substitute the actual value into each command.

Run the data collection script:

```bash
python3 <skill-dir>/scripts/analyze.py --days 30 --out <tmp>/replay_data.json
```

Where `<tmp>` is the literal value from detection above.

- Default: all projects. Use `--project <slug>` to filter (partial match).
- `--days` controls the analysis window. Use 7 for a quick look, 30 for a full review.

Read the output file with the Read tool. The JSON structure is:

```
{
  "projects": {
    "<project-path>": {
      "session_count": N,
      "git": {
        "commits_recent": N,
        "reverts_amends": N,
        "top_churned_files": [{ "file": "...", "modifications": N }],
        "net_lines_added": N,
        "net_lines_removed": N,
        "sub_repos": {                  // present if sub-repos detected inside project dir
          "<sub-repo-path>": { ...same fields as git... }
        },
        "sub_repos_total_commits": N    // aggregate across sub-repos
      },
      "manual_edits": {
        "ai_edited_files": [...],
        "committed_files": [...],
        "manual_edits": { "file.py": { committed_lines_not_in_ai, total_committed_lines } },
        "manual_edit_count": N,
        "stale_read_failures": N,
        "stale_read_examples": [...]
      },
      "setup_usage": {
        "skills_triggered": { "name": { count, sessions } },
        "mcp_tools_called": { "mcp__server__tool": { count, sessions } },
        "builtin_tools": { "Write": N, "Edit": N, ... },
        "total_skills_triggered": N,
        "total_mcp_tools_called": N
      },
      "sessions": [
        {
          "session_id": "...",
          "cwd": "...",
          "started_at": "...",
          "duration_minutes": N,
          "stats": {
            "user_messages": N,
            "assistant_messages": N,
            "corrections": N,           // user redirecting AI (system messages filtered out)
            "correction_examples": [...],
            "setup_gaps": N,            // user pasting context (system messages filtered out)
            "setup_gap_examples": [...]
          },
          "messages": [{ "role", "content", "timestamp" }]
        }
      ]
    }
  }
}
```

### Correction and setup gap filtering

The script automatically excludes these from correction/setup gap counts:

- Skill auto-load messages (`Base directory for this skill:`)
- Task notifications from subagents (`<task-notification>`)
- Command invocations and outputs (`<command-...>`, `<local-command-...>`)
- Context continuation summaries
- Grammar-check requests (`grammar?`, `smooth?`, `shorter?`)

### Sub-repo detection

A project directory may be a parent directory containing multiple git repos
(e.g. a monorepo workspace with several service repos inside).
The parent itself may or may not be a git repo.
The script scans for `.git` directories inside the project path and collects
git stats per sub-repo. The `sub_repos` field in the git data shows which
sub-repos had recent commits. Use `sub_repos_total_commits` for the real
commit count (the parent's `commits_recent` only covers the parent repo,
if it is one, and misses all sub-repo work).

## Grouping Sessions into Tasks

Run the summarize script to get a compact overview
(the full JSON is too large to read in context):

```bash
python3 <skill-dir>/scripts/summarize.py --timeline <tmp>/replay_data.json
```

- Default mode shows only sessions with manual corrections or setup gaps.
- `--timeline` shows all sessions chronologically with date, branch, duration,
  and first user message.

Use this output to group sessions into tasks.

### Helper scripts

Use these when you need to drill deeper into specific sessions:

- `python3 <skill-dir>/scripts/extract_task_details.py <tmp>/replay_data.json`
  Without `--session`: prints all sessions with correction flags.
  With `--session <id-prefix>`: prints full message flow for one session.
  Use to verify corrections and understand conversation context.

- `python3 <skill-dir>/scripts/scan_frustration.py <tmp>/replay_data.json`
  Scans for frustration keywords not yet in the detection list.
  Use to discover new correction patterns to add to `collect_sessions.py`.

Include all sessions where the user tried to get something done.
Only exclude pure Q&A sessions (1-2 questions, no file changes).

A task might span multiple sessions.
Group sessions that share the same goal by looking at:

- Similar `cwd` and `git_branch` across sessions
- Overlapping or adjacent time windows
- Related content in opening user messages

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
- **Manual corrections** (user redirecting AI): use `stats.corrections` from the JSON.
  Detected by keywords: "no", "try again", "revert", "wtf", "shit", "not work", "hmm", etc.
  Note: "hmm" specifically signals a mismatch between what the user expected and what Claude produced.
  The script filters out system-injected messages and grammar-check requests,
  but still verify by sampling `correction_examples` as keyword matching
  can produce false positives.
- **Setup gaps**: use `stats.setup_gaps`.
  Counts user messages that paste context Claude could have fetched itself.
  System-injected content (skill autoloads, task notifications) is filtered out.
  Root causes: missing CLAUDE.md entries, missing skills, missing MCP tools, or missing memory.

### Hard to measure (lower weight, flag uncertainty)

- **Manual work**: use `manual_edits` from the JSON.
  Compares committed git diff lines against Claude's Write/Edit tool outputs.
  Per-file ratio: `committed_lines_not_in_ai` / `total_committed_lines`.
  Also counts `stale_read_failures` (Edit where `old_string` was not found,
  meaning the file changed between Read and Edit).
- **Mental load**: infer from clarification loops, long pauses, complex back-and-forth.
- **Time**: weak signal since the user might walk away mid-task.
  Use only as a tiebreaker.

### Scoring Scale (1-5)

| Score | Label         | Meaning                                                     |
|-------|---------------|-------------------------------------------------------------|
| 5     | Autonomous    | One-shot or near-perfect. Clean git, no manual corrections. |
| 4     | Guided        | Minor tweaks. Mostly smooth, clean outcome.                 |
| 3     | Collaborative | Notable back-and-forth, justified by complexity.            |
| 2     | Corrective    | Multiple corrections, rework, or messy git history.         |
| 1     | Struggling    | Repeated failures, user took over, or abandoned.            |

### Scoring Heuristics

- 0 manual corrections + clean commits + task completed: 5
- 1 manual correction or minor clarifications + good outcome: 4
- 2-3 manual corrections or high file churn but solid final result: 3
- 4+ manual corrections, amends/fixups in git, or significant rework: 2
- Abandoned, restarted, user manually fixed, heavy rework: 1

Always adjust for task complexity:
a multi-file refactor scoring 3 is fine;
a typo fix scoring 3 means something went wrong.

### Cross-Validation

Do not trust conversation or git alone.

- Smooth conversation + git amends/fixups = score should drop
- Messy conversation + clean commits = score may rise
- High `top_churned_files` relative to `net_lines_added` = thrashing
- If the project is a parent directory with sub-repos, use `sub_repos` git data
  to find the actual repo where work happened, not the parent directory itself

## Ask the User When Helpful

Before producing the report,
check if additional context would meaningfully change the analysis:

- "Session X had 6 corrections: was this a complex refactor or a simple task?"
- "Git shows 3 revert commits after session Y:
  were those related to Claude's output or separate work?"
- "There's no CLAUDE.md in project Z: intentional?"

Only ask when it changes a score or a recommendation. Use judgment.

## Output Format

Write the report to `agent-conversation-analysis-result.md` in the current working directory.
Do not print the report inline; tell the user to open the file.

Read `<skill-dir>/template.md` for the report structure.
Follow the template exactly, filling in placeholders with real data.

## Rules

- Be honest and direct. Bad scores are useful feedback.
- Keep per-task summaries terse: one line per field.
- Focus on what the user can change: prompts, setup, skills, CLAUDE.md, workflow habits.
- Cross-validate conversation with git. Don't trust either alone.
- Mark tasks "Unscored" if too short or ambiguous to evaluate.
- In Patterns & Recommendations, only surface patterns from 2+ tasks.
- When suggesting CLAUDE.md additions, write the actual line to add.
- When suggesting skills, explain what repeated pattern it would eliminate.
- Report uncertainty on hard-to-measure criteria explicitly.
- The overall score averages across all tasks.
