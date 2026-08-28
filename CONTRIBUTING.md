# Contributing to AEGIS

## Workflow

1. Start with a bounded issue, threat/authorization impact, and acceptance tests.
2. Preserve domain boundaries; add a port only for a real replaceable adapter.
3. Keep operations side-effect-free until a policy decision reaches the sole
   tool gateway. Never add an alternate network/process execution path.
4. Add tests at the lowest useful layer and security regression tests for every
   policy or trust-boundary change.
5. Run `ruff format --check .`, `ruff check .`, `mypy`, and `pytest`.
6. Update architecture, threat model, ADR, migrations, and operator guidance when
   behavior or risk changes. Keep commits focused and reviewable.

Python 3.13+, strict typing, short cohesive functions, immutable boundary values,
and explicit dependency injection are expected. Imports must never be wrapped in
`try/except`. Never commit credentials, real target data, exploit payloads, or
authorization evidence; tests use reserved/synthetic names and addresses.

## Security review checklist

Confirm input normalization, tenant ownership, RBAC, scope/exclusion precedence,
approval and expiry, rate/quota/deadline/cancellation, kill-switch behavior,
audit/provenance, secret redaction, egress/SSRF, hostile outputs, race/replay,
dependency risk, and fail-closed errors. A reviewer independent from the author
must approve gateway, identity, crypto, audit, or sandbox changes.
