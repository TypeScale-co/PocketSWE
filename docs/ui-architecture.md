# Agent UI Architecture Contract

This contract governs **browser-based user interface** construction. It defines the stack,
patterns, and structure for web clients that consume backend APIs.

A web client is a `Clients` entry in the Architecture Canon. `architecture.md` governs the
client's relationship to the backend; this contract governs the client's internals.

For verification requirements, see `verification.md`. The UI is part of the system — not a
separate application.

## Objective

Build accessible, maintainable web interfaces using a constrained set of tools and patterns.

UI clients:

- MUST consume backend APIs as their only data source.
- MUST render correctly in current versions of Chrome, Firefox, Safari, and Edge.
- MUST support light and dark themes.
- MUST start and function from a single documented command.
- SHOULD remain understandable as they grow.

---

# Placement

A web client lives under `Clients`:

```text
Clients/web/
```

The client MUST NOT import backend Domain, Services, Ports, Adapters, or Controller code.
It communicates with the system only through published transport endpoints.

All paths in this contract are relative to the client root.

---

# Stack

## Framework

**Next.js** with App Router.

- Server Components MUST own initial page data.
- Client Components MUST be limited to interactive elements.
- Routing MUST be file-based.
- TypeScript MUST run in strict mode.

Other frameworks introduce unnecessary divergence.

## Styling

**Tailwind CSS** for all styling.

- Utility classes MUST be the only styling mechanism.
- CSS modules, CSS-in-JS, and inline style objects MUST NOT be used.
- Design tokens MUST be defined in Tailwind configuration rather than repeated as literals.

Tailwind provides consistency without runtime overhead.

## Components

**shadcn/ui** for component primitives.

- Primitives MUST be copied into the project, not consumed as a runtime dependency.
- The accessibility behavior supplied by Radix MUST be preserved.
- Customization happens in the copied source.

Owning the component source prevents version lock-in and enables customization.

## Icons

**Lucide React** for iconography.

- Icons MUST be imported individually to preserve tree-shaking.
- Decorative icons MUST be hidden from assistive technology.
- Icon-only controls MUST carry an accessible name.

## Theming

**next-themes** for dark mode.

- System preference MUST be detected by default.
- A manual toggle MUST be available.
- Palettes MUST switch through CSS variables bound to semantic tokens.
- Theme-specific colors MUST NOT be hardcoded at the component level.

---

# Data Access

## Reads

Server Components are the default owner of server data.

- Initial page data MUST be fetched in a Server Component and passed down as props.
- Server data MUST NOT be mirrored into `useState` as a cache.
- `useEffect` MUST NOT fetch data that a Server Component can fetch.

## Mutations

- Mutations MUST call a typed function in `services/`.
- After a successful mutation, affected data MUST be refreshed through `router.refresh()`.
- Server Actions MUST NOT be used. Mutations go through the API.

## Escalation

A client-side server-state library (TanStack Query) MAY be introduced only when a screen
requires behavior Server Components cannot express:

- Polling or live-updating data
- Pagination or infinite scroll retained across interaction
- Optimistic updates
- Cache invalidation shared across unrelated components

When introduced, it MUST be scoped to the feature that requires it and MUST NOT become the
default data path.

Client state management frameworks for non-server state MUST NOT be used.

---

# Design System

## Semantic Colors

Colors MUST be defined by purpose, not by value:

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

Font stack:

```text
Inter, system-ui, -apple-system, sans-serif
```

Type scale:

| Purpose         | Class                           |
| --------------- | ------------------------------- |
| Page title      | `text-2xl font-semibold`        |
| Section heading | `text-lg font-medium`           |
| Card/item title | `text-base font-medium`         |
| Body text       | `text-sm`                       |
| Caption/helper  | `text-xs text-muted-foreground` |

Sizes outside this scale MUST NOT be used without extending the table.

## Spacing

4px base grid. Values off the grid MUST NOT be used.

| Context      | Multiplier     | Tailwind                  |
| ------------ | -------------- | ------------------------- |
| Inline/tight | 2x (8px)       | `gap-2`                   |
| Form fields  | 4x (16px)      | `space-y-4`               |
| Card padding | 6x (24px)      | `p-6`                     |
| Sections     | 6-8x (24-32px) | `space-y-6` / `space-y-8` |

---

# Accessibility

Radix primitives supply baseline behavior. That baseline MUST NOT be defeated, and it does
not by itself satisfy this contract.

Every interface:

- MUST be fully operable by keyboard, in a logical tab order, with no keyboard traps.
- MUST show a visible focus indicator on every focusable element.
- MUST give every control an accessible name.
- MUST associate form inputs with their labels and their validation messages.
- MUST meet WCAG AA contrast in both themes: 4.5:1 for body text, 3:1 for large text and
  interactive boundaries.
- MUST NOT convey state through color alone.
- MUST announce asynchronous state changes and errors to assistive technology.
- MUST use semantic elements. A `div` MUST NOT stand in for a button, link, or heading.

The end-to-end suite MUST run an automated accessibility check against each verified screen.
Automated checks are necessary but not sufficient — keyboard operation MUST be exercised
explicitly.

---

# Structure

## Directory Layout

