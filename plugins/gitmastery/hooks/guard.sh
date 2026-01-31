#!/bin/bash
# Guard script - fast filter for PreToolUse hooks
# Exits 0 immediately for irrelevant commands, routes matched commands to handlers
#
# PATTERN FORMAT:
#   Each pattern is a grep -E regex matched against the command
#   Add patterns to PATTERNS array, handlers to HANDLERS array (same index)
#
# ADDING NEW PATTERNS:
#   1. Add regex to PATTERNS array
#   2. Add handler script path to HANDLERS array (same position)
#   3. Handler receives full JSON input via stdin

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ============================================================================
# PATTERN CONFIGURATION
# Add patterns here - matched top-to-bottom, first match wins
# ============================================================================

PATTERNS=(
    "^git add"
    "^git commit"
)

HANDLERS=(
    "${SCRIPT_DIR}/handlers/git_add.py"
    "${SCRIPT_DIR}/handlers/git_commit.py"
)

# ============================================================================
# GUARD LOGIC - No changes needed below
# ============================================================================

# Read input once
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Empty command - allow
[[ -z "$CMD" ]] && exit 0

# Check patterns
for i in "${!PATTERNS[@]}"; do
    if echo "$CMD" | grep -qE "${PATTERNS[$i]}"; then
        HANDLER="${HANDLERS[$i]}"

        # Check handler exists
        if [[ ! -x "$HANDLER" ]]; then
            echo "Handler not found or not executable: $HANDLER" >&2
            exit 1
        fi

        # Route to handler
        echo "$INPUT" | python3 "$HANDLER"
        exit $?
    fi
done

# No pattern matched - allow command
exit 0
