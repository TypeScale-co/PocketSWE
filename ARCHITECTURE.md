# Agent Build Contract

## Objective

Build and extend this application using onion architecture, SOLID principles, explicit dependency inversion, and high-cohesion modules.

The codebase must remain understandable as it grows.

A developer should be able to understand the application by reviewing a shallow architectural spine:

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

Every new feature must extend this structure rather than bypass it.

---

# Architecture

```text
Domain
Services
Services.Ports
Adapters
Controller
*.Util
```

Repositories are persistence ports defined under `Services.Ports` and implemented by database adapters.

Example:

```text
Services.Ports.Repository.CustomerRepository
Adapters.Postgres.CustomerRepository
```

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

## Mandatory dependency rules

### Domain

`Domain` defines the application’s core concepts, states, rules, and invariants.

Domain may contain:

- Entities
- Value objects
- Domain identifiers
- Domain errors
- Domain events
- State transitions
- Validation and invariants
- Pure domain behavior

Domain:

- MUST NOT depend on Services, Ports, Adapters, Controller, databases, frameworks, or vendor libraries.
- MUST protect states that must always remain valid (invariants).
- SHOULD use explicit domain types instead of generic primitives or untyped structures.
- SHOULD remain deterministic and independently testable.

If a rule must always be true for a domain object to be valid, it belongs in Domain.

---

### Services

`Services` contains business capabilities and application workflows.

Service names MUST describe a responsibility using noun-based names.

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

Services:

- MUST depend on external behavior only through Ports.
- MUST NOT import concrete Adapters.
- MUST NOT execute raw database queries.
- MUST NOT accept framework-specific request, response, or controller objects.
- MUST declare dependencies explicitly through construction or function parameters.
- SHOULD expose a small public surface.
- SHOULD represent one durable business responsibility.
- SHOULD return domain or application-owned types.
- MAY depend on other Services when responsibilities remain clear and circular dependencies are avoided.

A service coordinates behavior. It does not own transport, vendor, or database implementation details.

---

### Services.Ports

`Services.Ports` contains application-owned interfaces for capabilities implemented outside the application core.

Examples:

```text
PaymentGateway
EmailSender
Clock
IDGenerator
EventPublisher
CustomerRepository
OrderRepository
TransactionRunner
```

Ports:

- MUST be owned by the consuming application code.
- MUST describe what the application needs, not what a vendor provides.
- MUST use domain or application-owned types.
- MUST NOT expose SDK models, ORM entities, SQL rows, driver types, or framework objects.
- SHOULD be narrow and consumer-oriented.
- SHOULD document important behavioral expectations such as idempotency, ordering, atomicity, retry safety, and missing-value behavior.
- MUST NOT become universal infrastructure abstractions.

Prefer:

```text
PaymentGateway.Authorize(...)
CustomerRepository.FindByID(...)
EventPublisher.PublishOrderCreated(...)
```

Avoid:

```text
StripeClient.CreatePaymentIntent(...)
Database.Execute(...)
GenericRepository<T>
ExternalAPIClient.Call(...)
```

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

---

# Repositories

A repository is a specialized persistence Port.

Define repository interfaces in:

```text
Services.Ports.Repository
```

Implement them in a database Adapter:

```text
Adapters.Postgres.CustomerRepository
Adapters.SQLite.CustomerRepository
Adapters.Memory.CustomerRepository
```

Example:

```text
CustomerCreator
    |
    v
CustomerRepository port
    |
    v
Postgres CustomerRepository adapter
```

Repository Ports:

- MUST expose application-meaningful persistence operations.
- MUST return domain or application-owned types.
- MUST hide SQL, database drivers, ORM models, table structure, and storage-specific errors.
- SHOULD remain narrow.
- SHOULD model access patterns required by consumers rather than generic CRUD.

Prefer:

```text
FindCustomerByID
SaveCustomer
FindOpenOrders
RecordPaymentAuthorization
```

Avoid:

```text
Query(string)
Execute(any)
Find(map[string]any)
Repository<T>
```

Concrete repository Adapters own:

- SQL
- ORM usage
- Database rows
- Query builders
- Storage mappings
- Driver errors
- Database-specific optimization

Do not add a separate repository service layer by default.

Create a persistence-focused Service only when meaningful application behavior exists beyond ordinary storage access, such as:

- Assembling a complex aggregate
- Coordinating multiple repositories
- Applying application-level query policy
- Reconciling records
- Coordinating a business transaction
- Combining multiple persistence sources

Such Services must use responsibility-based names:

```text
CustomerAggregateLoader
LedgerReconciler
OrderHistoryReader
```

Do not create a repository wrapper that only forwards calls to another repository interface.

---

# Adapters

`Adapters` contains concrete integrations with external systems.

Examples:

```text
Adapters.Postgres
Adapters.Stripe
Adapters.SendGrid
Adapters.S3
Adapters.Redis
Adapters.SystemClock
```

Adapters:

- MUST implement Ports defined by the application core.
- MAY depend on vendor SDKs, database drivers, protocols, and frameworks.
- MUST translate external representations into application-owned types.
- MUST translate external failures into application-owned errors when crossing inward.
- MUST NOT contain application business policy.
- MUST NOT be imported directly by Services.
- MUST NOT allow vendor or persistence types to cross the adapter boundary.

