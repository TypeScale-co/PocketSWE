# Declarative Provisioning Profile

## Purpose and applicability

Manage infrastructure resources through explicit desired state, ownership, preview, controlled mutation, and observed convergence. Apply with the [Infrastructure Canon](infrastructure.md). This profile defines common obligations and separate Terraform, CloudFormation, and Bicep bindings. It does not introduce a universal resource model or pretend every tool provides an executable saved plan.

## Common provisioning rules

### Ownership and composition — PROV-01

- Resource/module ownership, state/stack boundaries, dependency edges, external references, and lifecycle coupling MUST be explicit. One resource property cannot have competing reconcilers.
- Existing resources MUST be adopted/imported only through an approved ownership transfer. Discovery does not grant authority to replace or destroy an unmanaged resource.
- Modules SHOULD expose stable application-relevant outputs and validated inputs. Split state/deployment units at lifecycle, authority, or failure boundaries, not at arbitrary file counts.

### Target, identity, and inputs — PROV-02

- Actual provider account/tenant/subscription, region, deployment scope, state/backend, and execution principal MUST match the declared environment.
- Source, modules/providers, parameters, policy, and referenced external artifacts MUST be versioned and bound to preview/execution evidence. Sensitive inputs use protected references and value handling.
- Read/plan credentials and apply credentials SHOULD be separated where the tool supports it. Provider plugins, data sources, custom resources, macros, scripts, and external programs retain their own execution risks.

### Change and drift — PROV-03

- Preview MUST expose create/update/delete/replace/import effects and unknown/unsupported coverage. Material destructive uncertainty blocks execution.
- Relevant drift and concurrent changes MUST be evaluated before applying; no drift report is assumed complete for unsupported resources/properties.
- Lifecycle protection, retain/snapshot behavior, replacement ordering, and dependencies MUST be reviewed for stateful resources. A declared retain flag is not a backup or restore test.

### State and concurrency — PROV-04

- State/stack ownership, lock semantics, operation identity, durable partial results, and recovery MUST be tool-specific and tested.
- Local process failure MUST be distinguished from remote operation status. Reconcile before replay, destroy, force-unlock, rollback, or import.
- Preview and apply MUST observe the relevant state/context identity; source or material target changes invalidate prior authorization/evidence according to the binding.

### Acceptance and cost — PROV-05

- Syntax, policy, preview, actual provisioning, and service acceptance MUST have separate results. Quota, permissions, regional capabilities, and cost/resource limits MUST be checked where required; an estimate is not a guaranteed bill.
- Apply and recovery testing MUST use explicitly authorized resources. A command named `test` is not exempt from mutation approval or disposal rules.
- Post-apply checks MUST observe required resource properties and service behavior, followed by drift/repeat checks with coverage identified. Validate recovery of stateful fixtures separately from deletion of disposable ones.

## Terraform binding

