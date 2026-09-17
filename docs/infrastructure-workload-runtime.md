# Workload Runtime Profile

## Purpose and applicability

Run accepted artifacts with explicit configuration, exposure, storage, health, and recovery behavior. Apply with the [Infrastructure Canon](infrastructure.md); select the [Artifact Build Profile](infrastructure-artifact-builds.md) only if the work also produces images. Initial binding: Docker Compose on an explicitly identified Linux host/daemon.

## 1. Composition and target identity — RUN-01

- The complete effective composition MUST be determined from explicit ordered files, profiles, parameter/secret references, image digests, and target daemon identity.
- A deterministic project/namespace identity MUST separate disposable verification from the live deployment. Explicit names, external networks/volumes, and host binds MUST be checked for collisions even when the Compose project name differs.
- Services MUST own coherent runtime responsibilities and communicate through declared interfaces. The number of services follows application requirements; “exactly two” is specific to the CE deployment request, not a universal infrastructure rule.
- Configuration resolution MUST use a controlled environment. Shell variables, implicit dotenv discovery, active contexts, or working-directory defaults MUST NOT redirect the reviewed deployment.

Compose project names provide useful namespacing, while interpolation precedence affects the resolved configuration. Both require explicit inputs for a stable review target. Rendered configuration may contain sensitive values and must not be dumped into ordinary logs. [Project names](https://docs.docker.com/compose/how-tos/project-name/), [Compose interpolation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/)

## 2. Runtime authority and exposure — RUN-02

- UID/GID, filesystem writes, capabilities, devices, secrets, network access, published interfaces, and resource limits MUST be explicit and minimal for the workload.
- The local/DGX baseline MUST publish only to explicit loopback addresses unless the operator approves another exposure profile. Network tests MUST observe the actual published bindings.
- Host sockets, privileged mode, host namespaces, arbitrary mounts, and GPU devices MUST NOT be enabled merely to make acceptance pass.
- Required authentication homes MUST preserve the application's trust checks. Mounting an entire credential home read-write needs a documented runtime requirement and separately authorized scope; prefer narrower supported mounts.

## 3. Storage and lifecycle — RUN-03

- Application data, project checkouts, build workspaces, fixture roots, and disposable scratch MUST be disjoint and owned by the intended runtime identity. Durable state MUST NOT be confined to an image layer or temporary session directory.
- Mount type, source identity, permissions, retention, backup/restore, migration compatibility, and retirement policy MUST be recorded for every stateful boundary.
- Restart, recreation, and version rollback MUST preserve intended state. A destructive down/volume removal MUST require explicit disposal authority; it is not the standard retry path.
- Application rollback MUST declare compatibility with stored data. Image rollback alone MUST NOT be described as restoring an earlier database state.

## 4. Readiness and failure behavior — RUN-04

- Startup order, readiness, and ongoing health MUST be distinguished. Dependencies MUST have a bounded readiness contract; the application MUST also handle subsequent dependency loss.
- Verification MUST cover configuration translation, client-to-service access, actual health, process termination, restart/recreation, and resource limits where relevant.
- Readiness and health failures MUST preserve useful bounded evidence and prevent false completion. Neither a process list nor an HTTP response from the wrong existing service is valid evidence.

Compose distinguishes container start order from readiness and supports health-based dependencies. This informs the startup checks; it does not supply an ongoing application dependency-recovery contract. [Compose startup and shutdown order](https://docs.docker.com/compose/how-tos/startup-order/)

## 5. Preview and authorization — RUN-05

- Compose configuration and diff/preview features MUST be classified as advisory unless a specific stronger execution contract has been verified. Rendered YAML is not a transactional executable deployment plan.
- Before live `up`, replacement, down, scale, publication, or host preparation, approval MUST identify effective configuration, exact images, daemon/project, affected mounts/ports, persistence effects, and the deployment/recovery procedure.
- Re-resolve and compare material inputs immediately before mutation. Lock the relevant deployment namespace against competing CE operations and check for external changes; disclose that the daemon does not make a multi-service rollout an atomic transaction.
- Deployment timeout/cancellation MUST reconcile actual containers, networks, volumes, and health before retry. Preserve partial results.

## 6. Acceptance and cleanup — RUN-06

- An owned disposable fixture MUST prove create, health, dependency failure, graceful stop, restart, recreation with retained data, and cleanup without touching a neighboring fixture.
- Negative tests MUST detect wrong image identity, unintended port exposure, wrong mount ownership, lost persistence, and insufficient readiness.
- Cleanup MUST use recorded resource identities plus current ownership checks. Project labels alone are insufficient when external/shared resources are present.
- Live acceptance MUST observe the actual deployed artifact and required user workflow. Fixture success qualifies the mechanism, not the current live state.

## Docker Compose binding and local/DGX boundary

Docker/Compose versions, daemon/context, supported configuration fields, architecture, filesystem semantics, and renderer behavior are compatibility inputs. Validate the resolved model before any resource mutation. Prepare a bounded execution request containing the ordered files and their identities, resolved nonsecret values, protected secret references, image digests, project identity, volume/network ownership, and operation limits.

Container creation for acceptance occurs only on an authorized disposable runner. If CE's agent sandbox cannot reach that runner, report the readiness blocker; do not expose the daemon to all agents. The actual shared DGX is a live target unless explicitly designated otherwise. No deployment commands are executed by this design package.

A DGX profile MUST record the actual CPU architecture and whether GPU access is required. When required, the driver/container-toolkit/device compatibility and native GPU workload need separate checks. A generic container smoke check cannot certify them. [NVIDIA Container Toolkit prerequisites and configuration](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

## Review questions and completion audit

1. Which daemon, project, images, configuration, and state would change?
2. Can the same deployment command accidentally target a neighboring stack?
3. Are process health, readiness, persistence, and user-visible behavior all proven?
4. What remains after partial rollout or cancellation, and how is it reconciled?
5. Which actions are approved, and which data may cleanup actually delete?

Acceptance cases: W01–W07 and applicable C cases in the [acceptance matrix](infrastructure-acceptance-matrix.md).
