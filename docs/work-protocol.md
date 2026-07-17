# Agent Work Protocol

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

Assign one agent per implementation step.

Each agent:

- Reviews the North Star
- Reviews the Architecture Canon
- Reviews the Epic context
- Reviews the Step context
- Plans against the current codebase
- Implements only its assigned step
- Adds appropriate tests
- Submits the step for code review
- Verifies completion

Agents should not modify unrelated steps.

### Parallel Execution

When steps execute in parallel, each agent works in a separate worktree and branch.

After a step's changes are accepted and integrated, the agent removes its worktree
and branch. Do not leave orphaned branches or worktrees.

### Step Verification

Before integration, each step requires:

- Unit tests covering the step's scope
- Code review via the `reviewing-code` skill

Step verification validates the implementation. Feature verification validates the
integrated system.

---

## 6. Integrate & Review

Integrate completed steps and review the combined result.

**Integration review** verifies:

- No conflicts between neighboring steps
- No duplicated work
- No architectural violations introduced by integration
- Combined behavior matches the North Star

**Code review** (via `reviewing-code` skill) validates the integrated feature before verification.

Resolve integration issues before closing the Epic.

---

## 7. Close

Before closing, complete:

- **Code review** of the integrated feature
- **Feature verification** (via `verifying-features` skill) proving the integrated
  system satisfies the North Star through executable end-to-end behavior

Verify that:

- Every acceptance criterion is satisfied.
- All steps are complete.
- Tests pass.
- Architecture remains compliant.
- Documentation is updated if required.

The Epic is complete only when the integrated system satisfies the original North Star.