**TF-01 — Dependency and initialization contract.** Pin CLI/provider compatibility, commit the dependency lock file, and explicitly version modules. The Terraform lock file tracks provider selections; module version selection needs its own controls. Initialization/provider execution MUST run through the approved input and credential boundary. [Terraform dependency lock](https://developer.hashicorp.com/terraform/language/files/dependency-lock)

**TF-02 — Validation and plan.** Formatting/validation and policy checks precede a target-bound plan. Capture plan mode, source/parameter identity, provider/backend/workspace identity, state context, replacements/destruction, and unresolved values. Treat saved plans and JSON representations as sensitive. Terraform can store sensitive values in a saved plan even when terminal output hides them. [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)

**TF-03 — Apply the approved plan.** Where the workflow produces a saved plan, execute that exact protected artifact, not a newly generated implicit plan. Verify integrity and selected context; stale or rejected plans require a new plan/review. A saved plan narrows intended actions but does not guarantee the external environment is unchanged or application acceptance succeeds.

**TF-04 — State and recovery.** Require a verified locking and access model for the chosen backend and ownership boundary. Lock timeout is a blocker; do not disable locking or force-unlock to make a build proceed. Record state lineage/version where available, protect snapshots, and reconcile partial apply. A configuration rollback may itself plan destructive changes. [Terraform state locking](https://developer.hashicorp.com/terraform/language/state/locking)

**TF-05 — Tests.** Distinguish validation, plan-based tests, mocked provider tests, and real apply-based tests. Terraform tests default to apply behavior in run blocks and can create real infrastructure. Bind fixture identity, permissions, cost, cleanup, and leak detection before executing them. Mocked tests cannot certify provider behavior. [Terraform tests](https://developer.hashicorp.com/terraform/language/tests)

Required negatives: wrong workspace/account/backend; stale/tampered plan; conflicting writer; state lock unavailable; hidden replacement; provider observation incomplete; apply response lost; fixture cleanup fails. A module/provider operation requiring unsupported credentials remains unevaluated.

## AWS CloudFormation binding

**CF-01 — Template and scope.** Bind template/parameters, nested templates, macros/transforms/custom resources, account, region, stack identity, service role, and acknowledged capabilities. Schema/lint and policy validation use a pinned supported tool/ruleset. IAM capabilities are acknowledgements, not a substitute for resource-level authorization. [cfn-lint](https://github.com/aws-cloudformation/cfn-lint), [CloudFormation Guard](https://docs.aws.amazon.com/cfn-guard/latest/ug/what-is-guard.html)

**CF-02 — Change sets.** Create and inspect the intended change set, including replacements and nested/custom behavior; execute the approved change-set identity. Creating a change set is a control-plane effect needing appropriate permission, even when no target resource deployment is performed. AWS explicitly states that a change set does not guarantee a successful update. Missing permissions, quotas, and unsupported behavior remain possible. [CloudFormation change sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html)

**CF-03 — Drift coverage.** Record unsupported resources/properties and check nested stacks separately when required. A stack can report IN_SYNC despite resources without drift support; do not turn that into complete coverage. Optional newer drift-aware features require their own selected-version contract. [CloudFormation drift](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html)

**CF-04 — Lifecycle.** Set and verify appropriate removal and replacement handling for stateful resources. `DeletionPolicy` and `UpdateReplacePolicy` govern different paths; neither alone proves data recovery. The framework requires inspection of both applicable paths, not blanket `Retain` on every disposable resource. [DeletionPolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-deletionpolicy.html), [UpdateReplacePolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-updatereplacepolicy.html)

**CF-05 — Remote operation.** Persist stack/change-set/operation identity and events before declaring success. Monitor to an authoritative terminal state and then perform application acceptance. Timeout, rollback, rollback failure, and partial custom-resource effects need distinct recovery. Do not assume killing the CLI stops the stack operation.

Required negatives: wrong stack/account; incomplete nested preview/drift; denied execution role; unexpected replacement; rollback failure; retained orphan resources; custom resource with uncertain side effects. Protect parameter/output evidence from secret disclosure.

## Azure Bicep / ARM binding

**BCP-01 — Compile and scope.** Bind Bicep/CLI version, modules, compiled template, parameters, API versions, tenant/subscription, deployment scope/name, deployment mode, and principal. Compile/lint validates source rules; it does not certify target behavior. [Bicep linter](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/linter)

**BCP-02 — What-if coverage.** Capture the selected tool's diagnostics and all incomplete/ignored/short-circuited resources. What-if can be unable to analyze resources or modules; newer CLI versions expose diagnostic information that older versions may omit. Required unresolved effects need further evidence or a narrower operation. [Bicep what-if](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-what-if)

**BCP-03 — Advisory preview.** Do not represent what-if output as a Terraform-style executable saved plan. Approval binds the source/compiled template, parameters, scope, mode, and preview observations. Recheck before deployment and compare meaningful changes; serialize owned deployment operations and disclose residual external race/preview limitations.

**BCP-04 — Lifecycle semantics.** Incremental deployment is not a partial patch of each property: omitted properties can reset. Deliberate resource deletion must use the selected supported lifecycle mechanism with explicit ownership and approval. Microsoft currently recommends deployment stacks for deletions and discourages complete mode; legacy complete-mode support requires a separately reviewed profile. [ARM deployment modes](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/deployment-modes)

**BCP-05 — Remote operation and recovery.** Preserve deployment-operation identity and status; reconcile partial effects and validate actual resources. Replacement, rollback/redeployment, orphan cleanup, and data restore have different contracts. A successful deployment response cannot replace workload acceptance.

Required negatives: wrong subscription/scope; what-if short circuit; mutable module/template inputs; property reset; unexpected removal; failed deployment with partial resources; client timeout while ARM continues.

## Extension boundary

Terraform, CloudFormation, and Bicep may target overlapping resources, but MUST NOT simultaneously own the same properties. A move between tools is an explicit state/ownership migration, not a second profile casually added to the same deployment. OpenTofu, Pulumi, Crossplane, CDK synthesis, Kubernetes, and other tools can be added through independently verified bindings; this document does not certify them by analogy.

## Review questions and completion audit

1. Who owns each resource/property, and which state or service records that ownership?
2. What will be created, replaced, deleted, or left unknown?
3. Does execution consume the approved plan/change set, or only an advisory preview?
4. Which resources and properties were actually checked for drift?
5. What continues remotely after a client timeout, and how is it reconciled?
6. Can the stateful fixture actually be restored, and are test resources bounded and owned?

Acceptance cases: P01–P08 and applicable C cases in the [acceptance matrix](infrastructure-acceptance-matrix.md).
