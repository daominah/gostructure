# Writing Style

- Avoid dashes (`-` or `—`) in the middle of sentences;
  rephrase or use colons instead.
  Compound words are allowed: "real-time", "back-end".
- Use standard straight quotes (`'` and `"`) instead of curly quotes.

# Testing

Do not weaken or remove test assertions when the error looks like an environment issue;
ask the user to fix the environment setup instead.

# Git Commit

- Before committing, check the staged changes for secrets (API keys, tokens, passwords, etc.)
  and warn the user if any are found.
- ALWAYS invoke skill `commit-messages` before ANY git commit,
  including short user requests: "commit", "git commit", "commit push", "git commit push", etc.
