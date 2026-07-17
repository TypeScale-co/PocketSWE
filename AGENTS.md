# PocketSWE Agent Contract

Build and extend this application using onion architecture, SOLID principles, explicit
dependency inversion, and high-cohesion modules. The codebase must remain understandable
as it grows.

## Architectural spine

A developer should be able to understand the application by reviewing a shallow spine:

```text
Domain
Services (public capabilities)
Services.Ports (dependency contracts)
```

Concrete implementations must remain contained behind that spine:

```text
Adapters
Controller
Service implementations
```

Every new feature must extend this structure rather than bypass it. Repositories are
persistence ports defined under `Services.Ports.Repository` and implemented by database
adapters (e.g. `Adapters.Postgres.CustomerRepository`).

## Dependency direction

Dependencies point inward:

```text
Controller
   |
   v
Services ---> Services.Ports <--- Adapters
   |
   v
Domain
```

- `Domain` depends on nothing outside itself — never on Services, Ports, Adapters,
  Controller, databases, frameworks, or vendor libraries.
- `Services` depend on external behavior only through Ports.
- `Adapters` implement Ports and translate external types and failures at the boundary.
- `Controller` composes everything and stays thin: translate input, invoke a Service,
  translate output.

## Complexity Controls

The following are prohibited:

- Domain importing outer layers
- Services importing concrete Adapters
- Business logic inside Controllers
- Business logic inside database or vendor Adapters
- Raw queries inside ordinary Services
- Vendor or database types crossing inward
- Circular dependencies
- Global mutable dependencies
- Service locators
- Unstructured maps passed across layers
- Generic repositories without demonstrated need
- Broad interfaces containing unrelated capabilities
- Wrapper layers that only forward calls
- Utilities used to hide unclear ownership
- God services with unrelated responsibilities

Code that changes for the same business reason SHOULD remain close together. Do not
fragment one cohesive feature across unnecessary classes, files, or abstractions. The
simplest design that respects the boundaries is preferred.

## Governing principle

Every feature adds complexity. Complexity must have one clear owner, one clear
dependency direction, one clear boundary, and one obvious place to change. Do not
eliminate necessary complexity. Contain it.

## Skills (procedures, loaded on demand)

- [planning-work](.agents/skills/planning-work/SKILL.md) — North Star, plan,
  decomposition, and dependency graph; use before starting a feature or epic.
- [building-features](.agents/skills/building-features/SKILL.md) — inside-out feature
  construction, required plan, and completion audit; use when implementing.
- [reviewing-code](.agents/skills/reviewing-code/SKILL.md) — coordinates independent
  code investigations across correctness, architecture, testing, and security.
- [verifying-features](.agents/skills/verifying-features/SKILL.md) — end-to-end North
  Star verification with an executable driver; use when a feature is code-complete.

## Full-text sources

- [docs/architecture.md](docs/architecture.md) — complete layer rules for Domain,
  Services, Ports, Repositories, Adapters, Controller, and Utilities.
- [docs/work-protocol.md](docs/work-protocol.md) — the full Discover→Close protocol.
- [docs/code-review.md](docs/code-review.md) — the full code review contract.
- [docs/verification.md](docs/verification.md) — the full verification contract.
