# ADR 0001: Begin as a modular monolith

- Status: Accepted
- Date: 2026-08-19

## Decision

Use one deployable Python application with feature-owned domain packages,
explicit ports, and versioned events. PostgreSQL is the transactional system of
record. Extract a service only when isolation, scaling, ownership, or failure
evidence justifies the operational cost.

## Consequences

Local transactions, tests, and deployment remain simple. Package import rules
and domain APIs must prevent accidental coupling. Queue and worker adapters are
replaceable without pretending the initial system is distributed.
