#!/bin/bash
# Creates a pull request through the GitHub REST API with credentials from ~/.netrc.
# Prints the pull request URL on success, the API error message on failure.
# Usage: create_pr.sh {owner}/{repo} {head_branch} {base_branch} {title} {body_file} [--draft]
set -euo pipefail

if [ $# -lt 5 ]; then
    echo "usage: $0 {owner}/{repo} {head_branch} {base_branch} {title} {body_file} [--draft]" >&2
    exit 2
fi
repo=$1 head=$2 base=$3 title=$4 body_file=$5
draft=false
if [ "${6:-}" = "--draft" ]; then draft=true; fi

if [ ! -f "$body_file" ]; then
    echo "body file not found: $body_file" >&2
    exit 2
fi
for tool in jq curl; do
    command -v "$tool" >/dev/null || { echo "missing dependency: $tool" >&2; exit 2; }
done

response=$(jq -n \
    --arg title "$title" --arg head "$head" --arg base "$base" \
    --rawfile body "$body_file" --argjson draft "$draft" \
    '{title: $title, head: $head, base: $base, body: $body, draft: $draft}' |
    curl -s --netrc -X POST \
        -H "Accept: application/vnd.github+json" \
        "https://api.github.com/repos/$repo/pulls" -d @-)

url=$(jq -r '.html_url // empty' <<<"$response")
if [ -z "$url" ]; then
    # 401 or 404 usually means a missing api.github.com entry in ~/.netrc or a token without access.
    jq -r '.message, (.errors // [] | .[] | tostring)' <<<"$response" >&2
    exit 1
fi
echo "$url"
