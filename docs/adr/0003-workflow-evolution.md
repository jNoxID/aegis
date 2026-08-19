# ADR 0003: Persist workflows before adopting a distributed queue

- Status: Accepted
- Date: 2026-08-19

## Decision

Define a durable workflow/task/execution state machine and run it through an
in-process queue adapter first. Adopt Dramatiq with Redis when multiple workers
are required; reassess Celery if complex canvas primitives become essential.

## Consequences

Correctness, cancellation, retries, and idempotency are designed independently
of broker delivery semantics. Distribution is delayed, while queue contracts
remain explicit and testable.
