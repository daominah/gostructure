---
name: reviewing-agent-skill
description: Suggest improvements to make a SKILL.md file follow authoring best practices. Use when reviewing or editing a SKILL.md file.
---

# Reviewing Agent Skills

## Review result format

Output the review with these sections in order:

- **Verdict**: PASS or NEEDS_WORK.
- **Summary**: Describe which criteria the skill does well on and overall quality assessment.
- **Issues**: problems that should be fixed. Present only when verdict is NEEDS_WORK.
- **Suggestions**: improvements that are not required but worth considering. Omit if empty.

## Review Checklist

### Automated Validation

Run [validate_skill.py](./validate_skill.py) with the target SKILL.md path.
The script checks:

- `name` field: max 64 characters, lowercase letters/numbers/hyphens only,
  no reserved words ("anthropic", "claude").
- `description` field: non-empty, max 1024 characters, **single line**
  (multi-line YAML values like `>-` or indented continuations are valid syntax,
  but can cause missed triggers).
- SKILL.md body is under 500 lines.
- No Windows-style backslash paths.

### Metadata

- Description is written in **third person**
  ("Processes files..." not "I help you..." or "You can use this to...").
- Description states both **what** the skill does and a **"Use when"** clause
  (trigger scenarios, key terms the user might mention).
- Description is specific enough for the agent to distinguish this skill
  from other available skills.
- `disable-model-invocation: true` is present when the skill is work-in-progress
  or should not trigger automatically, e.g. "deploy-something".

### Conciseness

- Only includes information the agent does not already know.
  Omit generic explanations of well-known concepts.

### Structure and Progressive Disclosure

- Detailed reference material lives in separate files, not inline in SKILL.md.
- File references from SKILL.md are **one level deep** (no chains like A → B → C).
- Reference files longer than 100 lines have a table of contents at the top.
  Exception: the SKILL.md explicitly instructs the agent to read the entire file
  (e.g. a SQL schema or generated file).

### Workflows

- Complex multi-step tasks are broken into clear sequential steps.
- Quality-critical tasks include a feedback loop (validate → fix → re-validate).
- Multistep workflows include a checklist so the agent can track progress.
- Skills that produce structured output should include an output template.
- Tasks with decision points should have conditional branching
  ("Creating new? follow X. Editing existing? follow Y"),
  not just linear sequential steps.

### Content Quality

- Terminology is consistent throughout (one term per concept, not mixing synonyms).
- Examples are concrete and specific, not abstract descriptions.
- No time-sensitive information (e.g. "before August 2025, use the old API").
  Use an "old patterns" section with `<details>` if historical context is needed.
- Skills where output quality depends on seeing examples should include
  multiple labeled examples (Input/Output pairs),
  not just mention that examples should be concrete.

### Scripts

- Scripts handle errors explicitly instead of failing and letting the agent figure it out.
- No "voodoo constants": magic numbers are documented with rationale.
- Required packages/dependencies are listed.
- Instructions clarify whether to **execute** or **read** each script.
- Prefer bundling pre-made scripts over asking the agent to generate code:
  scripts are more reliable, save tokens, and ensure consistency.

### Re-validation

If the verdict is NEEDS_WORK,
re-run the review after the author addresses the issues to verify fixes.
