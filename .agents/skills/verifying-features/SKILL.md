---
name: verifying-features
description: Verifies a completed feature end-to-end against its North Star through executable system behavior, driving a real entry point and collecting evidence with a bundled driver script. Use when a feature is code-complete and needs acceptance verification.
---

# Verifying Features

Verify completed end-to-end features against the North Star through executable system
behavior. A feature is not complete because its code compiles or its unit tests pass —
it is complete when the system can be exercised through an external entry point and its
behavior matches the North Star. The full-text source lives in
[docs/verification.md](../../../docs/verification.md).

Verification must prove that the integrated feature:

- Behaves as intended
- Preserves invariants
- Handles expected failure paths
- Works through a real controller or client boundary
- Produces observable evidence of correctness

## Inputs

Before verification begins, review: the North Star, Epic context, Step requirements,
acceptance criteria, the architecture contract, and existing tests and system
interfaces. Extract the behavior that must be demonstrated. Do not infer success from
implementation structure alone.

## Required plan (before building the verification system)

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

## 1. Define the Verification Model

Identify feature entry points, external systems, required inputs, expected outputs,
state transitions, invariants, failure paths, and observable side effects. Produce a
verification matrix:

```text
Scenario:
Input:
External conditions:
Expected output:
Expected state change:
Invariant exercised:
Failure behavior:
```

Every North Star acceptance criterion and critical invariant MUST map to at least one
executable scenario. Critical invariants SHOULD be exercised through both valid and
invalid paths.

## 2. Prepare External Boundaries

For each external dependency (databases, third-party APIs, message brokers,
filesystems, email providers, payment gateways, time, randomness, authentication
providers), choose a mock, a fake, a local emulator, a disposable real instance, or a
controlled test environment. Use the lightest boundary implementation that still proves
the required behavior.

- **Mocks** — exact interaction behavior, failure responses, timeouts, retries, rare
  external conditions, deterministic branching.
- **Fakes** — stateful workflows, repository behavior, repeated interactions,
  realistic feature paths, multiple scenarios without external infrastructure.
- **Real integrations** — behavior that depends on database semantics, serialization
  compatibility, network protocols, SDK behavior, transactions, external system
  contracts.

Do not mock the behavior being verified. External test implementations MUST preserve
the behavioral contract of their Ports.

## 3. Build Test Data

Create deterministic data that exercises the full feature: standard valid input,
boundary values, invalid input, missing data, conflicting state, duplicate requests,
external failures, retry conditions, permission failures, and invariant violations.

Test data MUST be repeatable, isolated, easy to understand, easy to reset, and
explicitly connected to a verification scenario. Avoid random data unless the random
seed is fixed and recorded.

## 4. Select the System Entry Point

Exercise the feature through the highest practical external boundary — the interface an
actual consumer uses:

```text
HTTP API -> scripted HTTP requests
CLI      -> command execution
SPA      -> Playwright
Worker   -> controlled event publication
Job      -> explicit job invocation
```

Do not bypass the Controller by invoking Services directly for end-to-end verification.
Service-level tests support verification but do not replace it.

## 5. Build the Verification Driver

Create an executable driver that operates the selected entry point. Start from the
bundled skeleton — copy [scripts/verify.sh](scripts/verify.sh) into the repository
(e.g. `verification/verify.sh`) and adapt its setup, scenarios, and assertions to the
feature.

The driver MUST prepare required state, supply deterministic inputs, exercise each
scenario, capture outputs and relevant side effects, report failures clearly, return a
failing exit status when expectations are not met, and be repeatable without manual
intervention. The driver SHOULD live with the repository and remain reusable. Manual
verification alone is insufficient for repeatable feature acceptance.

## 6. Execute and Collect Evidence

Run the complete system with the selected boundary implementations. For each scenario,
collect: input, output, exit or response status, relevant persisted state, emitted
events, external interactions, logs required to explain behavior, and screenshots when
verifying visual clients.

Evidence MUST be sufficient to determine whether the North Star behavior occurred. Logs
alone are not proof unless the expected behavior is itself log output. Prefer
assertions against externally observable behavior and durable state over internal
calls, logs, or implementation details.

## 7. Evaluate Against the North Star

Compare observed behavior directly against expected behavior, acceptance criteria,
invariants, constraints, failure semantics, and non-goals. Classify each scenario as
`PASS`, `FAIL`, `BLOCKED`, or `NOT TESTED`. A scenario MUST NOT be marked complete
without executable evidence.

When behavior differs from the North Star, determine whether the implementation, the
test environment, the driver, or the North Star itself is at fault. Do not silently
redefine expected behavior to match the implementation.

## 8. Adjust and Repeat

For every failure:

1. Identify the root cause.
2. Correct the implementation, test environment, data, or driver.
3. Rerun the failed scenario.
4. Rerun affected neighboring scenarios.
5. Rerun the full verification suite when changes may have broader impact.

Repeat until all required scenarios pass. A fix is incomplete if it only changes the
observed symptom without preserving the North Star invariants.

## Scope

End-to-end verification MUST cover the primary success path, important alternate paths,
critical validation failures, external dependency failures, state transitions, declared
invariants, observable side effects, relevant authorization boundaries, and idempotency
or retry behavior when required. Prioritize business risk over exhaustive input
combinations. Unit and integration tests provide depth; end-to-end verification
provides confidence that the complete system works through its real boundaries.

## Required Verification Report

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

The final result MUST be one of `VERIFIED`, `NOT VERIFIED`, `PARTIALLY VERIFIED`, or
`BLOCKED`. `VERIFIED` requires all mandatory North Star criteria and critical
invariants to pass.

## Governing principle

Verification must operate the system, not merely inspect it. Use controlled external
boundaries, deterministic data, and executable drivers to prove that observable
behavior matches the North Star. Build. Exercise. Observe. Compare. Correct. Repeat.
