# Customize ChatGPT and Copilot

Source of truth for coding conventions is `.claude/skills/`.
Run `copilot_from_skills.go` to regenerate `copilot_personalization.md`
from skills that contain only a `SKILL.md` file.
The script prints per-skill character counts to help trim if needed.

## GitHub Copilot

[./copilot_personalization.md](./copilot_personalization.md) is the repository-level
instructions file read automatically by Copilot.

To apply rules globally across all repositories in JetBrains IDEs,
go to `Settings` > `Tools` > `GitHub Copilot` > `Customizations` > `Global`
and paste the content there (or paste directly to file
`$HOME/AppData/Local/github-copilot/intellij/global-copilot-instructions.md`).

**Limit:** ~4000 characters before content may be truncated.

## ChatGPT

[./chatgpt_personalization.md](./chatgpt_personalization.md) contains instructions for ChatGPT.

To apply, go to `Settings` > `Personalization` > `Custom instructions`
and paste the content there.

**Limit:** 1500 characters.
