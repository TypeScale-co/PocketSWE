# Infrastructure framework acceptance matrix

Status: implementation acceptance design, not executed certification. Every binding must select the applicable cases and add target-specific cases. The common canon owns rule meaning; this matrix defines observable evidence and negative controls.

Use existing review severities. An executed violation fails the applicable gate; an unavailable required check is unevaluated and blocks the affected completion claim. An excluded profile needs an applicability reason, not fabricated passing results.

## Common contract

| ID | Rule | Positive evidence | Negative/interruption case and required result |
| --- | --- | --- | --- |
| C01 | INF-01, INF-11, INF-12 | Exact operation selects only required profiles and certified binding versions | Unknown tool, conflicting profiles, or missing target blocks affected execution; unrelated projects remain unchanged |
| C02 | INF-01, INF-04 | Actual target and principal match the approved packet | Switch Docker context, account, subscription, or inventory after review: zero unauthorized mutations |
| C03 | INF-02, INF-04, INF-05 | Execution uses bound source/parameters/artifact/plan | Modify artifact, parameters, protected secret version, module, or policy: invalidate relevant evidence/approval |
| C04 | INF-03 | Controlled probes pass through the actual runner | Deny scratch, trusted fixture root, loopback, daemon, dependency access, or lock: specific blocker, zero dependent model launches/repair charges |
| C05 | INF-04 | An unchanged operation proceeds within an existing explicit valid grant | Missing/expired/revoked/out-of-scope authority causes no mutation; repeated approval is not demanded for already-covered work |
| C06 | INF-05, INF-10 | Preview records complete/partial coverage and exact/advisory semantics | Unknown resource/short circuit/unsupported check never becomes no-change/pass |
| C07 | INF-06 | Competing writers are serialized at the real resource boundary | Concurrent CE run or external change causes wait/recheck/refusal, not silent overwrite |
| C08 | INF-07 | Operation result is durable and resumable | Drop response after remote acceptance: reconcile once by operation/resource identity; do not replay mutation blindly |
| C09 | INF-07, INF-08 | Cancellation settles owned work and preserves recovery state | Kill CLI while remote work continues: report unknown/in-progress until authoritative reconciliation; never claim rollback from process exit |
| C10 | INF-08 | Data and execution state survive restart and tested restore | Destroy disposable runtime/session storage: required evidence/data still recoverable; expose incomplete backup/restore |
| C11 | INF-10 | Bounded sanitized result plus protected evidence reference | Canary secret in plan/state/config/diff/error/callback never reaches model-visible or ordinary durable logs; truncation stays explicit |
| C12 | INF-07, INF-10 | Original blocker and later terminal outcomes both retained | Token/time ceiling after known blocker must not erase cause, partial changes, or cleanup status |
| C13 | INF-07, INF-09 | Negative controls act only on owned fixtures | Neighboring project/resource sentinel remains untouched after timeout, cancellation, and cleanup |
| C14 | INF-09, INF-10 | Acceptance observes exact resulting artifact/target | Healthy response from old service or wrong digest cannot pass candidate acceptance |
| C15 | INF-10, INF-12 | Evidence reuse matches version, inputs, environment, scope, and freshness policy | Change a relevant dependency/tool/permission/target observation: scoped revalidation; unchanged valid evidence is not needlessly regenerated |
| C16 | INF-01, INF-04 | Prepared-source outcome completes with truthful validation scope | A live-deployment North Star cannot close based only on source/lint/image success |

## Artifact builds

| ID | Rules | Required proof |
| --- | --- | --- |
| A01 | IMG-01 | Record source/context/frontend/base/platform identities; changing a relevant input invalidates evidence |
| A02 | IMG-01, IMG-03 | Fabricated forbidden file excluded before context/stage entry; attempted layer/metadata leakage is detected |
| A03 | IMG-02 | Unauthorized host bind, privileged entitlement, device, network, or shared-daemon target is refused |
| A04 | IMG-04 | Exact artifact runs required entrypoint/health/user/tool checks; wrong architecture, missing tool, or broken entrypoint fails |
| A05 | IMG-03, IMG-05 | Image/export digest and required attestations remain retrievable after builder/session cleanup; output-store failure remains incomplete |
| A06 | IMG-03, IMG-05 | Build and smoke authority does not allow registry publish or global prune; accepted output and neighboring artifacts survive cleanup |

## Workload runtime

