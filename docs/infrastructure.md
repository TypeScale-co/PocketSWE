# Infrastructure Canon

**Status:** Adopted PocketSWE methodology v0.1.0.

**Owner:** PocketSWE maintainers.

**Scope:** Common infrastructure rules and independently selectable artifact, workload, provisioning, and host-configuration profiles. This canon governs generation, validation, preparation, and explicitly authorized operations; it does not itself implement an executor or certify a deployment.

**Normative companion documents:** [artifact builds](infrastructure-artifact-builds.md), [workload runtime](infrastructure-workload-runtime.md), [provisioning](infrastructure-provisioning.md), [host configuration](infrastructure-host-configuration.md), [environment selection](infrastructure-environments.md), and the [acceptance matrix](infrastructure-acceptance-matrix.md).

## Purpose

Build, prepare, change, and operate infrastructure through explicit ownership, bounded authority, reproducible inputs, and executable evidence. A maintainer should be able to identify what will change, where it will change, why it is permitted, how success will be observed, and how interruption will be recovered.

This canon complements the Security and Architecture Canons. It applies to build and deployment definitions, resource provisioning, host configuration, and the mechanisms executing them. It does not claim that all tools share identical state, preview, transaction, or rollback semantics.

## How to use this canon

- MUST is required for an applicable operation; MUST NOT is prohibited. SHOULD is expected and a departure needs a recorded reason.
- Select the common rules and the relevant [profiles](README.md). Every required rule needs a check or an explicit evidence obligation. Filename detection may suggest a profile; it cannot grant execution authority or silently select a target.
- A rule may be inapplicable only with an explicit scope-based reason. Missing tools, credentials, permissions, or evidence are not inapplicability.
- A stricter environment or security profile adds requirements. Conflicting requirements block the affected operation until resolved; an agent cannot choose whichever is easier.
- Review findings use the existing review contract and severity vocabulary. Rule identifiers below provide traceability; they are not a new scoring system.
- A documented exception to a SHOULD identifies the owner, reason, affected scope, compensating evidence, and review/expiry condition. It cannot waive operator authority, truthful evidence, credential protection, or ownership checks.

## Architecture and ownership

```text
Application and infrastructure intent
            |
            v
Environment declaration + applicable profiles
            |
            v
Versioned source, dependencies, parameters, and artifacts
            |
            v
Validation and change evidence
            |
            v
Execution authority -> tool-specific operation -> observed result
                                                 |
                                                 v
                                    Acceptance, recovery, and retention
```

Each resource or independently managed property has one declared writer. Shared resources expose an explicit ownership contract. A provisioning tool, host configurator, and workload runtime may manage different boundaries of one system; they MUST NOT compete to reconcile the same property.

Infrastructure definitions SHOULD separate reusable modules from environment composition and secret references. Dependency edges and module outputs MUST be explicit. A module SHOULD own one cohesive lifecycle boundary. Do not invent an application Domain/Services directory tree for a Dockerfile or playbook. Application code used to orchestrate infrastructure still follows the Architecture Canon.

## 1. Scope, identity, and outcome — INF-01

- The work MUST name the intended outcome: prepared source, verified artifact, or verified deployment/configuration. Completion MUST be judged against that outcome. An explicitly scoped source-only task may finish without deployment; a deployment task may not.
- The selected build environment, target environment, runtime/tool binding, owner, resource scope, and permitted operations MUST be explicit. A working directory, active CLI context, environment name such as `dev`, or filename is not sufficient target identity.
- Operations MUST resolve the actual daemon endpoint, cloud account/subscription/tenant and region/scope, or host inventory and compare it with the intended target before acquiring mutation authority. Unresolved identity blocks that operation.
- Cross-environment promotions MUST name their source artifact and destination. A build-host architecture or credential does not determine the target architecture or principal.

## 2. Inputs and supply chain — INF-02

- Source revision plus any deliberate patch, tool/runtime versions, plugin/module/provider identities, parameters, policy versions, and artifact digests MUST be bound to the candidate under review.
- Dependencies MUST use the declared retrieval and integrity mechanism. Mutable references MUST be resolved and recorded; approved promotion MUST use immutable identities. Updates require a deliberate refresh process so pinning does not become indefinite neglect.
- Generated source, plugins, provider binaries, build frontends, callbacks, and scripts MUST be treated as executable inputs where they can execute. A command called validate, plan, or test is not automatically safe to run with unrestricted credentials.
- Build context, output context, cache, state, and credentials MUST have separate ownership and retention rules. A later deletion cannot excuse an earlier secret inclusion in an artifact, cache, or log.

## 3. Execution readiness — INF-03

