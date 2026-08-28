import asyncio
from ipaddress import ip_network
from uuid import uuid4

import pytest

from aegis.core.models import Actor, EngagementRef
from aegis.scope import Action, Scope, ScopePolicyEngine, Target


@pytest.fixture
def context():
    organization_id, engagement_id = uuid4(), uuid4()
    return (
        Actor(uuid4(), organization_id),
        EngagementRef(engagement_id, organization_id),
        Scope(
            engagement_id,
            domains=frozenset({"example.test", "*.lab.test"}),
            networks=(ip_network("10.10.0.0/16"),),
            excluded_domains=frozenset({"admin.example.test"}),
            excluded_networks=(ip_network("10.10.13.0/24"),),
        ),
    )


def test_scope_is_mandatory(context):
    actor, engagement, _ = context
    decision = asyncio.run(
        ScopePolicyEngine().authorize(
            actor=actor,
            action=Action.ACTIVE_PROBE,
            target=Target(domain="example.test"),
            engagement=engagement,
            scope=None,
        )
    )
    assert not decision.allowed
    assert decision.reason == "scope_required"


@pytest.mark.parametrize(
    ("target", "allowed", "reason"),
    [
        (Target(domain="example.test"), True, "target_in_scope"),
        (Target(domain="api.lab.test"), True, "target_in_scope"),
        (Target(domain="lab.test"), False, "target_not_allowlisted"),
        (Target(domain="admin.example.test"), False, "target_excluded"),
        (Target(ip="10.10.12.4"), True, "target_in_scope"),
        (Target(ip="10.10.13.4"), False, "target_excluded"),
        (Target(ip="203.0.113.1"), False, "target_not_allowlisted"),
    ],
)
def test_allowlists_and_exclusions(context, target, allowed, reason):
    actor, engagement, scope = context
    decision = asyncio.run(
        ScopePolicyEngine().authorize(
            actor=actor,
            action=Action.ACTIVE_PROBE,
            target=target,
            engagement=engagement,
            scope=scope,
        )
    )
    assert decision.allowed is allowed
    assert decision.reason == reason


def test_cross_organization_actor_is_denied(context):
    _, engagement, scope = context
    decision = asyncio.run(
        ScopePolicyEngine().authorize(
            actor=Actor(uuid4(), uuid4()),
            action=Action.READ,
            target=Target(domain="example.test"),
            engagement=engagement,
            scope=scope,
        )
    )
    assert not decision.allowed
    assert decision.reason == "organization_mismatch"
