# Environment selection and composition

## Purpose

Select only the framework contracts needed for an operation while preserving the distinction between where a change is built, where it runs, and who may execute it. This is a design for a portable declaration; it is not a new CE configuration format implemented today.

## Selection dimensions

| Dimension | Examples | What it determines |
| --- | --- | --- |
| Requested outcome | Prepared source; verified image; verified deployment | Required completion and acceptance boundary |
| Resource/operation family | Artifact build; workload runtime; provisioning; host configuration | Required profile(s) |
| Tool binding | Docker/BuildKit; Compose; Terraform; CloudFormation; Bicep; Ansible | Native validation, preview, state, execution, and reconciliation semantics |
| Build environment | Local workstation; DGX; CI worker; remote isolated builder | Toolchain, scratch/cache, platform, dependency access, daemon/network/fixture authority |
| Target environment | Named local daemon; DGX host; AWS account/region; Azure tenant/subscription/scope; host inventory | Actual target identity, ownership, state, connectivity, accepted effects |
| Lifecycle/data | Disposable fixture; stateless workload; persistent service; imported infrastructure | Retention, cleanup, replacement, backup/restore, recovery evidence |
| Authority | Generate/validate/prepare; bounded disposable execution grant; approved live operation | Which concrete effects the runner may perform |
| Exposure and assurance | Loopback-only; private network; public service; explicit compliance profile | Security overlays, transport rules, evidence and review requirements |
| Hardware/network constraints | amd64/arm64; GPU required/absent; online/offline; proxy/mirror | Compatibility and required native/cold-cache verification |

“Docker” does not identify a target. “AWS” does not identify a provisioning tool. “CI” does not imply disposable resources. “Local” does not imply safe mutation: the local daemon can host persistent user services.

## Deterministic selection procedure

1. Read the approved outcome and explicit operation inventory. Bound discovery to declared paths; detect likely tools without traversing secret homes, databases, dependency trees, or unrelated state.
2. Resolve operation-to-profile closure: building an image selects artifact rules; deploying it selects workload rules; provisioning its hosts selects provisioning; changing host configuration selects host configuration. Fetching a previously accepted image requires identity verification but not claiming a new build.
3. Resolve exact tool bindings and their supported versions/features. A familiar extension is not proof of a supported interpreter or renderer.
4. Load the build and target declarations independently. Read-only credential/daemon/host identity checks must confirm the selected target before any affected mutation.
5. Add declared exposure, persistence, hardware, and compliance obligations. Compliance scope is explicit; do not infer a STIG release or public-cloud authorization from the operating system name.
6. Detect missing values, conflicting rules, overlapping resource/property writers, unsupported preview coverage, and absent execution authority. Return actionable blockers for the affected operation.
7. Freeze the effective profile versions and declaration digest with the candidate evidence. Treat subsequent material changes as invalidation, not a silent settings refresh.

A selection result records each applied rule and each scope-based inapplicability. Nothing applicable is dropped because its test cannot run. Non-infrastructure projects keep their existing framework behavior.

## Default authority selected by the operator

The design default is generation, validation, and preparation, with operator approval before changing live infrastructure. This does not imply all preview tools are safe under live credentials.

- Local source checks may run in an owned bounded workspace under the existing authorization.
- Artifact builds and test-container creation require a designated builder/test runner and explicit bounded execution authority. If no such runner is registered, prepare the candidate and report verification unevaluated.
- Authenticated discovery and service-managed preview creation use narrowly scoped permissions. A preview that runs custom code or creates control-plane objects must disclose those effects.
- Live apply, stack deployment, host preparation, registry publication, state adoption/migration, and destructive cleanup are separate effects requiring approval.
- Existing explicit approval remains valid within its recorded target, inputs/effects, lifetime, and retry conditions. Material change, revocation, or expired authority invalidates it. Do not repeatedly prompt for the same unchanged authorized operation.

## Illustrative local/DGX declaration

The values below deliberately leave host-specific identities unresolved. They are examples for later schema design, not valid CE settings, a runnable deployment, or claims about this machine's DGX hardware.

