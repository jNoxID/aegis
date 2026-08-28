"""Typed values used by the scope policy engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from ipaddress import IPv4Network, IPv6Network
from uuid import UUID

IPNetwork = IPv4Network | IPv6Network


class Action(StrEnum):
    """Initial action taxonomy; unknown strings cannot enter the engine."""

    READ = "read"
    ACTIVE_PROBE = "active_probe"
    DESTRUCTIVE_TEST = "destructive_test"


@dataclass(frozen=True, slots=True)
class Target:
    """A normalized target with exactly one address kind."""

    domain: str | None = None
    ip: str | None = None

    def __post_init__(self) -> None:
        if (self.domain is None) == (self.ip is None):
            raise ValueError("target must contain exactly one of domain or ip")


@dataclass(frozen=True, slots=True)
class Scope:
    """An engagement allowlist with exclusions taking precedence."""

    engagement_id: UUID
    domains: frozenset[str] = field(default_factory=frozenset)
    networks: tuple[IPNetwork, ...] = ()
    excluded_domains: frozenset[str] = field(default_factory=frozenset)
    excluded_networks: tuple[IPNetwork, ...] = ()


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    """Stable decision record suitable for persistence in the audit domain."""

    allowed: bool
    reason: str
    decision_id: UUID
    actor_id: UUID
    engagement_id: UUID
    action: Action
    normalized_target: str
