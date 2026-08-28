"""Central deny-by-default scope policy evaluation."""

from __future__ import annotations

from ipaddress import ip_address
from uuid import uuid4

from aegis.core.models import Actor, EngagementRef
from aegis.scope.types import Action, PolicyDecision, Scope, Target


class ScopePolicyEngine:
    """Make deterministic scope decisions without performing network I/O.

    This kernel is deliberately final in effect rather than subclass-oriented:
    callers receive decisions, never hooks that can mutate policy evaluation.
    The future tool gateway will be the only component able to turn an allowed
    decision into an active operation.
    """

    async def authorize(
        self,
        *,
        actor: Actor,
        action: Action,
        target: Target,
        engagement: EngagementRef,
        scope: Scope | None,
    ) -> PolicyDecision:
        normalized_target = self._normalize_target(target)
        reason = self._deny_reason(actor, engagement, scope)
        if reason is None:
            assert scope is not None  # narrowed by _deny_reason
            allowed, reason = self._target_allowed(target, scope)
        else:
            allowed = False

        return PolicyDecision(
            allowed=allowed,
            reason=reason,
            decision_id=uuid4(),
            actor_id=actor.id,
            engagement_id=engagement.id,
            action=action,
            normalized_target=normalized_target,
        )

    @staticmethod
    def _deny_reason(actor: Actor, engagement: EngagementRef, scope: Scope | None) -> str | None:
        if not engagement.active:
            return "engagement_inactive"
        if actor.organization_id != engagement.organization_id:
            return "organization_mismatch"
        if scope is None:
            return "scope_required"
        if scope.engagement_id != engagement.id:
            return "scope_engagement_mismatch"
        return None

    @classmethod
    def _target_allowed(cls, target: Target, scope: Scope) -> tuple[bool, str]:
        if target.domain is not None:
            domain = cls._normalize_domain(target.domain)
            if cls._matches_domain(domain, scope.excluded_domains):
                return False, "target_excluded"
            if cls._matches_domain(domain, scope.domains):
                return True, "target_in_scope"
            return False, "target_not_allowlisted"

        assert target.ip is not None  # Target enforces exactly one address kind
        address = ip_address(target.ip)
        if any(address in network for network in scope.excluded_networks):
            return False, "target_excluded"
        if any(address in network for network in scope.networks):
            return True, "target_in_scope"
        return False, "target_not_allowlisted"

    @classmethod
    def _normalize_target(cls, target: Target) -> str:
        if target.domain is not None:
            return cls._normalize_domain(target.domain)
        assert target.ip is not None  # Target enforces exactly one address kind
        return str(ip_address(target.ip))

    @staticmethod
    def _normalize_domain(domain: str) -> str:
        normalized = domain.rstrip(".").lower()
        if not normalized or len(normalized) > 253:
            raise ValueError("invalid domain")
        labels = normalized.split(".")
        if any(
            not label
            or len(label) > 63
            or label.startswith("-")
            or label.endswith("-")
            or not all(char.isalnum() or char == "-" for char in label)
            for label in labels
        ):
            raise ValueError("invalid domain")
        return normalized

    @classmethod
    def _matches_domain(cls, domain: str, rules: frozenset[str]) -> bool:
        for raw_rule in rules:
            rule = cls._normalize_domain(raw_rule.removeprefix("*."))
            if raw_rule.startswith("*.") and domain.endswith(f".{rule}"):
                return True
            if not raw_rule.startswith("*.") and domain == rule:
                return True
        return False
