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
#   3. Handler receives command string as $1 argument

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
    "${SCRIPT_DIR}/handlers/git_add.sh"
    "${SCRIPT_DIR}/handlers/git_commit.sh"
)

# ============================================================================
# GUARD LOGIC - No changes needed below
# ============================================================================

# Read input once
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Empty command - allow
[[ -z "$CMD" ]] && exit 0

# Split compound command on && || ; | into sub-commands
# Uses RS (0x1e) as delimiter to preserve newlines in quoted strings (multiline commits)
# Then strip leading env var assignments (VAR=val VAR2=val2 ...) from each
RS=$'\x1e'
SUBCMDS=()
split_and_clean() {
    local cmd="$1"
    # Replace shell operators with RS
    local parts
    parts=$(printf '%s' "$cmd" | sed -E "s/[[:space:]]*(&&|\|\||\||;)[[:space:]]*/${RS}/g")

    # Split on RS using IFS, preserving embedded newlines
    local old_ifs="$IFS"
    IFS="$RS"
    local segments
    read -r -d '' -a segments <<< "${parts}${RS}" || true
    IFS="$old_ifs"

    local seg
    for seg in "${segments[@]}"; do
        [[ -z "$seg" ]] && continue
        # Strip leading KEY=value assignments
        local cleaned="$seg"
        while [[ "$cleaned" =~ ^[A-Za-z_][A-Za-z0-9_]*=[^[:space:]]*[[:space:]]+(.*) ]]; do
            cleaned="${BASH_REMATCH[1]}"
        done
        [[ -n "$cleaned" ]] && SUBCMDS+=("$cleaned")
    done
}

# Quick check: does the full command contain any pattern keyword?
# If not, skip splitting entirely — fastest path for unrelated commands
has_match=false
for i in "${!PATTERNS[@]}"; do
    if echo "$CMD" | grep -qE "${PATTERNS[$i]}"; then
        has_match=true
        break
    fi
done
$has_match || exit 0

# At least one pattern matched somewhere — split and validate each sub-command
split_and_clean "$CMD"

for subcmd in "${SUBCMDS[@]}"; do
    [[ -z "$subcmd" ]] && continue

    for i in "${!PATTERNS[@]}"; do
        if echo "$subcmd" | grep -qE "${PATTERNS[$i]}"; then
            HANDLER="${HANDLERS[$i]}"

            # Check handler exists
            if [[ ! -x "$HANDLER" ]]; then
                echo "Handler not found or not executable: $HANDLER" >&2
                exit 1
            fi

            # Route to handler — block on first failure
            "$HANDLER" "$subcmd"
            rc=$?
            [[ $rc -ne 0 ]] && exit $rc

            # Pattern matched for this subcmd, skip remaining patterns
            break
        fi
    done
done

# All sub-commands passed - allow
exit 0
