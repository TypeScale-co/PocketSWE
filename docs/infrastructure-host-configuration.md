# Host Configuration Profile

## Purpose and applicability

Converge explicitly selected hosts to a declared configuration while preserving identity, authority, service availability, and recoverability. Apply with the [Infrastructure Canon](infrastructure.md). Initial binding design: Ansible. This profile is independent of whether hosts were created manually, by Terraform, or by a cloud-native template.

## 1. Inventory and authority — HOST-01

- Inventory source/version, resolved host identities, selection limits, connection method, principal, privilege escalation, and affected host resources MUST be explicit.
- Dynamic inventory and delegated/local tasks MUST be included in the authority boundary. A host limit alone does not prove all tasks execute only there.
- Host-key/identity verification MUST remain enabled through the approved connection mechanism. Unknown or changed host identity is a blocker.
- Mutating host preparation, package installation, daemon configuration, filesystem ownership, user/group changes, reboots, and services requires authorized scope. A prerequisite check MUST NOT silently perform those repairs.

Ansible delegation changes where work executes and which connection context applies. Include delegated hosts and the controller itself when assessing scope. [Ansible delegation](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_delegation.html)

## 2. Desired configuration and convergence — HOST-02

- Roles/modules SHOULD express a desired state with explicit ownership. Prefer supported idempotent modules to shell execution when their contract fits.
- Commands/scripts MUST declare preconditions, postconditions, changed/failure semantics, privilege, repeat safety, and bounded execution. `changed_when: false` cannot conceal a mutation.
- Templates, packages, collections, roles, plugins, and execution environment MUST be versioned. Configuration dependencies and handlers MUST be explicit.
- A repeat run MUST converge according to the declared contract. Zero reported changes alone does not prove correct state; inspect actual files, permissions, services, and required behavior.

## 3. Preview and execution limits — HOST-03

- Syntax/lint, check mode, diff mode, and real execution MUST have separate evidence. Unsupported check-mode tasks, dynamic conditions, and runtime-only values MUST remain visible as coverage gaps.
- Tasks forcing normal execution during check mode MUST be detected and classified as mutation. Connection, lookup, inventory, and callback plugins require controlled execution even during preparation.
- Check/diff output MUST NOT be treated as an executable immutable plan. Approval binds source, resolved inventory, variables, execution environment, privilege, permitted effects, and recheck conditions.

Ansible documents that unsupported modules can do nothing in check mode, conditional behavior may be unavailable, and `check_mode: false` can force changes even under `--check`. Diff can expose sensitive values. These limitations are why this binding requires coverage and authority checks outside a command-name allowlist. [Check and diff mode](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_checkmode.html)

## 4. Secrets and output — HOST-04

- Secrets MUST use protected references and the selected supported delivery mechanism. Secret-bearing tasks MUST suppress sensitive output and diff at the source.
- `no_log`/diff controls MUST be exercised with fabricated canaries through callbacks, failure output, debug settings, and retained artifacts. They are not blanket proof against all disclosure.
- Host facts, inventory, resolved variables, and backups MUST have bounded retention and appropriate access. They MUST NOT be indiscriminately copied to model context.

Ansible warns that debugging can expose values despite ordinary task logging controls. The framework therefore verifies the actual configured output path. [Ansible logging](https://docs.ansible.com/projects/ansible/latest/reference_appendices/logging.html)

## 5. Partial failure and recovery — HOST-05

- Batch size, permitted concurrent hosts, health gates, failure thresholds, handler behavior, reboot/disconnection policy, and abort criteria MUST be explicit.
- A failed host and a failed fleet operation MUST be distinguishable. Preserve per-host effects and uncertainty; do not mark unreachable hosts successful or automatically rerun all hosts.
- Handler ordering and partial configuration MUST be tested. Recovery may require restoring configuration and restarting a service; it is not a generic inverse playbook.
- Rescue/ignore logic MUST preserve required failure reporting and cannot turn missing acceptance into success.

Ansible normally stops on the failing host while other hosts can continue, and a later task failure can prevent a notified handler from running. Those defaults motivate explicit batch and partial-state behavior. [Ansible error handling](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_error_handling.html)

## 6. Ansible binding and verification — HOST-06

Resolve and pin the controller/execution environment, ansible-core, collections/roles, inventory plugins, configuration, source, variables, and target identities. Run syntax checking and a pinned lint policy, then coverage-aware check/diff in the authorized boundary. Prepare a bounded execution request; live execution follows the canon's approval rule.

On an authorized disposable host, apply once, inspect actual state, apply again, inspect again, and inject a controlled failure. Test partial host failure, service readiness, restoration, delegated scope, and cleanup. Ansible Lint supplies automation-content checks; it does not prove the desired state is achieved. [Ansible Lint](https://docs.ansible.com/projects/lint/)

Required negatives: wrong/expanded inventory; unexpected delegation or privilege escalation; check-mode mutation; misleading changed/failed conditions; unreachable host; suppressed handler after partial change; secret in callback/diff; repeated non-idempotent operation.

## Review questions and completion audit

1. Which hosts, delegated targets, controller resources, and privileges are in scope?
2. What does preview omit or actually execute?
3. Does repeat execution preserve the intended state and expose real changes?
4. What remains partially configured after a failure or reboot?
5. Does the result prove actual service behavior, not just a green task summary?

Acceptance cases: H01–H06 and applicable C cases in the [acceptance matrix](infrastructure-acceptance-matrix.md).
