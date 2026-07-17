---
name: building-features
description: Builds and extends features using the onion/ports-and-adapters architecture — inside-out construction, a required pre-implementation plan, and a completion audit. Use when implementing a new feature or changing application structure.
---

# Building Features

Use this skill when implementing a new feature or changing application structure. Work
proceeds from the inside outward — Domain first, transport and vendors last — with a
required plan before implementation and a completion audit before completing the change.

Read [docs/architecture.md](../../../docs/architecture.md) and follow it directly. It is
the single source of truth for:

- The mandatory dependency rules for Domain, Services, Services.Ports, Repositories,
  Adapters, Controller, and Utilities
- The Feature Construction Procedure
- The Complexity Controls (prohibited patterns)
- The Required Agent Plan, produced before implementation
- The Required Completion Audit, verified before completing the change

Apply its MUST / SHOULD / MAY requirements exactly as written.
