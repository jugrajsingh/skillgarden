#!/usr/bin/env python3
"""Git add validator - enforces explicit file paths only.

Blocks directories, wildcards, and bulk-add flags.
Uses pathlib for reliable filesystem checks.

Exit codes:
    0 - Allow command
    2 - Block command (stderr shown to model)
"""

import json
import re
import sys
from pathlib import Path

BLOCKED_FLAGS = {"-A", "--all", "-u", "--update"}


def validate_git_add(command: str) -> tuple[bool, str]:
    """Validate git add command for explicit file paths.

    Args:
        command: The git add command string.

    Returns:
        Tuple of (is_valid, error_message).
    """
    match = re.match(r"^git\s+add\s+(.*)$", command, re.IGNORECASE)
    if not match:
        return True, ""

    args = match.group(1).strip()
    if not args:
        return True, ""

    tokens = re.findall(r'(?:[^\s"]+|"[^"]*")+', args)

    for token in tokens:
        # Block bulk-add flags
        if token in BLOCKED_FLAGS:
            return False, f"'{token}' stages too broadly. List files explicitly."

        # Skip other flags (--force, -p, etc.)
        if token.startswith("-"):
            continue

        # Block wildcards/globs
        if "*" in token or "?" in token:
            return False, f"'{token}' contains a glob. List files explicitly."

        # Block directories — this catches '.', '..', 'src/', 'tests/unit', etc.
        path = Path(token)
        if path.is_dir():
            return False, f"'{token}' is a directory. List files explicitly."

    return True, ""


def main() -> int:
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}", file=sys.stderr)
        return 1

    command = input_data.get("tool_input", {}).get("command", "")

    is_valid, error = validate_git_add(command)

    if not is_valid:
        print(f"Git Add Blocked: {error}", file=sys.stderr)
        print("Use 'git status' to see changed files.", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
