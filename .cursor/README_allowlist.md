# Cursor Agent Allowlists

Preemptively define allowlists to prevent Cursor agents from being blocked
during long tasks, such as implementing a new repository based on documentation,
while you are away from your computer.

## Command Allowlist

Go to Cursor settings UI and add the following commands one by one
(no config JSON supported):

`File` > `Preferences` > `Cursor Settings` > `Agents` > `Command AllowList`

```text
cat
cd
echo
git add
git diff
git log
git status
go
grep
head
make
sleep
tail
wc
```

## Fetch Domain Allowlist

Similarly, add the following domains one by one in the following section:

`File` > `Preferences` > `Cursor Settings` > `Agents` > `Fetch Domain AllowList`

```text
*.cursor.com
developers.facebook.com
*.github.com
*.go.dev
*.githubusercontent.com
*.google.com
open.shopee.com
stackoverflow.com
partner.tiktokshop.com
```
