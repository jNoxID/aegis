# Security policy

## Authorized use

Use AEGIS only for assets you own or have explicit permission to assess. Every
engagement must record owner, authorization evidence, allowlist, exclusions,
permitted actions, environment, time window, and emergency contact. AEGIS is not
an authorization oracle; operators remain responsible for lawful use.

No active security module will be accepted until the complete policy gateway,
durable audit, kill switch, approval controls, and bypass tests exist. Current
code performs no network activity.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability. Use the repository
host's private security-advisory channel and include affected version/commit,
impact, reproduction with synthetic targets, and proposed remediation if known.
Do not access other users' data, test public infrastructure, or retain secrets.
Maintainers should acknowledge within three business days, triage within seven,
coordinate a fix and disclosure, and credit reporters who request it.

## Baseline requirements

* Deny by default; enforce least privilege and organization separation.
* Keep secrets out of source, CLI arguments, logs, traces, and artifacts.
* Use established cryptographic libraries and managed key material only.
* Validate structured input; safely render untrusted evidence; prevent SSRF,
  traversal, injection, unsafe deserialization, and command construction.
* Pin and scan dependencies, emit an SBOM, and sign release provenance.
* Fail closed when policy, audit, identity, approval, or kill-switch state cannot
  be established; alert rather than suppress critical vulnerabilities.

## Operational response

Suspected out-of-scope behavior requires immediate global kill switch, worker
credential revocation, queue quarantine, preservation of append-only audit and
telemetry, tenant notification, and incident review before restart. Recovery
rotates credentials, validates audit-chain anchors, rebuilds workers from signed
artifacts, and explicitly re-authorizes queued work.