| ID | Rules | Required proof |
| --- | --- | --- |
| W01 | RUN-01, RUN-05 | Ordered files/interpolation/profiles resolve identically under controlled inputs; ambient variable/context changes cannot redirect execution |
| W02 | RUN-01, RUN-02 | Test namespace avoids live names, external volumes/networks, binds, ports, devices, and privileges |
| W03 | RUN-03 | Written fixture data survives restart and recreation; read/write ownership is correct; UI/stateless service cannot access protected state |
| W04 | RUN-04 | Dependency not ready, dependency lost, process stuck, and graceful shutdown tested; startup order alone cannot pass readiness |
| W05 | RUN-05 | Live command cannot execute before scoped approval; source/image/target change invalidates the relevant packet |
| W06 | RUN-03, RUN-06 | Interrupted partial rollout is reconciled; owned cleanup preserves retained data and neighboring services |
| W07 | RUN-04, RUN-06 | Actual image/platform and external workflow verified; GPU acceptance added only when required; emulation limitations recorded |

## Provisioning bindings

| ID | Rules | Required proof |
| --- | --- | --- |
| P01 | PROV-01, PROV-02 | Wrong ownership/account/backend/scope and competing tool ownership are refused before mutation |
| P02 | TF-01–TF-04 | Saved plan integrity, backend locking, stale-plan refusal, module/provider identity, and partial-apply recovery |
| P03 | TF-05 | Real-resource tests cannot run under validation-only authority; mocked/plan tests do not claim real provider qualification |
| P04 | CF-01–CF-03 | Correct change-set/stack identity, nested/unsupported coverage, and service-role failures are visible; no execute of an unapproved change set |
| P05 | CF-04, CF-05 | Separate removal/replacement retention paths and failed rollback/custom-resource uncertainty preserve actionable recovery |
| P06 | BCP-01–BCP-04 | Correct compiled template/scope, what-if gaps, advisory approval binding, property-reset/deletion effects |
| P07 | BCP-05, PROV-04 | Client timeout while cloud operation proceeds does not trigger duplicate deployment or false cancellation |
| P08 | PROV-03–PROV-05 | Quota/cost boundary, unexpected replacement, partial resources, drift coverage, recovery, and leftover-resource accounting |

## Host configuration

| ID | Rules | Required proof |
| --- | --- | --- |
| H01 | HOST-01 | Pinned resolved inventory and verified host identities; unexpected delegation/local mutation/privilege is blocked |
| H02 | HOST-02, HOST-06 | Apply then repeat on a disposable host; verify actual desired state both times; misleading change reporting fails |
| H03 | HOST-03 | Unsupported check-mode tasks and forced normal execution detected; check/diff cannot silently become mutation authority |
| H04 | HOST-04 | Fabricated secrets do not leak through diff, callbacks, debug, failure, or retained facts |
| H05 | HOST-05 | Partial batch failure, unreachable host, pending handler, and reboot/disconnection preserve per-host state and health gates |
| H06 | HOST-05, HOST-06 | Bounded recovery restores the declared configuration/service behavior; unrelated hosts and persistent data remain unchanged |

## Minimum local/DGX qualification sequence

1. Use a neutral fixture with one small image and then a small persistent workload. Run common/artifact cases first; no CE real-agent session is needed to qualify the primitive boundary.
2. Introduce denied filesystem/socket/daemon conditions through a controlled test boundary. Verify exact blockers without relaxing permissions.
3. Verify authorization and target binding using a fake mutation adapter plus a real designated disposable daemon. A fake proves call refusal; the real daemon proves actual isolation/ownership semantics.
4. Verify workload restart, recreation, health, partial failure, and scoped cleanup. Keep a neighboring sentinel workload/data object throughout.
5. Record pinned runtime/profile compatibility and evidence. Only then enable the supported path for an independently approved CE deployment attempt.
6. Test CE's actual two-container application criteria separately, including durable workspaces, authentication contract, browser/HTTP operator behavior, and real-agent delivery after the existing blockers are resolved.

## Certification record shape

```text
Case and rule IDs:
Candidate/profile/tool versions:
Build runner and actual target identity:
Execution authority reference:
Positive/negative/failure scenario:
Expected and observed effects:
Result: passed | failed | unevaluated
Coverage and truncation/unsupported limits:
Protected evidence references:
Recovery/cleanup outcome:
Reviewer and independent acceptance references:
```

Fixtures and cases must be meaningful at their real boundary. Do not write a test that merely asserts a command string appears in generated instructions or that a reviewer said a rule passed.