```yaml
design_example_version: 1
outcome: verified_deployment
profiles:
  - infrastructure-core@1
  - artifact-builds@1
  - workload-runtime@1
bindings:
  artifact: docker-buildkit
  workload: docker-compose
application:
  id: ce-turbine
  topology: exactly-two-services  # Application requirement, not a core rule.
  persistent_service: api
  stateless_service: operator-ui
build_environment:
  runner_identity: OPERATOR_SELECTED_BUILDER
  toolchain_manifest: VERSIONED_MANIFEST_REFERENCE
  source_identity: COMMIT_AND_PATCH_IDENTITY
  platform: EXPLICIT_BUILD_PLATFORM
  target_platform: EXPLICIT_TARGET_PLATFORM
  scratch_root: OWNED_SCRATCH_REFERENCE
  cache_root: OWNED_CACHE_REFERENCE
  trusted_fixture_root: OWNED_TRUSTED_FIXTURE_REFERENCE
  network_policy: DECLARED_DEPENDENCY_ENDPOINTS
target_environment:
  host_identity: OPERATOR_SELECTED_DGX_OR_LOCAL_HOST
  daemon_identity: VERIFIED_DAEMON_ENDPOINT_AND_IDENTITY
  compose_project: EXPLICIT_NONCOLLIDING_PROJECT
  exposure: loopback-only
  gpu_required: false  # Change only if the application actually requires it.
  state:
    database: DURABLE_DATABASE_ROOT_REFERENCE
    projects: DURABLE_PROJECT_ROOT_REFERENCE
    builds: DISJOINT_DURABLE_BUILD_ROOT_REFERENCE
  secret_sources: PROTECTED_RUNTIME_REFERENCES
  recovery_objectives: OPERATOR_DECLARED_OBJECTIVES
authority:
  default: generate-validate-prepare
  disposable_execution_grant: REQUIRED_BEFORE_TEST_RESOURCE_CREATION
  live_execution_approval: REQUIRED_BEFORE_LIVE_MUTATION
limits:
  operation_timeout: REQUIRED
  concurrency: REQUIRED
  disk_and_memory: REQUIRED
  evidence_output_and_retention: REQUIRED
  recovery_and_cleanup_allowance: REQUIRED
```

For a source-only proposal, the outcome may be prepared source and no live operation is authorized or required. For the original CE Docker deployment goal, source-only success cannot satisfy its runtime/persistence/operator-workflow acceptance.

The initial Docker example SHOULD use a tiny neutral fixture to qualify the mechanism before testing CE itself. CE's agent lifecycle, Go verification, and delivery problems must not become hidden prerequisites of every infrastructure framework fixture. A later CE application qualification explicitly adds real-agent operation and the full application acceptance criteria.

## Future combinations

| Target request | Required composition | What stays separate |
| --- | --- | --- |
| Build an OCI image on CI for DGX | Core + artifact + Docker binding; CI build and DGX platform declarations | Live Compose deployment |
| Run existing images on DGX | Core + workload + Compose binding | Image generation and cloud provisioning |
| Terraform creates AWS hosts; Ansible configures them | Core + provisioning/Terraform + host/Ansible; AWS target and host inventory | Terraform owns cloud resources; Ansible owns declared host properties |
| CloudFormation creates an AWS application stack | Core + provisioning/CloudFormation; AWS account/region/stack declarations | Terraform backend rules are not inherited |
| Bicep creates Azure resources | Core + provisioning/Bicep; Azure tenant/subscription/scope declarations | Terraform's saved-plan semantics are not assumed |
| Terraform manages Azure resources | Core + provisioning/Terraform; Azure target declaration | Bicep what-if and deployment-mode rules do not replace Terraform semantics |
| Ansible prepares a local Docker host | Core + host/Ansible; host target and privilege declaration | Docker daemon reconfiguration is a live host mutation |
| Air-gapped container build | Core + artifact + certified Docker binding; offline build overlay | Requires declared mirrors/bundles and freshness evidence; no fallback to public downloads |

## Approval packet

Before live execution, present a bounded human-readable packet backed by protected machine records:

```text
Requested effect and target identity:
Principal and resource/property scope:
Source, parameters, policy, tool, and artifact identities:
Preview type and identity (if executable/service-managed):
Creates / updates / replaces / deletes / imports:
Exposure, privilege, persistence, downtime, and cost implications:
Unknowns, preview coverage, and alternate evidence:
Preflight and independent review results:
Execution limits and validity/recheck conditions:
Partial-failure reconciliation and recovery:
Authorized cleanup scope and retained evidence:
```

The runner must verify the authorization against execution inputs, not merely record a boolean “approved” on a card. Exact plan equality is available only for bindings that support it. Advisory previews still require target rechecks and narrowly bounded effects.

## Decisions deferred until a concrete implementation target

The design is complete without guessing actual target values. Before implementation qualification, the operator/maintainer must supply builder and daemon identities, exact supported tool versions, architecture, GPU need, durable roots, exposure exceptions, fixture execution grant, operation limits, and recovery objectives. A cloud qualification additionally needs an approved account/subscription, region/scope, backend/stack ownership, quota/cost envelope, and disposal policy. Formal compliance needs a separately named applicable profile and release.
