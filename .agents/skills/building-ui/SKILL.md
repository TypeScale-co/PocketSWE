---
name: building-ui
description: Builds browser-based user interfaces against the constrained UI stack — Next.js App Router, Tailwind, shadcn/ui — with rules for placement, data access, accessibility, API integration, and UI verification. Use when implementing or changing a web client.
---

# Building UI

Use this skill when implementing or changing a browser-based web client. A web client is a
`Clients` entry in the Architecture Canon: this skill governs its internals, while
[docs/architecture.md](../../../docs/architecture.md) governs its relationship to the
backend.

Read [docs/ui-architecture.md](../../../docs/ui-architecture.md) and follow it directly. It
is the single source of truth for:

- Client placement under `Clients` and the boundary with backend code
- The mandated stack: Next.js App Router, Tailwind, shadcn/ui, Lucide, next-themes
- Data access — Server Components own reads, mutations go through `services/`, and the
  narrow conditions under which a client-side server-state library is permitted
- The design system: semantic colors, type scale, spacing grid
- Accessibility requirements and the automated check in the end-to-end suite
- Directory layout, API integration, error handling, loading states, forms, and auth
- UI-specific verification, including Playwright coverage against the real backend
- The Required Agent Plan, produced before implementation
- The Required Completion Audit, verified before completing the change

Apply its MUST / SHOULD / MAY requirements exactly as written.

The client is part of the system under verification. Internal dependencies — your client to
your backend — are never mocked. See
[docs/verification.md](../../../docs/verification.md) for the full verification contract.
