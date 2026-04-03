---
name: brainstorming
description: "Proposes 2-3 approaches with trade-offs for design decisions. Use when the user faces a decision with multiple viable paths: new tables, features, endpoints, or asks 'what if', 'how about', 'should we', 'pros cons', 'which approach'."
---

# Brainstorming

Propose approaches, wait for the user to pick, then step aside.

## Skip when

Exit this skill immediately (no output, no approaches) if any of these are true:

- A plan or design decision already exists for this topic in the conversation
  or in a working doc.
- The user gave a direct implementation instruction
  ("fix this", "add X to Y", "commit", "grammar?").
- The problem is too vague to identify distinct approaches even after clarifying.

## Workflow

1. **Scan context**: check relevant files, docs, or recent commits
   to understand the current state. Do not present approaches
   until you understand what exists.

2. **Clarify if needed**: if the problem has ambiguous requirements,
   ask one question at a time (prefer multiple choice) before proposing.
   Do not combine clarifying questions with approach proposals.

3. **Propose approaches**: present 2-3 options using the format below.
   Lead with your recommended option.

4. **Wait**: present the approaches and stop. Let the user respond.
  - **Picks one**: remind them of the most important cons of their chosen approach,
    then confirm. This skill is done; resume the parent flow if one exists.
  - **Requests revision**: adjust the chosen approach and re-present (step 3).
  - **Rejects all or adds new constraints**: go back to clarifying (step 2).
  - **Says "cancel" or "stop"**: skill is done, no decision made.

## Approach format

Read `approach_template.md` for the output template and rules.

