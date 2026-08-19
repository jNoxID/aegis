# ADR 0002: Centralize active operations behind a policy gateway

- Status: Accepted
- Date: 2026-08-19

## Decision

Only the tool gateway may possess credentials or transports capable of active
operations. It composes deny-by-default policy, persists a decision and audit
record, then issues an expiring audience-bound capability. Plugins, workflows,
and AI agents submit structured proposals and cannot invoke transports directly.

## Consequences

This creates a narrow, testable choke point and enables isolation. It also makes
gateway availability safety-critical: failures deny dispatch. DNS, redirects,
retries, and newly discovered targets require re-authorization.
