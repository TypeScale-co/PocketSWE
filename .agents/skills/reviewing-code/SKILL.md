---
name: reviewing-code
description: Coordinates independent code investigations across correctness, architecture, testing, and security before implementation proceeds.
---

# Reviewing Code

Use this skill to review a code change before integration or before closing a feature.

Code review is implementation analysis. It is not end-to-end verification.

Read [docs/code-review.md](../../../docs/code-review.md) and follow it directly. It is the single source of truth for:

-   The execution model (Review Coordinator and independent Reviewers)
-   The review schedule: which Reviewers run for a step and for the integrated feature
-   The four Reviewer roles: Correctness, Architecture, Test, Security
-   Reviewer responsibilities and constraints
-   Required output format and severity definitions
-   Consolidation rules and final result criteria

The Security Reviewer judges against [docs/security.md](../../../docs/security.md).
