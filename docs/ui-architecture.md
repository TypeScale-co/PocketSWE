# Agent UI Architecture Contract

This contract governs **browser-based user interface** construction. It defines the stack, patterns, and structure for building web clients that consume backend APIs.

For verification requirements, see `verification.md`. The UI is part of the system—not a separate application.

## Objective

Build accessible, maintainable web interfaces using a constrained set of tools and patterns.

UI clients must:

-   Consume backend APIs as their only data source
-   Render correctly across modern browsers
-   Support light and dark themes
-   Remain understandable as they grow
-   Work out of the box when delivered

---

# Stack

## Framework

**Next.js** with App Router.

-   Server Components for initial page loads
-   Client Components for interactive elements
-   File-based routing
-   TypeScript strict mode

Other frameworks introduce unnecessary divergence.

## Styling

**Tailwind CSS** for all styling.

-   Utility-first classes only
-   No CSS modules
-   No CSS-in-JS
-   No inline style objects
-   Custom design tokens via configuration

Tailwind provides consistency without runtime overhead.

## Components

**shadcn/ui** for component primitives.

-   Copy components into the project
-   Built on Radix primitives (accessibility handled)
-   Full source control for customization
-   No runtime component library dependency

Owning the component source prevents version lock-in and enables customization.

## Icons

**Lucide React** for iconography.

Consistent icon set with tree-shaking support.

## Theming

**next-themes** for dark mode.

-   System preference detection by default
-   Manual toggle available
-   CSS variables switch between palettes

---

# Design System

## Semantic Colors

Define colors by purpose, not by value:

```text
background / foreground
muted / muted-foreground
card / card-foreground
primary / primary-foreground
secondary / secondary-foreground
destructive / destructive-foreground
border / input / ring
```

Status colors follow a consistent pattern:

| Semantic | Meaning                  |
| -------- | ------------------------ |
| Neutral  | Default, draft, inactive |
| Blue     | Approved, informational  |
| Yellow   | In progress, warning     |
| Green    | Complete, success        |
| Orange   | Attention needed         |
| Red      | Error, destructive       |

## Typography

System font stack:

```text
Inter, system-ui, -apple-system, sans-serif
```

Type scale (base 14-16px):

| Purpose         | Relative Size               |
| --------------- | --------------------------- |
| Page title      | Large, semibold             |
| Section heading | Medium-large, medium weight |
| Card/item title | Base, medium weight         |
| Body text       | Base, normal weight         |
| Caption/helper  | Small, muted                |

## Spacing

4px base grid:

| Context      | Multiplier     |
| ------------ | -------------- |
| Inline/tight | 2x (8px)       |
| Form fields  | 4x (16px)      |
| Card padding | 6x (24px)      |
| Sections     | 6-8x (24-32px) |

Consistent spacing creates visual rhythm without effort.

---

# Structure

## Directory Layout

```text
app/                          # Routes and pages
├── layout.tsx                # Root layout
├── page.tsx                  # Entry point
├── (public)/                 # Unauthenticated routes
└── (authenticated)/          # Protected routes
    └── layout.tsx            # Auth wrapper

components/
├── ui/                       # Primitives (button, input, card)
├── layout/                   # Shell (header, nav, footer)
└── [feature]/                # Feature-specific components

services/                     # API client functions
providers/                    # React context providers
hooks/                        # Custom hooks
types/                        # TypeScript definitions
lib/                          # Utilities
```

## Organization Principles

**Group by feature, not by type.**

A feature folder contains all components specific to that feature.

**Shared components bubble up.**

When a component is used by multiple features, move it to `components/ui/` or `components/layout/`.

**Services are thin.**

API client functions handle fetch, auth headers, and error transformation. Business logic stays in the backend.

**Providers are minimal.**

Use React context for cross-cutting concerns: auth state, theme, toasts. Avoid prop drilling. Avoid overuse.

---

# API Integration

## Client Functions

Typed functions in `services/`:

```typescript
export async function getItems(): Promise<Item[]> {
    const response = await fetch("/api/v1/items", {
        headers: authHeaders(),
    });
    if (!response.ok) throw new ApiError(response);
    return response.json();
}
```

Each function handles one endpoint. Composition happens at the component level.

## Error Handling

API errors must be caught and surfaced.

| Error            | User Sees                      |
| ---------------- | ------------------------------ |
| Network failure  | "Unable to connect" + retry    |
| 401 Unauthorized | Redirect to login              |
| 4xx Client error | Actionable message             |
| 5xx Server error | "Something went wrong" + retry |

Never display raw errors, stack traces, or technical details.

## Loading States

All async operations show feedback:

-   Skeleton loaders for initial page data
-   Spinners for user-initiated actions
-   Disabled controls while submitting

## Authentication

-   Include credentials on API requests
-   Handle 401 globally (redirect to login)
-   Clear session state on logout
-   Persist session appropriately (secure http only cookies preferred)

---

# Verification

UI verification follows the same contract as backend verification (see `verification.md`).

Key principles for UI:

## The Client is Part of the System

A frontend calling a backend API is not standalone.

The frontend and backend together are the system under verification.

Internal dependencies (your frontend → your backend) **must not** be mocked.

## Seed Real Data

Verify against deterministic, seeded data—not mocks.

Test data should be created through the same API or database the real application uses.

## Turnkey Delivery

A single command must produce a working application:

1. Build all artifacts
2. Start all services
3. Seed necessary data
4. Ready for interaction

If the command fails or the application is broken, the feature is incomplete.

## Verification Checklist

A UI feature is verified when:

-   Application starts successfully
-   User can authenticate
-   Feature is accessible and functional
-   No console errors in normal operation
-   E2E tests pass against real backend
-   Error and loading states function correctly

Use playwright to exercise all of the capabilities in the North Star and Epic

e2e tests should be integrated with real API calls. It should not be possible for the app to be broken for a user while passing e2e tests

---

# Constraints

1. **Next.js App Router** — no other frameworks
2. **TypeScript strict** — no `any` without justification
3. **Tailwind CSS** — no alternative styling
4. **shadcn/ui** — no runtime component libraries
5. **Lucide icons** — consistent iconography
6. **API-only data** — UI never accesses database directly
7. **Responsive design** - Desktop prioritized but mobile should not be broken

---

# Non-Goals

-   Offline/PWA support
-   Real-time collaboration features
-   Complex client state management (Redux, etc.)
-   Server Actions for mutations (use API)
-   Micro-frontend architecture

---

# Governing Principle

The UI is the user's interface to the system.

It must be simple to build with the constrained stack.

It must be verified against the real backend.

It must be delivered as a working application.

Complexity in the UI creates maintenance burden without adding capability. The backend handles business logic. The UI handles presentation.

Keep it simple. Keep it working.
