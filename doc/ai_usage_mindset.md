# How to Use AI Effectively

## Guidelines

1. Even better than doing something yourself is having AI do it for you.
2. Prototype end-to-end fast: AI fills the gaps until specialists take over.
3. Provide and maintain context through docs and tools so AI understands your domain and specific work.
4. Repeated corrections likely mean a context gap. Fix the context, not the AI output.
5. Use plan mode: have AI outline the approach, refine until solid, then execute in small steps.
   Small steps control scope, not micromanaging how; give AI a clear goal and let it decide the path.
6. When verifying each step, check critical lines and read the tests.

---

## Guidelines Explained

### 1. Have AI Do It For You

Your job shifts from *doing* to *directing*.
Developers who stay in "I'll just do it myself" mode miss the multiplier entirely.

AI saves time on cognitive tasks.
Work that used to take hours (writing code, researching, drafting) now takes minutes.
You get a fast first output to react to, rather than starting from scratch.
Reacting is much easier than generating from nothing.

The better you are at directing AI, the more you can get done.

Identify repetitive tasks in your daily work that AI can handle, and automate them.

**Assign a role to get better output.**
Tell AI what persona to adopt before giving it a task.
"Act as a senior backend engineer reviewing this for security issues" produces
much more focused output than a generic prompt.

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

AI can do the narrow, specialized work.
You focus on the bigger picture and work across different areas
instead of sticking to one narrow specialty.

---

### 3. Provide and Maintain Context: Docs, Tools, Domain Knowledge

The model's intelligence is fixed. Context is the variable you control.

AI has no idea about your business, your codebase, your decisions, or your constraints
unless you tell it. The only way AI becomes *genuinely* useful rather than *generically*
useful is through the context you provide.

**What to write down and document:**

- **Business goals**: what you're trying to achieve and why, who the users are
- **Why decisions were made**: not just what you chose, but why.
  So AI doesn't confidently undo something you deliberately decided.
- **Constraints**: what's off limits, what stack you use, what standards to follow
- **What didn't work**: things you already tried.
  Without this, AI will confidently suggest the same failed approach again.

**How to maintain it:**

Document these so future sessions can use them.
After solving a hard problem, write down why you made the decision.
When you discover a constraint, note it immediately.
When your system evolves, update the docs.

**Tools to provide and update context:**

- **Custom instructions**: Write standing instructions that apply to every session automatically.
  Use this for coding style, preferred stack, tone, or any rule you always want AI to follow.
  Examples: Cursor rules, Cursor skills, ChatGPT custom instructions, Claude project instructions.
- **RAG (Retrieval-Augmented Generation)**: Store your docs in a searchable index.
  When you ask AI something, it fetches the relevant parts and adds them to the prompt.
  Use this when you have too much context to fit in one chat.
- **MCP (Model Context Protocol)**: Let AI connect to your tools, data, and APIs.
  Instead of copy-pasting, AI can pull live data when needed.
  Use this when context changes often or lives in external systems.

You are building a living asset, not briefing a stranger every single session.

**Once the context is solid, trust AI to figure out the path.**
Give it a clear goal rather than a rigid step-by-step script.
Avoid "boxing in" the AI with overly detailed instructions.
Micromanaging limits what AI can do.
Often, less structure gives better results.

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

### 5. Use Plan Mode: Get to a Solid Plan First

For any non-trivial task, do not let AI jump straight into generating code or output.
Ask it to produce a plan first.

For example: "Outline a plan to implement X. Do not write any code yet."

Review the plan. This is where your effort is most valuable.
Catching a wrong assumption at the plan stage costs nothing.
Catching it after AI has generated 300 lines of code costs a lot more.

Once the plan looks right, tell AI to proceed in small steps rather than all at once.
Smaller outputs are easier to verify and easier to correct if something is off.
Small steps control the scope of each task, not micromanaging how to do it.
Within each step, give AI a clear goal and let it decide how to get there.
This is different from boxing in the AI: small steps narrow the scope, not the approach.

---

### 6. Work in Small Steps With Smart Reviews Focused on Critical Paths and Tests

As you work through each step, focus your review on what matters most, not every line.

**Check critical lines first:**

- **DB writes**: inserts, updates, deletes
- **Auth and access checks**: who is allowed to do what
- **Input handling**: anything that touches user-supplied data
- **Error handling**: what gets swallowed silently, what fails loudly
- **What AI removed or changed**: it sometimes quietly refactors things you did not ask it to touch

**Then read the tests, not necessarily all the code.**
Tests are shorter and closer to what the code should do: given this input, expect this outcome.
Better yet, have AI generate the tests too, then review those.
If the tests are wrong or missing, that tells you where the real gaps are.
You can also ask AI to explain any part of the output you are unsure about.

**AI can hallucinate.**
It can confidently produce wrong facts, incorrect API usage, or outdated information.
Verify anything critical before shipping or acting on it.
