---
name: github-api-fallback-for-gh
description: Fall back to the GitHub REST API with curl --netrc when the gh CLI is logged into the wrong account. Use when gh pr create, gh pr comment, or another gh write fails with "must be a collaborator", "Resource not accessible", or "Could not resolve to a Repository", typically a work account on a personal repo or the other way round.
---

# GitHub API Fallback for gh

The `gh` CLI holds one active account,
while `~/.netrc` can hold the credentials of another.
When the active `gh` account has no access to the repo,
call the GitHub REST API with `curl --netrc` instead.

## Rules

- **Try `gh` first.** Fall back only when it fails on access, not on bad input.
- **Do not switch `gh` accounts** (`gh auth switch`, `gh auth login`)
  without explicit confirmation: other sessions may rely on the active account.
- **Never read or print the token**: no `cat ~/.netrc`, no keychain lookups.
  `curl --netrc` uses it without exposing it.
- `~/.netrc` needs an entry for `api.github.com`
  (an entry for `github.com` alone is not used by API calls).
  The token needs `Pull requests: Read and write` on the repo for pull request calls.
  If the call returns 401 or 404, ask the user to check the entry and the token scope.

## Create a pull request

Write the description to a file first,
then build the JSON body with `jq --rawfile`, so quotes and newlines are escaped.
Do not inline the description as `"$(cat <<'EOF' ...)"`:
an apostrophe in the text breaks the shell quoting.
Read the URL from the response:

```bash
jq -n \
  --arg title "{title}" \
  --arg head "{branch}" \
  --arg base "main" \
  --rawfile body {body_file} \
  '{title: $title, head: $head, base: $base, body: $body, draft: false}' |
  curl -s --netrc -X POST \
    -H "Accept: application/vnd.github+json" \
    https://api.github.com/repos/{owner}/{repo}/pulls -d @- |
  jq -r '.html_url // .message, (.errors // [] | .[]?.message)'
```

Set `draft: true` for a draft pull request.

## Other calls

Same `curl -s --netrc -H "Accept: application/vnd.github+json"` prefix:

- Edit title or body: `PATCH /repos/{owner}/{repo}/pulls/{number}`.
- Comment on a pull request or issue: `POST /repos/{owner}/{repo}/issues/{number}/comments`
  with `{"body": "..."}`.
- Read a pull request: `GET /repos/{owner}/{repo}/pulls/{number}`.

Marking a draft as ready for review is not in the REST API
(GraphQL mutation `markPullRequestReadyForReview` only):
ask the user to click "Ready for review" on the pull request page.

## Avoid repeated permission prompts

Suggest the user allow the exact command shape per repo
in the project `.claude/settings.local.json`:

```json
"Bash(curl -s --netrc -X POST -H \"Accept: application/vnd.github+json\" https://api.github.com/repos/{owner}/{repo}/pulls -d @-)"
```
