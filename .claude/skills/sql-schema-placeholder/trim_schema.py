#!/usr/bin/env python3
"""Trim useless info from a pg_dump --schema-only output to save AI context.

Giving the AI the database schema helps it generate correct queries,
but the raw dump carries a lot of noise the AI does not need.
This keeps the structure that matters (tables, indexes, constraints, and the like)
and drops the rest.

Removes: pg_dump header/footer, SET statements, RDS admin functions,
OWNER TO lines, ACL/GRANT blocks, and psql \\restrict / \\unrestrict directives.

Usage:
    python3 trim_schema.py raw.sql > schema.sql
"""

import re
import sys


def trim_schema(lines: list[str]) -> list[str]:
    out = [
        "-- placeholder PostgreSQL schema\n",
        "-- Schema structure (privileges, RDS functions, and pg_dump noise removed)\n",
        "\n",
    ]

    skip_function = False  # inside an rdsAdmin function block
    function_saw_end = False
    skip_acl = False  # inside an ACL comment block

    for line in lines:
        stripped = line.strip()

        # --- Skip pg_dump header/footer ---
        if stripped.startswith("-- Dumped from database version"):
            continue
        if stripped.startswith("-- Dumped by pg_dump version"):
            continue
        if stripped.startswith("-- PostgreSQL database dump"):
            continue

        # --- Skip psql \restrict / \unrestrict directives ---
        if stripped.startswith(("\\restrict", "\\unrestrict")):
            continue

        # --- Skip SET / SELECT pg_catalog at the top ---
        if stripped.startswith("SET "):
            continue
        if stripped.startswith("SELECT pg_catalog.set_config"):
            continue

        # --- Skip schema-level DDL ---
        if stripped.startswith(("CREATE SCHEMA", "ALTER SCHEMA", "COMMENT ON SCHEMA")):
            continue

        # --- Skip RDS admin function blocks (multi-line) ---
        if re.match(r"^-- Name:.*Type: FUNCTION.*Owner: rdsAdmin", stripped):
            skip_function = True
            function_saw_end = False
            continue

        if skip_function:
            if stripped == "" and function_saw_end:
                skip_function = False
                function_saw_end = False
            if stripped.endswith("$$;") or re.match(r"^ALTER FUNCTION.*OWNER TO", stripped):
                function_saw_end = True
            continue

        # --- Skip OWNER TO lines ---
        if re.match(r"^ALTER .* OWNER TO ", stripped):
            continue

        # --- Skip ACL blocks ---
        if re.match(r"^-- Name:.*Type: ACL", stripped):
            skip_acl = True
            continue

        if skip_acl:
            if re.match(r"^-- Name:", stripped) and "Type: ACL" not in stripped:
                skip_acl = False
            else:
                continue

        # --- Skip GRANT / REVOKE / ALTER DEFAULT PRIVILEGES ---
        if stripped.startswith(("GRANT ", "REVOKE ", "ALTER DEFAULT PRIVILEGES")):
            continue

        out.append(line)

    return out


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 trim_schema.py <input.sql>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        lines = f.readlines()

    for line in trim_schema(lines):
        sys.stdout.write(line)


if __name__ == "__main__":
    main()
