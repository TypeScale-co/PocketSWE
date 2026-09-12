---
name: reviewing-code
description: Coordinates independent code investigations across correctness, architecture, testing, and security before implementation proceeds.
---

# Reviewing Code

Use this skill to review a code change before integration or before closing a feature.

Code review is implementation analysis. It is not end-to-end verification.

Read [docs/code-review.md](../../../docs/code-review.md) and follow it directly. It is the single source of truth for:

-   The execution model (one step Correctness Reviewer, optional additive specialist
    escalation, and the full independent integration board)
-   The four Reviewer roles: Correctness, Architecture, Test, Security
-   Reviewer responsibilities and constraints
-   Required output format and severity definitions
-   Consolidation rules and final result criteria

For ordinary steps, run exactly one Correctness Review. The Epic Orchestrator may
add Architecture, Test, and/or Security Reviewers when a step is exceptional in
that dimension; these specialists never replace the Correctness Review. At
integration, run the complete Correctness, Architecture, Test, and Security board.
The Security Reviewer judges against [docs/security.md](../../../docs/security.md)
as well as the general review contract.
