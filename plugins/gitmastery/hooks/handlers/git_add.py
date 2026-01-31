#!/usr/bin/env python3
"""Git add validator - blocks wildcards and current directory staging.

Exit codes:
    0 - Allow command
    2 - Block command (stderr shown to model)
"""

import json
import re
import sys


def validate_git_add(command: str) -> tuple[bool, str]:
    """Validate git add command for explicit file paths.

    Args:
        command: The git add command string

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Extract arguments after 'git add'
    match = re.match(r"^git\s+add\s+(.*)$", command, re.IGNORECASE)
    if not match:
        return True, ""

    args = match.group(1).strip()

    # Allow flags without files (--help, --dry-run, etc.)
    if not args or args.startswith("-"):
        return True, ""

    # Split into tokens, respecting quotes
    tokens = re.findall(r'(?:[^\s"]+|"[^"]*")+', args)

    blocked_patterns = [
        (".", "current directory"),
        ("..", "parent directory"),
        ("*", "wildcard"),
        ("-A", "all files flag"),
        ("--all", "all files flag"),
    ]

    for token in tokens:
        # Skip flags
        if token.startswith("-"):
            continue

        # Check blocked patterns
        for pattern, description in blocked_patterns:
            if token == pattern or (pattern == "*" and "*" in token):
                return (
                    False,
                    f"'{token}' ({description}) not allowed. List files explicitly.",
                )

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
