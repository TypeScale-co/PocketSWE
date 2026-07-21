# Agent Work Protocol

## Agent Hierarchy

```text
Epic Orchestrator
    │
    ├── Step Agent (sub-agent)
    │       │
    │       └── Reviewer Sub-agents
    │               Correctness
    │               Architecture
    │               Test
    │               Security
    │
    ├── Step Agent (sub-agent)
    │       │
    │       └── Reviewer Sub-agents
    │
    └── ... (one Step Agent per implementation step)

    After all steps submit:
    │
    ├── Reviewer Sub-agents (integrated feature)
    │
    └── Feature Verification
```

The **Epic Orchestrator** owns the epic from discovery through close. It spawns Step Agents, receives their completed work, integrates, reviews the integrated result, verifies, and closes.

Each **Step Agent** is a fresh-context sub-agent responsible for one implementation step. It implements, orchestrates its own code review (spawning Reviewer sub-agents), resolves findings, and submits the completed step back to the Epic Orchestrator.

**Reviewer Sub-agents** are fresh-context sub-agents spawned by either a Step Agent or the Epic Orchestrator to perform independent code review investigations.

---

## 1. Discover

Gather information until the feature intent is unambiguous.

Produce a North Star describing:

- Goal
- Expected behavior
- Domain concepts
- Invariants
- Constraints
- Non-goals
- Acceptance criteria

Do not begin implementation until the North Star is complete.

---

## 2. Architect

Translate the North Star into an implementation plan.

Identify:

- Domain changes
- Services
- Ports
- Adapters
- Controllers
- Tests

Determine where each responsibility belongs according to the Architecture Canon.

---

## 3. Decompose

Break the work into self-contained implementation steps.

Each step should:

- Have one clear responsibility
- Be independently reviewable
- Minimize overlap with other steps
- Expose a clear completion criterion

Each step contains its own requirements and acceptance criteria.

---

## 4. Build Dependency Graph

Identify dependencies between steps.

Mark each step as:

- Independent
- Depends on X
- Blocks Y

Maximize parallelism while preserving correctness.

---

## 5. Execute

The Epic Orchestrator spawns one Step Agent (sub-agent) per implementation step.

### Step Agent Responsibilities

Each Step Agent:

1. Reviews the North Star
2. Reviews the Architecture Canon
3. Reviews the Epic context
4. Reviews the Step requirements
5. Plans against the current codebase
6. Implements only its assigned step
7. Adds appropriate tests
8. Orchestrates code review (via `reviewing-code` skill)
9. Resolves all blocking findings
10. Submits completed step to the Epic Orchestrator

Step Agents MUST NOT submit steps with unresolved blocking findings.

Step Agents MUST NOT modify code outside their assigned step.

### Parallel Execution

When steps execute in parallel, each Step Agent works in a separate worktree and branch.

After a step's changes are accepted and integrated, the Step Agent removes its worktree and branch. Do not leave orphaned branches or worktrees.

---

## 6. Integrate & Review

The Epic Orchestrator receives completed steps from Step Agents and integrates them.

After integration, the Epic Orchestrator:

1. Orchestrates code review of the integrated feature (via `reviewing-code` skill)
2. Resolves all blocking findings
3. Verifies no conflicts between steps
4. Verifies no architectural violations introduced by integration
5. Verifies combined behavior matches the North Star

Do not proceed to Close with unresolved blocking findings.

---

## 7. Close

The Epic Orchestrator completes verification and closes the epic.

1. Run feature verification (via `verifying-features` skill)
2. Prove the integrated system satisfies the North Star through executable end-to-end behavior
3. Verify all acceptance criteria are satisfied
4. Verify all tests pass
5. Verify architecture remains compliant
6. Update documentation if required

The Epic is complete only when the integrated system satisfies the original North Star.
