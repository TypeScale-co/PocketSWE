---
name: reviewing-code
description: Coordinates independent code investigations across correctness, architecture, testing, and security before implementation proceeds.
---

# Reviewing Code

## Objective

Determine whether an implementation correctly and completely realizes its requirements while preserving the system's contracts.

Code review is implementation analysis.

It is not end-to-end verification.

---

# Execution Model

The agent invoking this skill is the **Review Coordinator**.

The Review Coordinator MUST NOT perform the primary review itself.

Instead, the Review Coordinator coordinates independent investigations performed by fresh-context sub-agents.

Every investigation defined in this document MUST be assigned to exactly one independent Reviewer.

Every Reviewer:

-   is a separate fresh-context sub-agent
-   receives the same review target
-   investigates only its assigned domain
-   performs its own repository investigation
-   MUST NOT see another Reviewer's findings
-   returns only its own findings

The Review Coordinator:

1. Defines the review target.
2. Launches the required Reviewers.
3. Collects Reviewer findings.
4. Removes duplicate findings.
5. Resolves contradictory findings.
6. Produces one consolidated review result.

Reviewer agreement is not evidence.

Evidence determines correctness.

---

# Review Target

The Review Coordinator provides:

-   implementation diff
-   North Star
-   requirements
-   Architecture Canon

Reviewers are responsible for gathering any additional repository context required to complete their investigation.

The diff is the starting point—not the boundary—of review.

---

# Reviewer Responsibilities

Every Reviewer MUST:

-   understand the requirements relevant to its investigation
-   inspect all necessary repository context
-   trace affected execution paths
-   validate findings before reporting them
-   report only concrete, consequential issues

Reviewers MUST NOT:

-   modify the implementation
-   speculate
-   report stylistic preferences as defects
-   investigate domains assigned to other Reviewers unless a discovered issue directly crosses domains

---

# Correctness Reviewer

**Ask:**

> **If this implementation were wrong, where would it fail?**

Determine whether the implementation is both **correct** and **complete**.

Inspect for issues including, but not limited to:

-   incorrect behavior
-   missing behavior
-   unnecessary behavior
-   regressions
-   bugs and logic errors
-   violated invariants
-   boundary-value errors
-   edge cases
-   invalid or missing input
-   incorrect error handling
-   partial failures
-   retry behavior
-   idempotency
-   ordering
-   concurrency
-   transaction boundaries
-   cleanup failures
-   compatibility breaks

Every finding MUST identify:

-   trigger
-   incorrect behavior
-   violated requirement or invariant
-   evidence

---

# Architecture Reviewer

**Ask:**

> **What architectural constraint does this implementation threaten?**

Determine whether the implementation preserves the Architecture Canon.

Inspect for issues including, but not limited to:

-   dependency violations
-   misplaced responsibilities
-   incorrect ownership
-   bypassed Ports
-   leaking external types
-   unnecessary coupling
-   fragmented cohesion
-   circular dependencies
-   unnecessary abstractions
-   pass-through wrappers
-   unclear utilities
-   disproportionate complexity
-   violations of the Architecture Canon

Every finding MUST identify either:

-   the violated canonical rule

or

-   the concrete architectural harm introduced.

---

# Test Reviewer

**Ask:**

> **If this implementation broke tomorrow, would the current tests catch it?**

Determine whether the implementation is sufficiently proven by its tests.

Ask:

-   Do the tests prove the required behavior?
-   Would they detect regressions?
-   Can they fail when the implementation is wrong?

Inspect for issues including, but not limited to:

-   missing requirement coverage
-   missing regression coverage
-   missing edge cases
-   missing failure scenarios
-   weak assertions
-   tautological tests
-   tests that duplicate implementation logic
-   tests that cannot fail meaningfully
-   incorrect mocks
-   mocks that hide defects
-   weakened or bypassed tests
-   missing integration coverage

Passing tests are evidence.

Passing tests are not proof.

Every finding MUST identify the behavior that remains unproven.

---

# Security Reviewer

**Ask:**

> **Can an untrusted actor make the system behave in an unintended way?**

Launch this Reviewer whenever the implementation changes:

-   trust boundaries
-   authentication
-   authorization
-   externally controlled input
-   sensitive data
-   secrets
-   isolation
-   resource limits

Inspect for issues including, but not limited to:

-   authentication bypass
-   authorization bypass
-   injection
-   unsafe deserialization
-   path traversal
-   sensitive-data exposure
-   unsafe logging
-   privilege escalation
-   replay
-   race conditions
-   denial of service
-   unsafe defaults

Every finding MUST identify a credible trigger-to-impact path.

Do not report hypothetical vulnerabilities.

---

# Reviewer Output

Every Reviewer returns:

```text
Reviewer:

Confidence:
High | Medium | Low

Findings:

- Title:
  Severity:
  Location:
  Trigger:
  Problem:
  Impact:
  Evidence:
  Recommendation:

Unresolved Questions:

Summary:
```

If no findings exist:

```text
Findings: None
```

Reviewers MUST NOT assign PASS, REVISE, or ESCALATE.

Only the Review Coordinator produces the final review result.

---

# Severity

## BLOCKING

A demonstrated defect preventing progression, including:

-   unmet requirement
-   regression
-   correctness defect
-   violated invariant
-   violated contract
-   concrete vulnerability
-   materially harmful architectural violation
-   insufficient tests for critical changed behavior

---

## WARNING

A demonstrated non-blocking weakness or engineering risk.

---

## NOTE

A useful optional improvement.

Do not invent findings.

Do not inflate severity.

---

# Consolidation

The Review Coordinator evaluates findings by evidence.

The Review Coordinator MUST:

-   merge duplicate findings
-   reject unsupported findings
-   reconcile contradictory findings
-   preserve the strongest accurate finding

When conflicting evidence cannot be resolved, launch another fresh-context Reviewer focused on the disputed issue.

Do not resolve disagreements by majority vote.

---

# Final Result

Produce one of:

## PASS

No blocking findings remain.

---

## REVISE

Blocking findings exist and can be corrected.

---

## ESCALATE

Correctness cannot be determined because requirements, architecture, or expected behavior require clarification.

PASS permits the implementation to proceed.

It does not certify end-to-end correctness.

---

# Governing Principle

Independent Reviewers investigate the implementation from different engineering perspectives.

The Review Coordinator consolidates those independent investigations into one evidence-based decision.
