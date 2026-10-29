---
name: github-api-fallback-for-gh
description: Falls back to the GitHub REST and GraphQL APIs with curl --netrc when the gh CLI is logged into the wrong account. Use when gh pr create, gh pr comment, or another gh write fails with "must be a collaborator", "Resource not accessible", or "Could not resolve to a Repository", typically a work account on a personal repo or the other way round.
---

# GitHub API Fallback for gh

The `gh` CLI holds one active account,
while `~/.netrc` can hold the credentials of another.
When the active `gh` account has no access to the repo,
call the GitHub API with `curl --netrc` instead.

## Rules

- **Try `gh` first.** Fall back only when it fails on access, not on bad input.
- **Do not switch `gh` accounts** (`gh auth switch`, `gh auth login`)
  without explicit confirmation: other sessions may rely on the active account.
- **Never read or print the token**: no `cat ~/.netrc`, no keychain lookups.
  `curl --netrc` uses it without exposing it.
- `~/.netrc` needs an entry for `api.github.com`
  (an entry for `github.com` alone is not used by API calls).
  The token needs `Pull requests: Read and write` on the repo for pull request calls.
  If a call returns 401 or 404, ask the user to check the entry and the token scope.

## Create a pull request

Write the description to a file, then execute [create_pr.sh](./create_pr.sh)
from this skill directory (`{skill_dir}`, shown when the skill loads):

```bash
{skill_dir}/create_pr.sh \
  {owner}/{repo} {head_branch} main "{title}" {body_file} [--draft]
```

It prints the pull request URL, or the API error message and exits non-zero.
Requires `jq` and `curl`.

## Other calls

Same `curl -s --netrc -H "Accept: application/vnd.github+json"` prefix:

- Edit title or body: `PATCH /repos/{owner}/{repo}/pulls/{number}`.
- Comment on a pull request or issue: `POST /repos/{owner}/{repo}/issues/{number}/comments`
  with `{"body": "..."}`; build the JSON with `jq --rawfile` from a file.
- Read a pull request: `GET /repos/{owner}/{repo}/pulls/{number}`.
- Mark a draft ready for review: not in the REST API, only GraphQL.
  Take `node_id` from the `GET` above, then:

```bash
jq -n --arg id "{node_id}" \
  '{query: "mutation($id: ID!) { markPullRequestReadyForReview(input: {pullRequestId: $id}) { pullRequest { isDraft } } }", variables: {id: $id}}' |
  curl -s --netrc -X POST https://api.github.com/graphql -d @-
```

## Avoid repeated permission prompts

Suggest the user allow the script in their user settings (`~/.claude/settings.json`),
since the script is installed under `~/.claude/skills`:

```json
"Bash(~/.claude/skills/github-api-fallback-for-gh/create_pr.sh *)"
```
