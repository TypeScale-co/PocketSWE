---
name: building-features
description: Builds and extends features using the onion/ports-and-adapters architecture — inside-out construction, a required pre-implementation plan, and a completion audit. Use when implementing a new feature or changing application structure.
---

# Building Features

Work from the inside outward: Domain first, transport and vendors last. The always-on
contract (`AGENTS.md`) defines the spine, dependency direction, and prohibited
patterns. The complete layer rules — everything Domain, Services, Ports, Repositories,
Adapters, Controller, and Utilities MUST and SHOULD do — live in
[docs/architecture.md](../../../docs/architecture.md). Consult them whenever a
placement decision is unclear.

## Required plan (before implementation)

Before implementation, produce:

```text
Domain:
Services:
Ports:
Repositories:
Adapters:
Controller:
Tests:
```

Use `None` for categories that are not required.

The plan must identify existing components to reuse before introducing new ones.

## Feature Construction Procedure

### 1. Identify Domain impact

Determine whether the feature adds or changes:

- Concepts
- States
- Invariants
- Value objects
- Errors
- Transitions
- Domain events

Do not begin with an endpoint, database table, or vendor client when the feature
changes application meaning.

Domain must remain deterministic, independently testable, and free of dependencies on
outer layers. If a rule must always be true for a domain object to be valid, it belongs
in Domain. Use explicit domain types instead of generic primitives or untyped
structures.

### 2. Identify the Service responsibility

Create or extend a focused Service using a noun-based responsibility name.

Preferred:

```text
CustomerCreator
PaymentAuthorizer
ShipmentScheduler
RenewalPriceCalculator
OrderReconciler
```

Avoid:

```text
CreateCustomerService
GeneralManager
CommonService
DataProcessor
```

Do not place the workflow inside a Controller or Adapter.

A service coordinates behavior. It does not own transport, vendor, or database
implementation details. It declares its dependencies explicitly through construction or
function parameters, exposes a small public surface, represents one durable business
responsibility, and returns domain or application-owned types.

### 3. Identify required Ports

Define only the external capabilities the Service actually needs.

Reuse an existing Port when its contract already matches the requirement.

Do not expand an existing Port with unrelated methods.

Ports are owned by the consuming application: they describe what the application needs,
not what a vendor provides, and they use domain or application-owned types — never SDK
models, ORM entities, SQL rows, driver types, or framework objects. Keep them narrow
and consumer-oriented, and document important behavioral expectations such as
idempotency, ordering, atomicity, retry safety, and missing-value behavior.

Create a Port only when a real architectural boundary exists, such as:

- Persistence
- Network access
- Vendor integration
- Filesystem access
- Time
- Randomness
- Identifier generation
- Messaging
- Transactions
- Nondeterministic system behavior

Do not create an interface solely because a concrete type exists.

### 4. Add repository access when needed

Define persistence requirements as narrow repository Ports under
`Services.Ports.Repository`, exposing application-meaningful operations
(`FindCustomerByID`, `SaveCustomer`) rather than generic CRUD (`Query(string)`,
`Repository<T>`). Implement them in the relevant database Adapter.

Do not introduce an additional repository service unless it coordinates meaningful
application behavior (assembling a complex aggregate, coordinating multiple
repositories, reconciling records). Never create a repository wrapper that only
forwards calls to another repository interface.

### 5. Implement or extend Adapters

Contain all external, vendor, transport, and persistence-specific details inside the
Adapter. Translate external types and failures into application-owned ones at the
boundary. Adapter-local types (API models, database rows, ORM entities) belong to the
adapter whose external representation they model — not to a global shared package.

### 6. Compose the feature

Register concrete implementations and construct Services in Controller. Controllers
stay thin: translate input, invoke a Service, translate output. No business logic, no
database queries, no coordinating adapters into business workflows.

### 7. Add tests

Test each affected boundary at the appropriate layer. Use only the layers required by
the feature — a pure domain change may require only Domain and tests. Do not create a
Service, Port, Adapter, repository, mapper, or utility merely to satisfy a template.

Mock or fake dependencies at architectural boundaries when appropriate. Prefer:

- Domain tests with no mocks.
- Service tests with mocked Ports.
- Adapter tests with mocked external systems where practical, plus targeted
  integration tests against the real technology.
- Controller tests with mocked Services.

## Required Completion Audit

Before completing the change, verify:

- Domain invariants remain protected.
- Dependencies point inward.
- Services depend only on application-owned abstractions.
- Repository interfaces are narrow and application-oriented.
- Concrete persistence remains inside Adapters.
- External types do not leak inward.
- Controllers contain no business logic.
- No unnecessary interface, layer, mapper, or utility was added.
- No circular dependency was introduced.
- The new behavior has one clear owner.
- Tests cover the affected boundaries.
- The architectural spine remains shallow and understandable.

Complete the change with this summary:

```text
Domain:
Services:
Ports:
Repositories:
Adapters:
Controller:
Tests:
Architecture notes:
```
