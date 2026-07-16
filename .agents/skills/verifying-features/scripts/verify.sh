#!/usr/bin/env bash
#
# PocketSWE verification driver skeleton.
#
# Copy this file into the repository under verification (e.g. verification/verify.sh),
# then adapt setup, teardown, and the scenario list to the feature under verification.
#
# The driver contract (docs/verification.md, section 5):
#   - Prepare required state
#   - Supply deterministic inputs
#   - Exercise each scenario through the real entry point
#   - Capture outputs and relevant side effects as evidence
#   - Report failures clearly
#   - Return a failing exit status when expectations are not met
#   - Be repeatable without manual intervention
#
# Usage:
#   ./verify.sh                 run all scenarios
#   ./verify.sh <scenario>      run a single scenario by name

set -u

EVIDENCE_DIR="${EVIDENCE_DIR:-$(pwd)/verification-evidence}"
PASS_COUNT=0
FAIL_COUNT=0
FAILED_SCENARIOS=()
CURRENT_SCENARIO=""
CURRENT_FAILURES=0

# --- Framework -----------------------------------------------------------------

# begin_scenario <name> — start a scenario; evidence goes to $EVIDENCE_DIR/<name>/
begin_scenario() {
    CURRENT_SCENARIO="$1"
    CURRENT_FAILURES=0
    mkdir -p "$EVIDENCE_DIR/$CURRENT_SCENARIO"
    echo ""
    echo "=== Scenario: $CURRENT_SCENARIO"
}

# capture <label> <command...> — run a command, record stdout/stderr/exit status as evidence
capture() {
    local label="$1"; shift
    local dir="$EVIDENCE_DIR/$CURRENT_SCENARIO"
    "$@" >"$dir/$label.out" 2>"$dir/$label.err"
    echo "$?" >"$dir/$label.status"
    cat "$dir/$label.out"
}

# fail <message> — record an expectation failure for the current scenario
fail() {
    CURRENT_FAILURES=$((CURRENT_FAILURES + 1))
    echo "    FAIL: $1"
}

# assert_eq <expected> <actual> <description>
assert_eq() {
    if [ "$1" != "$2" ]; then
        fail "$3 (expected: '$1', actual: '$2')"
    fi
}

# assert_contains <needle> <haystack> <description>
assert_contains() {
    case "$2" in
        *"$1"*) ;;
        *) fail "$3 (missing: '$1')" ;;
    esac
}

# assert_status <expected-exit-code> <label> <description> — check a captured command's exit status
assert_status() {
    local actual
    actual="$(cat "$EVIDENCE_DIR/$CURRENT_SCENARIO/$2.status")"
    assert_eq "$1" "$actual" "$3"
}

# end_scenario — classify the scenario and update totals
end_scenario() {
    if [ "$CURRENT_FAILURES" -eq 0 ]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        echo "    PASS"
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        FAILED_SCENARIOS+=("$CURRENT_SCENARIO")
    fi
}

# --- Environment ---------------------------------------------------------------

# Prepare required state: start the system, reset storage, seed deterministic test
# data, configure mocks/fakes/emulators for each external boundary. Use fixed seeds
# and fixed clocks; verification must be repeatable.
setup() {
    : # TODO: implement
}

# Tear down whatever setup created so consecutive runs start clean.
teardown() {
    : # TODO: implement
}

# --- Scenarios -----------------------------------------------------------------
#
# One function per row of the verification matrix. Exercise the feature through its
# real entry point (scripted HTTP requests, CLI invocation, Playwright, event
# publication, job invocation) — do not call Services directly. Assert on externally
# observable behavior and durable state, not internal calls or logs.
#
# Example (HTTP API):
#
# scenario_create_customer_succeeds() {
#     begin_scenario "create_customer_succeeds"
#     local body
#     body="$(capture create-request \
#         curl -s -o /dev/stderr -w '%{http_code}' \
#         -X POST "$BASE_URL/customers" -d '{"name":"Ada"}')"
#     assert_eq "201" "$body" "create returns 201"
#     local stored
#     stored="$(capture db-state query_customer_by_name "Ada")"
#     assert_contains '"name":"Ada"' "$stored" "customer persisted"
#     end_scenario
# }

scenario_example() {
    begin_scenario "example"
    fail "no scenarios implemented yet — replace scenario_example with real scenarios"
    end_scenario
}

# List every scenario function here. Each North Star acceptance criterion and critical
# invariant must map to at least one scenario; exercise critical invariants through
# both valid and invalid paths.
SCENARIOS=(
    scenario_example
)

# --- Main ----------------------------------------------------------------------

main() {
    rm -rf "$EVIDENCE_DIR"
    mkdir -p "$EVIDENCE_DIR"

    setup
    trap teardown EXIT

    local only="${1:-}"
    for s in "${SCENARIOS[@]}"; do
        if [ -n "$only" ] && [ "$s" != "scenario_$only" ] && [ "$s" != "$only" ]; then
            continue
        fi
        "$s"
    done

    echo ""
    echo "=== Verification summary"
    echo "    Passed: $PASS_COUNT"
    echo "    Failed: $FAIL_COUNT"
    if [ "$FAIL_COUNT" -gt 0 ]; then
        for s in "${FAILED_SCENARIOS[@]}"; do
            echo "    FAILED: $s"
        done
        echo "    Evidence: $EVIDENCE_DIR"
        exit 1
    fi
    echo "    Evidence: $EVIDENCE_DIR"
}

main "$@"
