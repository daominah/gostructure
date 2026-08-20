---
name: sql-schema-placeholder
description: Provides the PostgreSQL schema for "placeholder". Use when writing or fixing SQL queries, migrations, or investigating slow queries for the "placeholder" repo.
disable-model-invocation: true
---

# Placeholder Database SQL Skill

Use this skill to write or fix SQL queries for the PostgreSQL database in the "placeholder" repo.

## Schema

You MUST read the **entire** [schema.sql](schema.sql) file into your context,
do not rely on a preview or partial content,
to understand the database structure, indexes, and foreign keys
before writing or fixing SQL queries.

If `schema.sql` is missing or invalid, ask the user to regenerate it:

```bash
pg_dump --dbname=placeholder --schema-only --lock-wait-timeout=2s \
    --schema=public --username=placeholder --host=127.0.0.1 --port=5432 \
    --no-owner --no-privileges \
    --file=/tmp/placeholder_raw.sql \
  && python3 $HOME/.claude/skills/sql-schema-placeholder/trim_schema.py \
    /tmp/placeholder_raw.sql \
    > $HOME/.claude/skills/sql-schema-placeholder/schema.sql
```

The [trim_schema.py](trim_schema.py) script strips pg_dump noise the AI does not need,
keeping the schema structure that helps generate correct queries.

## Conventions

- When writing SQL, do not use table name aliases (short abbreviations).
  Use the name in the schema for clarity.
- Apply rules from the `sql-formatting` skill to the resulting SQL.