- Before model-driven implementation that requires an execution path, a bounded host-owned preflight MUST prove the needed path can run its controlled prerequisites. Before an actual operation, relevant volatile prerequisites MUST be rechecked.
- The preflight MUST cover required toolchain, declared dependency access, writable scratch/cache, fixture roots, socket/network/daemon access, target identity, storage, locks, and resource limits where applicable.
- Probes MUST run through the same supported boundary as the eventual check. A host pass cannot stand in for a denied agent-sandbox operation. Cold or intentionally refreshed dependency/cache scenarios MUST be covered where fresh execution is claimed.
- A denied or unavailable prerequisite MUST produce a specific blocker and remedy. It MUST NOT be converted into a code-repair loop, a skipped passing test, or an automatic privilege expansion.
- Preflight MUST distinguish environment mechanics from project assertions. A failing business test is not automatically an environment blocker.

## 4. Authority and reviewable changes — INF-04

- Default agent authority is to generate, validate, and prepare. Live apply, deploy, destroy, import/adopt, state migration, privilege changes, publication, and host mutation MUST require operator authorization covering that operation and target.
- An existing explicit authorization may cover bounded repeated operations. Do not request approval again for an unchanged operation already within that grant. A generic build approval MUST NOT silently confer live deployment authority.
- Disposable validation MUST run only inside an explicitly designated execution environment with bounded resources, credentials, network access, lifetime, and cleanup rights. Merely labeling a shared host or cloud workspace disposable is insufficient.
- Operator approval MUST bind the reviewed artifact/configuration identity, resolved target, parameter identities, permitted effects, relevant observations, and validity conditions. Material changes or expired/revoked authority require renewed review/authorization.
- Changes that may replace/delete resources, alter public exposure or authority, migrate state, incur material cost, or interrupt service MUST be visible before authorization. Unresolved destructive effects block live mutation.
- Credentials MUST be brokered to the owned runner with the least authority for the operation. They MUST NOT be made available to unrelated model tools, prompt context, or reviewers.

## 5. Preview fidelity — INF-05

- Validation, preview, apply, acceptance, and recovery MUST be distinct claims. Successful syntax checking is not a complete preview; a preview is not proof that apply or rollback will succeed.
- A binding MUST declare whether it supplies an executable saved plan, a service-managed change set, an advisory preview, or no preview. Unknown/unsupported coverage MUST be listed explicitly.
- Where an exact executable plan exists, application MUST consume the approved instance. Otherwise execution MUST use the approved source/parameters and a target recheck under bounded authority; it MUST NOT claim exact plan/apply equivalence.
- Preview output MUST be examined for replacement, deletion, unknown values, omitted resources, hooks, and side effects. Relevant unsupported coverage needs an alternate check or a narrower operation; it cannot silently count as no change.

## 6. Durable state and concurrency — INF-06

- Desired state, tool state, application data, runtime sessions, and audit evidence MUST have distinct ownership and lifetimes. Durable recovery MUST NOT depend solely on a disposable workspace or session home.
- The operation MUST serialize competing writers at the real ownership boundary. A backend lock, stack operation, host batch, or daemon lease MUST be used according to the binding's semantics. A process-local lock alone cannot coordinate external actors.
- Lock timeout, stale-lock recovery, state import/migration, and ownership handoff MUST have explicit procedures. An agent MUST NOT force-unlock or replace state because a normal attempt failed.
- State, plans, rendered configuration, inventories, and backups MUST be treated as potentially sensitive. Access, encryption where required by the security profile, retention, restore, and deletion MUST be specified.
- Resource identifiers and successful partial effects MUST be durably recorded even when acceptance or delivery subsequently fails.

## 7. Bounded execution and interruption — INF-07

- Work MUST have explicit limits for elapsed time, subprocesses, concurrent resources/hosts, output, retries, storage, and cost where applicable. Final verification and recovery need budget; they cannot depend on whatever implementation leaves unused.
- Mutations MUST have an operation identity. A lost response or transport timeout MUST enter reconciliation; it MUST NOT immediately replay a potentially successful mutation.
- Cancelling a local CLI MUST NOT be reported as cancelling a cloud operation or reverting its effects. Query authoritative operation/resource state before retry or compensation.
- On an established external blocker, dependent model work MUST stop or settle within a finite policy. Unrelated authorized work may continue when independence is established.
- Cleanup MUST release only resources the operation owns and is authorized to remove. Shared caches, operator data, production volumes, and diagnostic evidence are not generic scratch.

## 8. Data lifecycle and recovery — INF-08

- Stateful resources MUST declare persistence, retention, backup/restore, replacement, and retirement behavior. Availability and recovery objectives MUST be set for the application; the framework does not invent universal RPO/RTO numbers.
- A release rollback, resource recreation, and data restore MUST be distinguished. An older image or template may not reverse a schema migration or recover deleted data.
- Recovery MUST identify the last known valid revision/state, what was changed, what remains unknown, and the authorized next operation. Compensation can fail and needs its own evidence.
- Destructive recovery scenarios MUST be exercised on disposable fixtures or a separately authorized recovery environment. Production restore/destroy is never an implicit negative test.

