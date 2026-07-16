# PocketSWE

A fully opinionated set of documentation to shape AI agent builds and keep complexity contained.

## What This Is

PocketSWE tells AI agents _how_ to build software. Drop it into a greenfield project and agents will follow consistent architectural patterns, verification procedures, and work protocols.

It is packaged the way coding agents load context:

-   **`AGENTS.md`** — a lean, always-on contract holding the non-negotiable architectural invariants: the spine, the dependency direction, and the prohibited-complexity list. Auto-discovered by the many tools that support the [AGENTS.md standard](https://agents.md) (Codex, Cursor, Copilot CLI, Gemini CLI, Claude Code, and more).
-   **Skills** (`.agents/skills/`) — phase-specific procedures loaded on demand via progressive disclosure: only each skill's name and description sit in context until a matching task loads the body.
-   **`docs/`** — the full-text sources, linked from `AGENTS.md`, as the portable fallback for tools without skill support.

These documents encode hard-won opinions about:

-   **Architecture** - Onion architecture with explicit dependency inversion, SOLID principles, and high-cohesion modules
-   **Verification** - End-to-end feature verification against a defined "North Star"
-   **Work Protocol** - A structured workflow from discovery through integration

## Why This Exists

AI agents are capable builders, but they benefit from constraints. Without guidance, agents make inconsistent architectural decisions, skip verification, or produce code that becomes difficult to maintain as it grows.

PocketSWE locks in the boring decisions upfront so agents can focus on solving your actual problem. And because always-on rules are expensive — every line of `AGENTS.md` rides along on every task — only the invariants stay resident; each procedure loads only when its phase of work begins.

## The Layout

| Path                                        | Loaded             | Purpose                                                                             |
| ------------------------------------------- | ------------------ | ----------------------------------------------------------------------------------- |
| `AGENTS.md`                                 | Always             | Spine, dependency direction, prohibited complexity, pointers to skills and docs     |
| `.agents/skills/planning-work/`             | When planning      | The Discover → Architect → Decompose → Graph → Execute → Integrate → Close protocol |
| `.agents/skills/building-features/`         | When implementing  | Inside-out construction procedure, required plan, completion audit                  |
| `.agents/skills/verifying-features/`        | When verifying     | North Star verification procedure + bundled executable driver script                |
| `docs/architecture.md`                      | On demand          | Full architecture contract (layer rules in detail)                                  |
| `docs/work-protocol.md`                     | On demand          | Full work protocol                                                                  |
| `docs/verification.md`                      | On demand          | Full verification contract                                                          |

## Usage

1. Copy `AGENTS.md`, `.agents/`, and `docs/` into your project root
2. Build — tools that support `AGENTS.md` discover the contract automatically

Agents plan with `planning-work`, implement with `building-features`, and accept nothing as done until `verifying-features` passes. Tools without skill support get the same content through the `docs/` links in `AGENTS.md`.

### Claude users

Claude Code discovers Skills under `.claude/skills/` and reads `CLAUDE.md`. Symlink so the canonical `.agents/` files are picked up:

```bash
mkdir -p .claude && ln -s ../.agents/skills .claude/skills   # skills
ln -s AGENTS.md CLAUDE.md                                    # optional: instruction file
```

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
