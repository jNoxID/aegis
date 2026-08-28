"""Deny-by-default authorization of operation targets."""

from aegis.scope.policy import ScopePolicyEngine
from aegis.scope.types import Action, PolicyDecision, Scope, Target

__all__ = ["Action", "PolicyDecision", "Scope", "ScopePolicyEngine", "Target"]