## 9. Operational acceptance — INF-09

- Acceptance MUST exercise the required behavior at its actual external boundary, under representative target architecture, runtime permissions, and dependencies. Emulation evidence MUST identify what was not tested natively.
- Process running, successful resource creation, and healthy application behavior MUST be distinguished. Readiness, dependency availability, startup/shutdown, failure response, persistence, and resource limits MUST be checked where the change affects them.
- Critical changed behavior MUST have a meaningful negative control. Mutation tests and fault injection MUST operate only in isolated, owned copies/environments.
- After mutation, observe actual resource identities and relevant state; use drift/repeat-convergence checks with coverage limitations recorded. A no-change result is not proof of availability or absence of unmanaged resources.

## 10. Evidence and findings — INF-10

- Every applicable requirement MUST map to a result: evaluated/pass, evaluated/fail, or unevaluated with a reason. Inapplicability is a separate selection decision, not a successful execution result.
- Evidence MUST bind the candidate identity, tool/binding version, build and target environments, authority reference, check/operation, timestamps, observed effects, and output completeness. Relevant changes invalidate reuse.
- Raw sensitive artifacts MUST remain in protected storage; model-visible summaries MUST be bounded and sanitized before persistence. Plaintext secret hashes can reveal low-entropy values; use opaque secret versions/references or an appropriate protected keyed identity.
- Reports MUST retain the first established blocker and later outcomes, including token termination, timeout, and cleanup failure. A later terminal reason cannot erase the cause of lost progress.
- Tool output and agent statements are inputs to validation, not authority to declare a gate passed. Partial/truncated/unavailable evidence MUST remain identifiable.

## 11. Composition and proportionality — INF-11

- Select profiles by operation, resource family, tool, build environment, and target requirements. Cloud provider alone is not sufficient: Terraform on Azure needs Terraform state rules and Azure target identity rules.
- Required security/architecture rules MUST remain in force. Do not duplicate their rule sets into every tool binding. Additional compliance profiles MUST identify exact releases, applicability, inherited controls, and evidence owners.
- Each delivery slice MUST name its reviewers and complete acceptance boundary. Common rules SHOULD be shared, but unrelated tools MUST NOT be forced into one generic execute/rollback API.
- Reviewers receive the applicable canon sections and evidence references. The existing independent review process remains; a profile does not create an extra mandatory reviewer or waive one.

## 12. Support and versioning — INF-12

- A profile/binding MUST distinguish designed, implemented, and verified support. A documented CLI flag or offline fixture alone is not certification of the selected execution boundary.
- Enabling a binding MUST require a pinned compatibility matrix, positive and negative acceptance evidence, interruption behavior, and known limitations. Changed versions or relevant environment settings require scoped recertification.
- Unknown tool features, unsupported targets, or contradictory profiles MUST fail explicitly. Never silently substitute a default provider, environment, or weaker check.

## Required agent plan

```text
Outcome and acceptance boundary:
Applicable canon/profile versions:
Existing components and artifacts to reuse:
Resource owners and dependency graph:
Build environment and target identity:
Source/dependency/artifact identities:
Declared execution authority and approval boundary:
Preflight and blocked behavior:
Preview type, coverage, and unknowns:
State, locks, data retention, and recovery:
Verification matrix and negative controls:
Reviewers and bounded work division:
Evidence destination and validity conditions:
```

## Construction procedure

1. Define outcome and resource ownership; select profiles and environments.
2. Inspect bounded source and known state; identify reusable modules and current tooling.
3. Establish the authorized verification path and deterministic preflight before model work depends on it.
4. Bind versioned inputs; implement one cohesive slice with its tests and cleanup.
5. Produce preview/change evidence and independent review under the existing contract.
6. If live mutation is needed, present the concrete change and obtain or validate its scoped authorization.
7. Execute through the owned binding, reconcile partial outcomes, and independently verify the resulting artifact or target.
8. Preserve results and recovery information; report the actual completed outcome.

## Required completion audit

- Are target identity, authority, ownership, and relevant locks established?
- Do the built and applied identities match what was reviewed?
- Were required checks executed through their supported paths, with no hidden gaps?
- Are secret-bearing inputs and evidence protected at every sink?
- Did partial failure, retry, cancellation, and cleanup preserve unrelated work and durable evidence?
- Is persistent data recoverable according to the declared objective?
- Does the reported outcome match actual artifact/target behavior?

Completion summary:

```text
Outcome achieved:
Candidate and resulting resource/artifact identities:
Applicable profiles and environment:
Checks passed / failed / unevaluated:
Authorization and execution evidence:
Unresolved blockers and preview gaps:
Recovery and retained state:
```

## Governing principle

Every infrastructure change has an owner, a target, an authority boundary, and an observable result. Make those explicit before the change acquires power; preserve them when the operation fails.