```text
Clients/web/
├── app/                      # Routes and pages
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Entry point
│   ├── (public)/             # Unauthenticated routes
│   └── (authenticated)/      # Protected routes
│       └── layout.tsx        # Auth wrapper
│
├── components/
│   ├── ui/                   # Primitives (button, input, card)
│   ├── layout/               # Shell (header, nav, footer)
│   └── [feature]/            # Feature-specific components
│
├── services/                 # API client functions
├── providers/                # React context providers
├── hooks/                    # Custom hooks
├── types/                    # TypeScript definitions
└── lib/                      # Utilities
```

## Organization Principles

**Group by feature, not by type.**

A feature folder MUST contain the components specific to that feature.

**Shared components bubble up.**

When a component is used by more than one feature, it MUST move to `components/ui/` or
`components/layout/`. It MUST NOT be duplicated per feature.

**Services are thin.**

Service functions own fetch, auth headers, and error transformation. Business logic MUST
remain in the backend.

**Providers are minimal.**

React context is for cross-cutting concerns: auth state, theme, toasts. Use it to avoid
prop drilling, not as a general state store.

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

- Each function MUST handle exactly one endpoint.
- Each function MUST return an application-owned type, never a raw response.
- Composition happens at the component level.

## Error Handling

API errors MUST be caught and surfaced:

| Error            | User Sees                      |
| ---------------- | ------------------------------ |
| Network failure  | "Unable to connect" + retry    |
| 401 Unauthorized | Redirect to login              |
| 4xx Client error | Actionable message             |
| 5xx Server error | "Something went wrong" + retry |

Raw errors, stack traces, and technical details MUST NOT be displayed.

## Loading States

Every async operation MUST show feedback:

- Skeleton loaders for initial page data
- Spinners for user-initiated actions
- Disabled controls while submitting

## Forms

- Client-side validation MUST be limited to input shape and immediate feedback.
- Business rules MUST be enforced by the backend. The client surfaces backend validation
  errors rather than duplicating the rules.
- Submit controls MUST be disabled while a submission is in flight.

## Authentication

- Requests MUST include credentials.
- 401 responses MUST be handled globally by redirecting to login.
- Session state MUST be cleared on logout.
- Sessions SHOULD be persisted in secure, `HttpOnly` cookies.

---

# Verification

UI verification follows `verification.md`. This section states the UI-specific requirements.

## The Client Is Part of the System

A frontend calling a backend API is not standalone. The frontend and backend together are
the system under verification.

- Internal dependencies (your client to your backend) MUST NOT be mocked.
- Third-party externals MAY use the lightest boundary implementation `verification.md`
  permits.

## Seed Real Data

- Verification MUST run against deterministic, seeded data.
- Seed data MUST be created through the same API or database the real application uses.

## Turnkey Delivery

A single command MUST:

1. Build all artifacts
2. Start all services
3. Seed necessary data
4. Leave the application ready for interaction

If the command fails or the application is broken, the feature is incomplete.

## Test Layers

- Component tests MAY cover isolated rendering and interaction logic.
- End-to-end tests MUST use Playwright.
- End-to-end tests MUST exercise every North Star and Epic capability through the running
  application against the real backend.
- It MUST NOT be possible for the application to be broken for a user while the end-to-end
  suite passes.

## Verification Checklist

A UI feature is verified when:

- The application starts from the single command.
- A user can authenticate.
- The feature is reachable and functional through the UI.
- Loading, empty, and error states render correctly.
- Accessibility checks pass.
- No console errors occur in normal operation.
- Playwright tests pass against the real backend.

---

# Constraints

1. **Next.js App Router** — no other framework
2. **TypeScript strict** — `any` is prohibited; use `unknown` at boundaries and narrow
3. **Tailwind CSS** — no alternative styling mechanism
4. **shadcn/ui** — no runtime component library
5. **Lucide icons** — no second icon set
6. **API-only data** — the client never reaches the database
7. **Responsive** — desktop is prioritized; every screen MUST remain usable down to 360px
   with no horizontal scroll

---

# Non-Goals

- Offline and PWA support
- Real-time collaboration
- Client state management frameworks
- Server Actions for mutations
- Micro-frontend architecture

---

# Required Agent Plan

Before implementation, produce:

```text
Routes:
Server Components:
Client Components:
Shared components:
Services:
Providers:
Hooks:
Types:
States (loading / empty / error):
Accessibility:
Tests:
```

Use `None` for categories that are not required.

The plan MUST identify existing components, services, and hooks to reuse before introducing
new ones.

---

# Required Completion Audit

Before completing the change, verify:

- The client reaches the backend only through `services/`.
- No business rule was implemented in the client.
- Server Components own server data, or an escalation is justified against the listed
  triggers.
- Shared components live at the correct level and are not duplicated per feature.
- Styling uses only Tailwind utilities and semantic tokens.
- Both themes render correctly.
- Loading, empty, and error states exist for every async path.
- Accessibility requirements are met and checked.
- The application runs from the single command.
- Playwright covers every North Star capability against the real backend.

Complete the change with this summary:

```text
Routes:
Components:
Services:
Providers:
Hooks:
Types:
Tests:
Accessibility notes:
UI notes:
```

---

# Governing Principle

The UI is the user's interface to the system.

It must be simple to build with the constrained stack.

It must be verified against the real backend.

It must be delivered as a working application.

Complexity in the UI creates maintenance burden without adding capability. The backend
handles business logic. The UI handles presentation.

Keep it simple. Keep it working.
