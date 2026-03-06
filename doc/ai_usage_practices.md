# AI Usage Practices

General concepts for working productively with AI coding agents.
For tool-specific setup, see [ai_common_settings.md](ai_common_settings.md).

## Basic Concepts

These concepts apply to any AI coding agent (Cursor, Claude Code, etc.).
Understanding them is essential for productive use.

### Context Window

The context window holds everything the agent sees in a session:
your messages, files it reads, command outputs, and its own responses.
It has a fixed size and performance degrades as it fills up.

Manage it actively:

- Start a new session or clear context (`/clear`) between unrelated tasks.
- Avoid letting the agent read too many files in one session.
  Delegate research to subagents when possible.
- If the agent starts "forgetting" instructions or making odd mistakes,
  the context is likely too full. Clear and restart with a better prompt.

### Explore, Plan, Then Code

Jumping straight to coding often solves the wrong problem.
The recommended flow:

- **Explore**: let the agent read relevant code and understand the current state.
- **Plan**: ask for an implementation plan. Review it before any code is written.
- **Implement**: execute the plan, with tests to verify.
- **Commit**: commit with a descriptive message.

Skip planning for small, obvious changes (typo fix, rename, add a log line).
Use it when the scope is unclear, multiple files are involved,
or you are unfamiliar with the code.

### Give the Agent a Way to Verify Its Work

This is the single highest-leverage practice.
Without verification, the agent produces code that looks right but may not work.

- Provide test cases or expected outputs.
- Ask the agent to run tests after implementing.
- For bugs: paste the actual error, not just "it's broken."
- For UI: paste a screenshot and ask the agent to compare its result.

### Be Specific in Prompts

Vague prompts lead to guesswork and wasted iterations.

- Reference specific files, functions, or line numbers.
- Describe the symptom, likely location, and what "fixed" looks like.
- Point to existing patterns in the codebase for the agent to follow.

### Course-Correct Early

Correct the agent as soon as it goes off track. Do not wait for it to finish.

- Interrupt mid-action if you see it heading the wrong way.
- If you have corrected the same issue twice, clear context
  and start fresh with a better prompt.
- Undo and rewind are cheap. Use them freely.

Reference: [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
