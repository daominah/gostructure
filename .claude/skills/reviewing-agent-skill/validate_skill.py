"""Validate a SKILL.md file against mechanical checklist rules.

Usage: python3 validate_skill.py path/to/SKILL.md

Dependencies (optional): PyYAML (pip install pyyaml) for strict YAML validation.
Falls back to heuristic checks when PyYAML is not installed.
"""

import re
import sys

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def _is_yaml_quoted(value: str) -> bool:
    """Check if a YAML value is wrapped in quotes (single or double).

    Does not handle YAML escaped quotes (e.g. 'it''s a value')
    or multi-line folded values. Sufficient for single-line descriptions.
    """
    stripped = value.strip()
    if len(stripped) < 2:
        return False
    return (
        (stripped[0] == "'" and stripped[-1] == "'")
        or (stripped[0] == '"' and stripped[-1] == '"')
    )


def extract_frontmatter(lines: list[str]) -> tuple[dict[str, str], list[str], int]:
    """Return (frontmatter key-values, yaml_errors, body start line index)."""
    if not lines or lines[0].strip() != "---":
        return {}, [], 0
    end = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = i
            break
    if end is None:
        return {}, [], 0

    fm_text = "\n".join(lines[1:end])
    yaml_errors: list[str] = []

    # Try strict YAML parsing first
    if HAS_YAML:
        try:
            parsed = yaml.safe_load(fm_text)
            if isinstance(parsed, dict):
                fm = {k: str(v) for k, v in parsed.items() if v is not None}
                return fm, [], end + 1
        except yaml.YAMLError as exc:
            yaml_errors.append(f"YAML parse error in frontmatter: {exc}")

    # Fallback: naive regex extraction + heuristic checks
    fm: dict[str, str] = {}
    for line in lines[1:end]:
        m = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if m:
            key, value = m.group(1), m.group(2)
            fm[key] = value
            # Only run heuristic when strict parsing did not already report an error
            if not yaml_errors and not _is_yaml_quoted(value) and re.search(r":\s", value):
                yaml_errors.append(
                    f"'{key}' value contains ': ' (colon-space) without quoting. "
                    f"YAML parsers will misinterpret this as a nested mapping. "
                    f"Wrap the value in single quotes."
                )

    return fm, yaml_errors, end + 1


def validate(path: str) -> list[str]:
    errors: list[str] = []

    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return [f"File not found: {path}"]

    raw_lines = [line.rstrip("\n") for line in lines]
    fm, yaml_errors, body_start = extract_frontmatter(raw_lines)
    errors.extend(yaml_errors)

    if not fm:
        errors.append("Missing YAML frontmatter (expected --- delimiters)")
        return errors

    # -- name --
    name = fm.get("name", "")
    if not name:
        errors.append("Missing 'name' field in frontmatter")
    else:
        if len(name) > 64:
            errors.append(f"name exceeds 64 characters (got {len(name)})")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            errors.append(
                f"name contains invalid characters or has "
                f"leading/trailing/consecutive hyphens: '{name}'"
            )
        if re.search(r"anthropic|claude", name, re.IGNORECASE):
            errors.append(
                f"name contains reserved word ('anthropic' or 'claude'): '{name}'"
            )

    # -- description --
    desc = fm.get("description", "")
    if not desc:
        errors.append("Missing 'description' field in frontmatter")
    else:
        if len(desc) > 1024:
            errors.append(
                f"description exceeds 1024 characters (got {len(desc)})"
            )
        if desc.startswith(">") or desc.startswith("|"):
            errors.append(
                "description uses multi-line YAML syntax (>- or |), "
                "should be a single line"
            )
        # Overlapping trigger clauses
        desc_lower = desc.lower()
        has_use_when = "use when" in desc_lower
        has_trigger_on = bool(re.search(r"\btrigger\s*(on|when|if)\b", desc_lower))
        if has_use_when and has_trigger_on:
            errors.append(
                "description has overlapping trigger clauses "
                "('Use when' and 'Trigger on'). "
                "Merge the useful keywords into a single 'Use when' clause."
            )

    # -- body line count --
    body_lines = len(raw_lines) - body_start
    if body_lines > 500:
        errors.append(f"Body exceeds 500 lines (got {body_lines})")

    # -- no backslash paths (skip fenced code blocks) --
    in_code_block = False
    for i, line in enumerate(raw_lines, start=1):
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if "\\" in line:
            errors.append(f"Possible Windows-style backslash path on line {i}")

    return errors


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path-to-SKILL.md>", file=sys.stderr)
        sys.exit(2)

    path = sys.argv[1]
    errors = validate(path)

    if not errors:
        print(f"PASS: all mechanical checks passed for {path}")
        sys.exit(0)
    else:
        print(f"FAIL: {len(errors)} issue(s) found in {path}")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
