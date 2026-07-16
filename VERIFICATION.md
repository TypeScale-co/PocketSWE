# Agent Verification Contract

## Objective

Verify completed end-to-end features against the North Star through executable system behavior.

Verification must prove that the integrated feature:

- Behaves as intended
- Preserves invariants
- Handles expected failure paths
- Works through a real controller or client boundary
- Produces observable evidence of correctness

A feature is not complete because its code compiles or its unit tests pass.

It is complete when the system can be exercised through an external entry point and its behavior matches the North Star.

---

# Verification Inputs

Before verification begins, review:

- The North Star
- Epic context
- Step requirements
- Acceptance criteria
- Architecture Manifest
- Existing tests and system interfaces

Extract the behavior that must be demonstrated.

Do not infer success from implementation structure alone.

---

# 1. Define the Verification Model

Identify:

- Feature entry points
- External systems
- Required inputs
- Expected outputs
- State transitions
- Invariants
- Failure paths
- Observable side effects

Produce a verification matrix:

```text
Scenario:
Input:
External conditions:
Expected output:
Expected state change:
Invariant exercised:
Failure behavior:
```

Every North Star acceptance criterion and critical invariant MUST map to at least one executable scenario.

Critical invariants SHOULD be exercised through both valid and invalid paths.

---

# 2. Prepare External Boundaries

Identify all external dependencies involved in the feature.

Examples:

- Databases
- Third-party APIs
- Message brokers
- Filesystems
- Email providers
- Payment gateways
- Time
- Randomness
- Authentication providers
- External services

For each dependency, determine whether verification should use:

- A mock
- A fake
- A local emulator
- A disposable real instance
- A controlled test environment

Use the lightest boundary implementation that still proves the required behavior.

## Mocks

Use mocks when verifying:

- Exact interaction behavior
- Failure responses
- Timeouts
- Retries
- Rare external conditions
- Deterministic branching

## Fakes

Use fakes when verifying:

- Stateful workflows
- Repository behavior
- Repeated interactions
- Realistic feature paths
- Multiple scenarios without external infrastructure

## Real integrations

Use targeted real integrations when behavior depends on:

- Database semantics
- Serialization compatibility
- Network protocols
- SDK behavior
- Transactions
- External system contracts

Do not mock the behavior being verified.

External test implementations MUST preserve the behavioral contract of their Ports.

---

# 3. Build Test Data

Create deterministic data that exercises the full feature.

Test data SHOULD include:

- Standard valid input
- Boundary values
- Invalid input
- Missing data
- Conflicting state
- Duplicate requests
- External failures
- Retry conditions
- Permission failures
- Invariant violations

Test data MUST be:

- Repeatable
- Isolated
- Easy to understand
- Easy to reset
- Explicitly connected to a verification scenario

Avoid random data unless the random seed is fixed and recorded.

---

# 4. Select the System Entry Point

Exercise the feature through the highest practical external boundary.

Examples:

```text
HTTP API
CLI
Web SPA
Mobile client
Scheduled job
Event consumer
Worker
```

Prefer verifying through the interface an actual consumer uses.

Examples:

```text
HTTP API -> scripted HTTP requests
CLI      -> command execution
SPA      -> Playwright
Worker   -> controlled event publication
Job      -> explicit job invocation
```

Do not bypass the Controller by invoking Services directly for end-to-end verification.

Service-level tests support verification but do not replace it.

---

# 5. Build the Verification Driver

Create an executable driver that operates the selected entry point.

Examples:

- Shell script using `curl`
- API test script
- CLI harness
- Playwright test
- Event producer
- Worker runner
- Scenario test executable

The driver MUST:

- Prepare required state
- Supply deterministic inputs
- Exercise each scenario
- Capture outputs
- Capture relevant side effects
- Report failures clearly
- Return a failing exit status when expectations are not met
- Be repeatable without manual intervention

The driver SHOULD live with the repository and remain reusable.

Manual verification alone is insufficient for repeatable feature acceptance.

---

# 6. Execute and Collect Evidence

Run the complete system with the selected mocks, fakes, emulators, or controlled integrations.

For each scenario, collect:

- Input
- Output
- Exit status or response status
- Relevant persisted state
- Emitted events
- External interactions
- Logs required to explain behavior
- Screenshots when verifying visual clients

Evidence MUST be sufficient to determine whether the North Star behavior occurred.

Logs alone are not proof unless the expected behavior is itself log output.

Prefer assertions against externally observable behavior and durable state over internal calls, logs, or implementation details.

---

# 7. Evaluate Against the North Star

Compare observed behavior directly against:

- Expected behavior
- Acceptance criteria
- Invariants
- Constraints
- Failure semantics
- Non-goals

Classify each scenario:

```text
PASS
FAIL
BLOCKED
NOT TESTED
```

A scenario MUST NOT be marked complete without executable evidence.

When behavior differs from the North Star, determine whether:

- The implementation is incorrect
- The test environment is incorrect
- The driver is incorrect
- The North Star is ambiguous or outdated

Do not silently redefine expected behavior to match the implementation.

---

# 8. Adjust and Repeat

For every failure:

1. Identify the root cause.
2. Correct the implementation, test environment, data, or driver.
3. Rerun the failed scenario.
4. Rerun affected neighboring scenarios.
5. Rerun the full verification suite when changes may have broader impact.

Repeat until all required scenarios pass.

A fix is incomplete if it only changes the observed symptom without preserving the North Star invariants.

---

# Verification Scope

End-to-end verification MUST cover:

- Primary success path
- Important alternate paths
- Critical validation failures
- External dependency failures
- State transitions
- Declared invariants
- Observable side effects
- Relevant authorization boundaries
- Idempotency or retry behavior when required

Verification SHOULD prioritize business risk over exhaustive input combinations.

Unit and integration tests provide depth.

End-to-end verification provides confidence that the complete system works through its real boundaries.

---

# Required Agent Plan

Before building the verification system, produce:

```text
North Star behaviors:
Entry point:
External dependencies:
Mocks:
Fakes:
Real integrations:
Test data:
Scenarios:
Driver:
Evidence:
```

Use `None` where appropriate.

---

# Required Verification Report

Complete verification with:

```text
Feature:
Entry point:
Environment:
External boundaries:
Driver:

Scenarios:
- Scenario:
  Result:
  Evidence:

North Star criteria:
- Criterion:
  Result:

Adjustments made:
Remaining gaps:
Final result:
```

The final result MUST be one of:

```text
VERIFIED
NOT VERIFIED
PARTIALLY VERIFIED
BLOCKED
```

`VERIFIED` requires all mandatory North Star criteria and critical invariants to pass.

---

# Governing Principle

Verification must operate the system, not merely inspect it.

Use controlled external boundaries, deterministic data, and executable drivers to prove that observable behavior matches the North Star.

Build.

Exercise.

Observe.

Compare.

Correct.

Repeat.
