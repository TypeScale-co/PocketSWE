---
name: verifying-features
description: Verifies a completed feature end-to-end against its North Star through executable system behavior, driving a real entry point and collecting evidence. Use when a feature is code-complete and needs acceptance verification.
---

# Verifying Features

Use this skill when a feature is code-complete and needs acceptance verification. A
feature is not complete because its code compiles or its unit tests pass — it is
complete when the system can be exercised through an external entry point and its
behavior matches the North Star.

Read [docs/verification.md](../../../docs/verification.md) and follow it directly. It is
the single source of truth for:

- Verification inputs and the required pre-verification plan
- The eight-step procedure, from defining the verification model through adjust-and-repeat
- Verification scope and the required Verification Report

Build the verification driver to fit the feature's actual entry point — scripted HTTP
requests, a CLI harness, a Playwright test, an event producer, a job runner. Every
driver is feature-specific; the driver contract in the source document is the template.
