# PocketSWE Security Canon

## Purpose

This document defines what secure implementation means under PocketSWE. It is the
Security Reviewer's canon and a secure-by-default design guide for the writing agent.
It complements `code-review.md`: that document defines how a review is conducted and
reported; this document defines the security properties being judged.

This is a software security baseline, not a penetration test, a formal assessment,
an authorization to operate, or a claim of compliance with a deployment standard.
A project or deployment may add a security profile, but a profile must name its
scope and provide evidence that source review cannot establish.

The baseline is informed by NIST SP 800-218 SSDF 1.1 and OWASP ASVS 5.0.0. ASVS
controls apply where the project is a web application or API. A project requiring
DoD controls may additionally declare an applicable DISA Application Security and
Development STIG release. STIG, ASVS, and SSDF are references, not substitutes for
the rules below.

## How to use this canon

- A MUST is a required security property unless the North Star explicitly makes it
  inapplicable.
- A MUST NOT is prohibited.
- A security finding must name the changed or reachable code, the trigger, the
  unintended behavior, and the impact.
- A reviewer may follow a data flow beyond the implementation diff when the diff
  changes a boundary or a caller's authority.
- A failure in authentication, authorization, validation, isolation, or integrity
  checking MUST fail closed. An unavailable check MUST NOT become an allow decision.

## 1. Threat model and boundaries

- The North Star or implementation plan MUST identify the important assets, actors,
  trust boundaries, and security-relevant assumptions for a feature that handles
  credentials, sensitive data, external input, privileged operations, or code
  execution.
- Every input crossing a process, network, user, file, plugin, agent, or privilege
  boundary MUST be treated as untrusted until validated.
- The implementation MUST name where validation, authentication, authorization,
  and normalization occur. A caller's claim that it already checked something is
  not proof at a new boundary.
- The implementation MUST preserve the narrowest authority needed for each actor,
  component, process, and credential.
- A failure in authentication, authorization, validation, isolation, or integrity
  checking MUST fail closed. An unavailable check MUST NOT become an allow decision.

## 2. Identity and authorization

- Authentication MUST establish the identity of the principal before a protected
  operation is performed.
- Authorization MUST be checked for the specific operation and resource, not only
  for entry to a general endpoint or process.
- The system MUST NOT trust user-controlled identity, role, tenant, path, or
  ownership fields as authorization evidence.
- Privileged operations MUST have one clearly owned authorization path. A legacy or
  sibling endpoint MUST NOT bypass the rules of the newer path.
- Credentials, tokens, and session identifiers MUST be protected in transit and at
  rest according to the application's declared threat model.
- Secrets MUST NOT be accepted in URLs, committed to source, embedded in fixtures,
  written to logs, or returned in ordinary error responses.

## 3. Input, output, and execution safety

- Inputs MUST be validated at the boundary where they first acquire meaning.
  Validation MUST cover type, length, format, range, cardinality, and nesting where
  each can affect behavior or resource use.
- The implementation MUST use parameterized queries or equivalent structured APIs.
  It MUST NOT construct commands, queries, templates, HTML, paths, or protocol
  messages by interpolating untrusted strings where a safe API exists.
- A process or shell invocation MUST use a fixed executable and an explicit argument
  list. Untrusted input MUST NOT become shell syntax.
- A path derived from external input MUST be confined to the intended root after
  normalization, and symlinks or alternate path forms MUST NOT escape that root.
- Deserialization MUST use an expected schema and bounded input. Unknown or
  dangerous fields MUST be rejected or handled explicitly.
- Output MUST be encoded for its destination. Data returned to a browser, command
  interpreter, log sink, or structured protocol MUST NOT be allowed to change the
  destination's syntax.
- Redirects, callbacks, URLs, and network destinations derived from input MUST be
  constrained to the allowed scheme, host, port, and purpose.

## 4. Data, secrets, errors, and logging

- The implementation MUST classify the sensitive data it handles and minimize
  collection, retention, copying, and exposure.
- Secrets and sensitive values MUST NOT appear in source control, prompts, generated
  instructions, logs, traces, metrics, crash reports, or test output unless the
  North Star explicitly requires a protected representation.
- Logs SHOULD record the security-relevant event and actor without recording the
  secret or unnecessary sensitive payload.
- Error responses MUST be useful to the intended caller without exposing credentials,
  internal paths, stack traces, tokens, query text, or other information that makes
  exploitation easier.
- Redaction MUST happen before a value reaches the sink. A later display filter is
  not sufficient protection for stored logs or telemetry.

## 5. Resources and isolation

- Every externally controlled operation MUST have explicit bounds on time, memory,
  input size, output size, recursion, concurrency, retries, or other resources that
  can be exhausted.
- The implementation MUST avoid unbounded buffering, pagination, fan-out, retries,
  polling, or recursive work based on attacker-controlled values.
- Code execution, file access, network access, and subprocess authority MUST be
  limited to the smallest scope the feature requires.
- A sandbox or isolation boundary MUST be enforced by the mechanism that owns the
  boundary, not only described in a prompt or configuration comment.
- Cleanup, timeout, cancellation, and failure paths MUST release credentials,
  processes, file handles, locks, and temporary data.
- Concurrency controls MUST protect security decisions and state transitions from
  races, replay, duplicate submission, and time-of-check/time-of-use gaps.

## 6. Dependencies and build integrity

- Dependencies MUST be selected, versioned, and retrieved through the project's
  declared mechanism. A build MUST NOT silently execute an unreviewed tool supplied
  by untrusted project content.
- Security-sensitive behavior MUST use maintained, well-understood primitives and
  standard cryptographic libraries. The implementation MUST NOT invent cryptography.
- Generated artifacts, manifests, configuration, and release inputs MUST be
  validated before they acquire authority.
- A security scan or passing test MUST NOT be treated as proof that manual review
  obligations disappeared.

## 7. Security evidence

- A security-relevant behavior MUST have a negative case or boundary test where a
  meaningful failure can occur, unless the project documents why executable proof is
  not possible.
- Tests MUST exercise the boundary that matters: authorization through the protected
  operation, path confinement through the filesystem boundary, and safe output
  through the response or sink.
- A reviewer MUST trace at least one credible trigger-to-impact path for every
  finding and cite the code that makes the path possible.
- A finding based only on a generic possibility, without a reachable trigger and
  concrete impact, is not a finding.

## 8. Optional deployment profiles

A deployment profile adds requirements; it does not weaken this canon.

- A STIG profile MUST identify the exact applicable DISA document and release,
  system components in scope, inherited controls, and required evidence.
- Platform, container, operating-system, network, and application STIGs are separate
  scopes. Passing a source-code review does not establish their configuration.
- The Security Reviewer may flag a missing profile decision when the North Star
  requires one, but MUST NOT claim that a source diff proves formal STIG compliance.
- ASVS-derived requirements SHOULD be selected according to the application's
  exposure and data sensitivity rather than copied indiscriminately into unrelated
  projects.

## Review questions

1. What is untrusted, where does it cross a boundary, and where is it validated?
2. Who is allowed to perform this operation on this resource, and where is that
   decision made?
3. Can any input become code, a path, a query, a URL, a template, or a protocol
   control sequence?
4. Can an attacker cause unbounded work, retained data, repeated work, or leaked
   authority?
5. Could secrets or sensitive data reach a prompt, log, error, response, artifact,
   or dependency?
6. What happens when authentication, authorization, validation, isolation, or a
   dependency is unavailable?
7. Which negative test demonstrates the security property at its real boundary?
8. Does the project require an additional application or deployment profile?
