#!/bin/bash
# Git add validator - enforces explicit file paths only.
# Blocks directories, wildcards, and bulk-add flags.
#
# Input: git add command string as $1
# Exit codes: 0=allow, 2=block, 1=error

set -euo pipefail

CMD="$1"

# Extract args after "git add"
ARGS="${CMD#git add }"
[[ "$ARGS" == "$CMD" ]] && exit 0  # no match — not a git add
[[ -z "$ARGS" ]] && exit 0

# Tokenize (handles quoted paths)
eval set -- $ARGS 2>/dev/null || set -- $ARGS

for token in "$@"; do
    # Block bulk-add flags
    case "$token" in
        -A|--all|-u|--update)
            echo "Git Add Blocked: '$token' stages too broadly. List files explicitly." >&2
            echo "Use 'git status' to see changed files." >&2
            exit 2
            ;;
        -*) continue ;;  # skip other flags
    esac

    # Block wildcards/globs
    if [[ "$token" == *'*'* || "$token" == *'?'* ]]; then
        echo "Git Add Blocked: '$token' contains a glob. List files explicitly." >&2
        echo "Use 'git status' to see changed files." >&2
        exit 2
    fi

    # Block directories
    if [[ -d "$token" ]]; then
        echo "Git Add Blocked: '$token' is a directory. List files explicitly." >&2
        echo "Use 'git status' to see changed files." >&2
        exit 2
    fi
done

exit 0
