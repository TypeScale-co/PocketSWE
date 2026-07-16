---
name: planning-work
description: Turns a feature request into a North Star, implementation plan, decomposition, and dependency graph, then coordinates execution through integration and close. Use before starting implementation of a feature or epic.
---

# Planning Work

Follow this seven-step protocol for every feature or epic. The full-text source lives
in [docs/work-protocol.md](../../../docs/work-protocol.md).

## 1. Discover

Gather information until the feature intent is unambiguous.

Produce a North Star describing:

- Goal
- Expected behavior
- Domain concepts
- Invariants
- Constraints
- Non-goals
- Acceptance criteria

Do not begin implementation until the North Star is complete.

## 2. Architect

Translate the North Star into an implementation plan.

Identify:

- Domain changes
- Services
- Ports
- Adapters
- Controllers
- Tests

Determine where each responsibility belongs according to the architecture contract
([docs/architecture.md](../../../docs/architecture.md)).

## 3. Decompose

Break the work into self-contained implementation steps.

Each step should:

- Have one clear responsibility
- Be independently reviewable
- Minimize overlap with other steps
- Expose a clear completion criterion

Each step contains its own requirements and acceptance criteria.

## 4. Build Dependency Graph

Identify dependencies between steps.

Mark each step as:

- Independent
- Depends on X
- Blocks Y

Maximize parallelism while preserving correctness.

## 5. Execute

Assign one agent per implementation step.

Each agent:

- Reviews the North Star
- Reviews the architecture contract
- Reviews the Epic context
- Reviews the Step context
- Plans against the current codebase
- Implements only its assigned step
- Adds appropriate tests
- Verifies completion

Agents should not modify unrelated steps.

## 6. Integrate & Review

Review every completed step against:

- North Star
- Step requirements
- Architecture contract
- Existing codebase
- Neighboring steps

Verify:

- Correctness
- Completeness
- Architectural compliance
- No duplicated work
- No conflicting implementations

Resolve integration issues before closing the Epic.

## 7. Close

Verify that:

- Every acceptance criterion is satisfied.
- All steps are complete.
- Tests pass.
- Architecture remains compliant.
- Documentation is updated if required.

The Epic is complete only when the integrated system satisfies the original North Star.
