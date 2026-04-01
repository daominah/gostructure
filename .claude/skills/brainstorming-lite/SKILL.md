---
name: brainstorming-lite
description: "Proposes 2-3 approaches with trade-offs for design decisions. Use when the user faces a decision with multiple viable paths: new tables, features, endpoints, or asks 'what if', 'how about', 'should we', 'pros cons', 'which approach'."
---

# Brainstorming Lite

Propose approaches, wait for the user to pick, then step aside.

## Skip when

Exit this skill immediately (no output, no approaches) if any of these are true:

- A plan or design decision already exists for this topic in the conversation
  or in a working doc.
- The user gave a direct implementation instruction
  ("fix this", "add X to Y", "commit", "grammar?").
- The problem is unclear: clarify first, then re-evaluate whether multiple approaches exist.

## Workflow

1. **Scan context**: check relevant files, docs, or recent commits
   to understand the current state. Do not present approaches
   until you understand what exists.

2. **Clarify if needed**: if the problem has ambiguous requirements,
   ask one question at a time (prefer multiple choice) before proposing.
   Do not combine clarifying questions with approach proposals.

3. **Propose approaches**: present 2-3 options using the format below.
   Lead with your recommended option. Do not propose more than 3.

4. **Wait**: present the approaches and stop. Let the user respond.
   - **Picks one**: skill is done.
   - **Requests revision**: adjust the chosen approach and re-present (step 3).
   - **Rejects all or adds new constraints**: go back to clarifying (step 2).
   - **Says "cancel" or "stop"**: skill is done, no decision made.

## Approach format

For each approach:

> **Name** (recommended)
> 1-2 sentence description of what this approach does.
> **Trade-off**: what you gain vs. what you give up.

Mark exactly one approach as "recommended" with your reasoning.
Keep each approach to 3 lines maximum.

## Done

When the user picks an approach, this skill is done.
Do not write a spec document, do not invoke another skill.
