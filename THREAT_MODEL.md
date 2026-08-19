# AEGIS threat model

## Method and scope

This living model applies STRIDE plus abuse-case analysis to the control plane,
policy/tool gateway, worker plane, plugins, artifacts, persistence, supply chain,
and future AI gateway. Safety means both protecting AEGIS and preventing AEGIS
from operating beyond explicit authorization.

## Assets and adversaries

Protected assets include credentials and keys, tenant data, engagement scopes,
approvals, policy/audit integrity, worker capabilities, artifacts/evidence, and
target availability. Adversaries include unauthenticated clients, malicious or
compromised tenants/operators, compromised dependencies/plugins/workers, hostile
target responses and artifacts, and malicious prompt/tool content. Administrators
are powerful but not implicitly trusted to rewrite audit history or self-approve
high-risk actions.

## Principal threats and controls

| Threat | Boundary | Required controls |
|---|---|---|
| Spoofed actor/service | client/control, control/worker | MFA, short sessions, hashed API keys, workload identity, mTLS |
| Cross-tenant access | identity/database | derived tenant context, RBAC, PostgreSQL RLS, composite constraints/tests |
| Out-of-scope execution | gateway/target | deny default, normalized allowlist, exclusions, recheck DNS/redirect/retry |
| SSRF and DNS rebinding | worker egress | dedicated resolving proxy, private/special IP policy, pinned answers, hop checks |
| Policy/audit tampering | control/storage | transactional decision+audit, append-only roles, hash chain, external anchor |
| Approval replay | approval/gateway | exact request digest, risk, approver, expiry, nonce, single-use token |
| Plugin escape/RCE | plugin/worker | signed allowlist, container sandbox, syscall/resource/network limits, no host secrets |
| Malicious artifact | worker/control/UI | quarantine, digest, parsers in sandbox, output encoding, CSP, download headers |
| Queue forgery/replay | control/worker | authenticated messages, schema/version, idempotency, expiry and audience |
| Kill-switch bypass | all execution paths | gateway-enforced global/tenant/engagement switches, cached fail-closed state |
| Secret disclosure | logs/artifacts/storage | vault references, envelope encryption, redaction, least privilege, rotation |
| Prompt/tool injection | AI/tool gateway | treat content as data, structured schemas, policy recheck, no direct tools/secrets |
| Resource exhaustion | every boundary | body limits, quotas, rate limits, deadlines, concurrency/resource envelopes |
| Supply-chain compromise | build/runtime | lock hashes, review, SAST/SCA, SBOM, provenance, signed artifacts/images |

## Abuse cases and invariants

* A plugin proposes a public redirect or embeds an IP in an alternate notation:
  normalization and destination re-authorization deny it.
* A tenant submits another tenant's engagement UUID: identity-derived organization
  checks and RLS deny it and create an audit event.
* An approver changes the target after approval: request-digest binding invalidates
  approval.
* A worker retries after scope expiry or kill-switch activation: a fresh/single-use
  authorization is required and dispatch fails closed.
* A model asks a tool to ignore policy: the model has no execution credential;
  its typed proposal follows the same gateway path as any untrusted client.

Non-negotiable invariants: no active transport outside the gateway; absence or
failure of policy/audit/approval denies; exclusions override inclusions; derived
targets are new targets; plugins and models cannot mint capabilities; range and
production routing never overlap; sensitive actions are reconstructible.

## Residual risk and validation

Authorization documents may themselves be fraudulent or stale; AEGIS cannot
prove legal ownership. Organizations must retain evidence and expiry, reviewers
must validate it, and incident response can globally revoke execution. Sandbox
and cryptographic controls reduce rather than eliminate platform compromise.

The model is reviewed for every new execution primitive, trust boundary, data
type, identity mechanism, and release. Security tests must cover bypasses,
canonicalization, race/replay, tenant isolation, fail-open dependency failures,
hostile artifacts, and egress. Findings update this document and an ADR.