Adapter-local types MAY be placed in:

```text
Adapters.Stripe.Types
Adapters.Postgres.Types
```

Use adapter-local Types for:

- API request and response models
- Database rows
- ORM entities
- Wire representations
- Vendor-specific enums
- Serialization structures

Do not create one global `Adapters.Types` package shared across unrelated adapters.

Types belong to the adapter whose external representation they model.

---

# Controller

`Controller` is the composition and application-entry layer.

It owns:

- Bootstrapping
- Configuration
- Dependency construction
- Dependency registration
- Route, command, worker, and handler registration
- Application startup and shutdown
- Transport input and output translation

Controller may depend on all layers because it binds interfaces to implementations.

Example:

```text
CustomerRepository -> PostgresCustomerRepository
PaymentGateway      -> StripePaymentGateway
Clock               -> SystemClock
```

Controllers:

- MUST remain thin.
- MUST translate input into application-owned input.
- MUST invoke a Service.
- MUST translate the result into transport output.
- MUST NOT implement business rules.
- MUST NOT execute database queries.
- MUST NOT coordinate adapters to perform business workflows.

Controller may expose one or more transport endpoints, including:

- HTTP APIs
- CLI applications
- Background workers
- Scheduled jobs
- Event consumers

Transport endpoints gather input, invoke Services, and render or emit results.

They MUST NOT contain business logic.

---

# Utilities

A `Util` package MAY exist inside any architectural bucket:

```text
Domain.Util
Services.Util
Adapters.Postgres.Util
Controller.HTTP.Util
```

Utilities support DRY only when repeated code represents the same stable knowledge.

Utilities:

- MUST remain within the dependency rules of their containing layer.
- MUST have a clear owner and narrow purpose.
- SHOULD remain close to their consumers.
- MUST NOT contain business workflows or domain rules.
- MUST NOT become a dumping ground for code with unclear ownership.

Prefer duplication over the wrong abstraction.

Extract a utility only when:

1. The behavior is genuinely the same.
2. It is expected to evolve for the same reason.
3. Its owning layer is clear.
4. Extraction reduces maintenance without creating coupling.

---

# Additional Project Structure

The following directories support the application architecture but are not part of the architectural dependency model.

## Clients

`Clients` contains standalone applications that consume the system through published transport endpoints.

Examples:

- Web SPA
- Mobile application
- Desktop application

Clients communicate with the system through published APIs or other transport interfaces.

Client architecture is independent of the backend architecture.

Clients MUST NOT depend directly on backend Domain, Services, Ports, Adapters, or Controller code.

---

## Docs

`Docs` contains project documentation and architectural knowledge.

Examples:

- Architecture
- North Stars
- Epics
- ADRs
- API documentation
- Design proposals

Documentation should remain synchronized with significant architectural and behavioral changes.

---

# Feature Construction Procedure

For every requested feature, work from the inside outward.

## 1. Identify Domain impact

Determine whether the feature adds or changes:

- Concepts
- States
- Invariants
- Value objects
- Errors
- Transitions
- Domain events

Do not begin with an endpoint, database table, or vendor client when the feature changes application meaning.

## 2. Identify the Service responsibility

Create or extend a focused Service using a noun-based responsibility name.

Do not place the workflow inside a Controller or Adapter.

## 3. Identify required Ports

Define only the external capabilities the Service actually needs.

Reuse an existing Port when its contract already matches the requirement.

Do not expand an existing Port with unrelated methods.

## 4. Add repository access when needed

Define persistence requirements as narrow repository Ports.

Implement them in the relevant database Adapter.

Do not introduce an additional repository service unless it coordinates meaningful application behavior.

## 5. Implement or extend Adapters

Contain all external, vendor, transport, and persistence-specific details inside the Adapter.

Translate external types at the boundary.

## 6. Compose the feature

Register concrete implementations and construct Services in Controller.

## 7. Add tests

Test each affected boundary at the appropriate layer.

Use only the layers required by the feature.

A pure domain change may require only Domain and tests.

Do not create a Service, Port, Adapter, repository, mapper, or utility merely to satisfy a template.

Mock or fake dependencies at architectural boundaries when appropriate.

Prefer:

- Domain tests with no mocks.
- Service tests with mocked Ports.
- Adapter tests with mocked external systems where practical, plus targeted integration tests against the real technology.
- Controller tests with mocked Services.

---

# Complexity Controls

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

Code that changes for the same business reason SHOULD remain close together.

Do not fragment one cohesive feature across unnecessary classes, files, or abstractions.

The simplest design that respects the boundaries is preferred.

---

# Required Agent Plan

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

---

# Required Completion Audit

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

---

# Governing Principle

Every feature adds complexity.

The architecture must ensure that complexity has:

- One clear owner
- One clear dependency direction
- One clear boundary
- One obvious place to change

Grow the application by extending a stable spine of Domain, Services (public), and Ports with contained leaves of Adapters, Service implementations, and Controllers.

Do not eliminate necessary complexity.

Contain it.
