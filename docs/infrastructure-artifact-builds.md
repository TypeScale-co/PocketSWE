# Artifact Build Profile

## Purpose and applicability

Produce an identifiable, inspectable artifact from declared inputs. Apply with the [Infrastructure Canon](infrastructure.md) when building a container image or comparable immutable package. Deploying that artifact additionally selects the [Workload Runtime Profile](infrastructure-workload-runtime.md).

A verified image is not a verified deployment. This profile's initial concrete binding is Docker/BuildKit on an explicitly selected local or remote builder; broader OCI implementations require separate compatibility evidence.

## 1. Build identity and context — IMG-01

- Source/patch identity, ordered build inputs, Dockerfile/frontend, build context, named contexts, dependency identities, target platform, and builder identity MUST be explicit.
- Exclusions MUST apply before material enters any build stage. Fixtures MUST demonstrate that credentials, databases/sidecars, unrelated worktrees, local dependencies, and generated output cannot enter an unauthorized context or layer.
- Base images used for accepted output MUST resolve to recorded digests. Builder/compiler dependencies and runtime dependencies MUST be distinguished. Rebuild/update policy MUST address vulnerability fixes without silently replacing an accepted digest.
- Minimal runtime contents SHOULD follow the application's actual needs. An application that executes build tools requires those tools; “minimal” is not a reason to remove a required runtime capability.

Docker documents context exclusions, multi-stage construction, and the trade-off between immutable base digests and automatic refresh. These mechanisms inform the proposed rules; they do not alone prove a hermetic or bit-for-bit reproducible build. [Docker build practices](https://docs.docker.com/build/building/best-practices/)

## 2. Builder authority — IMG-02

- Docker/BuildKit access MUST be brokered through the selected owned runner. Direct access to a shared daemon MUST NOT be inferred from permission to edit a Dockerfile.
- Build network, privileged entitlements, host binds, devices, SSH forwarding, and secret mounts MUST be independently declared. Unneeded capabilities MUST remain unavailable.
- Build instructions execute code. A untrusted build MUST NOT run with unrestricted host/daemon access merely because the operation only intends to produce an image.
- Builder/cache ownership, concurrency, time, disk, and output limits MUST be enforced. Failure cannot authorize global image/cache pruning.

Docker identifies daemon access as a substantial host authority boundary. Rootless operation or a dedicated builder can reduce exposure but does not remove the need to validate the complete chosen boundary. [Docker Engine security](https://docs.docker.com/engine/security/)

## 3. Secrets and provenance — IMG-03

- Build secrets MUST use the supported secret/SSH mechanism where necessary; they MUST NOT be put in ARG/ENV, COPY inputs, command output, or committed files.
- A secret mount is not proof that build code did not copy or print its content. Tests MUST inspect output artifacts and relevant retained build evidence using fabricated sentinels.
- Final digest, platform, dependency inventory, and provenance MUST be recorded. Attestations MUST be bound to the artifact they describe; presence alone does not prove a trusted builder or clean contents.
- Publishing, signing with a release identity, or updating a mutable registry tag MUST be separate authorized effects. Validation may prepare these actions without executing them.

Docker's build-secret mounts avoid the persistence behavior of ordinary build arguments/environment variables. Attestations can carry provenance and SBOM information, but their storage/export behavior depends on the selected exporter/image store and must be verified. [Build secrets](https://docs.docker.com/build/building/secrets/), [build attestations](https://docs.docker.com/build/metadata/attestations/)

## 4. Artifact acceptance — IMG-04

- Native syntax/build checks MUST precede expensive build work where supported. They do not replace an actual build and executable smoke check.
- Acceptance MUST verify the final artifact's platform, entry point, required files/tools, runtime user, startup/health, signal handling, and relevant dependencies in a disposable supported boundary.
- Cross-compilation or emulation MUST be labeled. GPU, kernel, device, filesystem, or native-library behavior requires representative target evidence when the application depends on it.
- Negative controls MUST include wrong platform/entrypoint or missing required contents and a forbidden-context/layer sentinel. Artifact identity MUST change when the candidate changes.

## 5. Lifecycle and cleanup — IMG-05

- Artifact output and evidence MUST survive disposable builder/session teardown. Temporary tags and containers MUST carry verified ownership; retain the accepted digest or export before cleanup.
- Build success followed by export/persistence failure MUST remain incomplete. An artifact that cannot be retrieved and matched by digest is not deliverable.
- Repeated builds SHOULD demonstrate declared reproducibility expectations; nondeterministic metadata and external dependencies MUST be disclosed rather than hidden by a vague reproducibility claim.

## Docker/BuildKit binding

| Stage | Required behavior | Evidence limit |
| --- | --- | --- |
| Resolve | Pin builder/context, platform, Dockerfile/frontend, dependencies, contexts, and declared network/secrets | Local CLI defaults are not target proof |
| Validate | Use the selected version's supported build checks and policy checks | A check may need frontend/dependency resolution; execute it under the same input-trust policy |
| Build | Execute with bounded resources and export policy | Build success is not runtime acceptance |
| Inspect | Capture immutable image/export identity; inspect config, inventory, provenance, and forbidden contents | A final filesystem scan alone can miss earlier layers or build metadata |
| Smoke | Run the exact artifact under declared disposable authority | No deployment to shared/live services is implied |
| Deliver | Preserve the artifact and evidence; publish only if authorized | Publishing authority is distinct from building |

The selected Buildx version must be tested for its supported `--check`/call modes, platforms, secret mechanisms, and output handling. This design does not prescribe an unverified universal command line. [Buildx command reference](https://docs.docker.com/reference/cli/docker/buildx/build/)

## Review questions and completion audit

1. Which exact source, builder, dependencies, and platform produced this digest?
2. Could a forbidden file enter any context, stage, cache, or attestation?
3. Did validation require more authority than the build was permitted?
4. Was the exact final artifact exercised, including failure behavior?
5. Is accepted output retrievable after cleanup, and was publication separately authorized?

Acceptance cases: A01–A06 and applicable C cases in the [acceptance matrix](infrastructure-acceptance-matrix.md).
