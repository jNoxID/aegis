"""Common immutable identifiers passed across domain boundaries."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Actor:
    """Authenticated principal requesting an operation."""

    id: UUID
    organization_id: UUID


@dataclass(frozen=True, slots=True)
class EngagementRef:
    """Minimal engagement identity needed by the policy boundary."""

    id: UUID
    organization_id: UUID
    active: bool = True
