#!/bin/bash
#
# Iron Fist: Pre-commit gate hook for PocketSWE
#
# This hook runs BEFORE any git commit command is allowed.
# It checks that the PocketSWE work protocol has been followed.
#
# Exit 0 = allow
# Exit non-zero = block with error message
#

set -e

# Find project root
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$PROJECT_ROOT"

# Check for active work that hasn't been completed
WORK_CURRENT="$PROJECT_ROOT/work/current"
if [ -d "$WORK_CURRENT" ]; then
    ACTIVE_WORK=$(find "$WORK_CURRENT" -name "*.yaml" -o -name "*.yml" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$ACTIVE_WORK" -gt 0 ]; then
        echo "================================================================" >&2
        echo "IRON FIST: COMMIT BLOCKED" >&2
        echo "================================================================" >&2
        echo "" >&2
        echo "There are $ACTIVE_WORK active work record(s) in work/current/" >&2
        echo "" >&2
        echo "You MUST call complete_work() before committing." >&2
        echo "Work records must be archived to work/archive/ first." >&2
        echo "" >&2
        echo "Before calling complete_work(), ensure:" >&2
        echo "  1. Code review completed (/reviewing-code skill)" >&2
        echo "  2. Verification completed (/verifying-features skill)" >&2
        echo "  3. All BLOCKING findings resolved" >&2
        echo "" >&2
        echo "Active work:" >&2
        ls -1 "$WORK_CURRENT"/*.yaml "$WORK_CURRENT"/*.yml 2>/dev/null | head -5 >&2
        echo "" >&2
        echo "To complete work:" >&2
        echo "  from pocketswe import complete_work" >&2
        echo "  complete_work(work_id='<work_id>')" >&2
        echo "================================================================" >&2
        exit 1
    fi
fi

# All checks passed
exit 0
