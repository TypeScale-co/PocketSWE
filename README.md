# PocketSWE

A fully opinionated set of documentation to shape AI agent builds and keep complexity contained.

## What This Is

PocketSWE provides a minimal set of contracts that tell AI agents _how_ to build software. Drop these files into a greenfield project and agents will follow consistent architectural patterns, verification procedures, and work protocols.

These documents encode hard-won opinions about:

-   **Architecture** - Onion architecture with explicit dependency inversion, SOLID principles, and high-cohesion modules
-   **Verification** - End-to-end feature verification against a defined "North Star"
-   **Work Protocol** - A structured workflow from discovery through integration

## Why This Exists

AI agents are capable builders, but they benefit from constraints. Without guidance, agents make inconsistent architectural decisions, skip verification, or produce code that becomes difficult to maintain as it grows.

PocketSWE locks in the boring decisions upfront so agents can focus on solving your actual problem.

## The Documents

| File               | Purpose                                                                                              |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| `ARCHITECTURE.md`  | Defines the architectural spine (Domain, Services, Ports, Adapters, Controller) and dependency rules |
| `VERIFICATION.md`  | Defines how to verify completed features through executable system behavior                          |
| `WORK_PROTOCOL.md` | Defines the workflow: Discover, Architect, Decompose, Execute, Integrate, Close                      |

## Usage

1. Copy these files into your project root
2. Reference them in your agent's system prompt or context
3. Build

The documents are designed to be self-contained. Agents should read `ARCHITECTURE.md` before building, `WORK_PROTOCOL.md` before planning, and `VERIFICATION.md` before marking features complete.

## Best For

-   Greenfield projects where you want to establish patterns early
-   Teams using AI agents for feature development
-   Projects where maintainability matters more than speed-to-first-commit

## Not For

-   Brownfield projects with established (different) patterns
-   Quick prototypes where structure is overhead
-   Projects where the existing architecture should be preserved

## License

MIT License. See [LICENSE](LICENSE).

## Contributing

Issues and pull requests welcome at [github.com/TypeScale-co/PocketSWE](https://github.com/TypeScale-co/PocketSWE).
