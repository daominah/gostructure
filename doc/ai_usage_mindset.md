# How to Use AI Effectively

## Guidelines

1. Even better than doing something yourself is having AI do it for you.
2. Prototype end-to-end fast: AI fills the gaps until specialists take over.
3. Provide and maintain context through docs and tools so AI understands your domain and specific work.
4. Repeated corrections likely mean a context gap. Fix the context, not the AI output.
5. Get to a solid high-level plan before coding. Review it carefully to avoid big code changes later.
6. When verifying each step, check critical lines and read the tests.

---

## Guidelines Explained

### 1. Have AI Do It For You

Invest in your agent setup continuously: write down your preferences, conventions,
and workflows so the agent applies them automatically, without re-explaining each session.
The output should fit your specific work, not be generic.
The better your setup, the less you need to correct.

Identify repetitive tasks in your daily work and set up the agent to handle them automatically.

---

### 2. You Can Go Further Alone Now

As a backend developer, you can now ship a runnable frontend or a working design
without waiting for a specialist.
It may not be production-grade, but it is good enough to move forward and validate ideas.
Bring in a specialist later when it actually matters.

The same applies in reverse: designers can prototype logic, non-devs can write scripts.

Get a working end-to-end flow running yourself first.
That gives you something concrete to show, test, and hand off.
A running flow also lets you give AI better feedback while working on the problem.

---

### 3. Provide and Maintain Context: Docs, Tools, Domain Knowledge

The model's intelligence is fixed. Context is the variable you control.
AI has no idea about your business goals, past decisions, or constraints
unless you tell it.

What to write down and document:

- Business goals: what you're trying to achieve and why, who the users are.
- Why decisions were made: not just what you chose, but why.
  So AI doesn't confidently undo something you deliberately decided.
- Constraints: what's off limits, what stack you use, what standards to follow.
- What didn't work: things you already tried.
  Without this, AI will confidently suggest the same failed approach again.

How to maintain it:

Document these so future sessions can use them.
After making a decision, write down why you chose it and the trade-offs considered.
Use diagrams for complex logic flows; they help both AI and humans understand the system.
When your system evolves, update the docs.

Tools to provide and update context:

- Custom instructions: Write standing instructions that apply to every session automatically.
  Use this for coding style, preferred stack, tone, or any rule you always want AI to follow.
  Examples: Cursor rules, Cursor skills, ChatGPT custom instructions, Claude project instructions.
- RAG (Retrieval-Augmented Generation): Store your docs in a searchable index.
  When you ask AI something, it fetches the relevant parts and adds them to the prompt.
  Use this when you have too much context to fit in one chat.
- MCP (Model Context Protocol): Let AI connect to your tools, data, and APIs.
  Instead of copy-pasting, AI can pull live data when needed.
  Use this when context changes often or lives in external systems.

You are building a living asset, not briefing a stranger every single session.

**Be careful with sensitive data.**
Avoid entering confidential, personal, or proprietary information into public AI models.
Data entered into public models may be used for training or exposed in other ways.
For sensitive work, use models deployed in your own environment or with clear data policies.

---

### 4. Repeated Corrections Signal a Context Gap

If you keep having to correct AI on the same thing,
that is likely a signal that your context has gaps.

Every repeated correction is a bug report on your context.
Stop correcting the output and fix the context instead.

Once you fill the gap, every future session benefits automatically.
That is the long-term benefit of treating context as an asset.

---

### 5. Get to a Solid High-level Plan Before Coding

- High-level design: what to build, how it connects to existing systems,
  key trade-offs and risks. **Review this carefully.**
  Catching a wrong assumption here is better than doing a big refactor after code is written.
- Detailed plan: which files to create or modify, execution order.
  Skim this; it usually has too much detail to be perfect and is refined as implementation proceeds.

---

### 6. Work in Small Steps With Smart Reviews Focused on Critical Paths and Tests

As you work through each step, focus your review on what matters most, not every line.

Check critical lines first:

- DB writes: inserts, updates, deletes.
- Auth and access checks: who is allowed to do what.
- Input handling: anything that touches user-supplied data.
- Error handling: what gets swallowed silently, what fails loudly.
- What AI removed: it sometimes quietly refactors things you did not ask it to touch.

**Then read the tests, not necessarily all the code.**
Tests are shorter and closer to what the code should do: given this input, expect this outcome.
Better yet, have AI generate the tests too, then review those.
If the tests are wrong or missing, that tells you where the real gaps are.
You can also ask AI to explain any part of the output you are unsure about.

**AI can hallucinate.**
It can confidently produce wrong facts, incorrect API usage, or outdated information.
Verify anything critical before shipping or acting on it.
