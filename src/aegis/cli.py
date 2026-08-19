"""Dependency-free bootstrap CLI for the first executable increment."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from ipaddress import ip_network
from uuid import uuid4

from aegis import __version__
from aegis.core.models import Actor, EngagementRef
from aegis.scope import Action, Scope, ScopePolicyEngine, Target


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aegis", description="AEGIS control-plane bootstrap")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="validate the local runtime")
    check = commands.add_parser("scope-check", help="evaluate scope without network activity")
    target = check.add_mutually_exclusive_group(required=True)
    target.add_argument("--domain")
    target.add_argument("--ip")
    check.add_argument("--allow-domain", action="append", default=[])
    check.add_argument("--allow-cidr", action="append", default=[])
    check.add_argument("--exclude-domain", action="append", default=[])
    check.add_argument("--exclude-cidr", action="append", default=[])
    return parser


async def _scope_check(args: argparse.Namespace) -> int:
    organization_id, engagement_id = uuid4(), uuid4()
    decision = await ScopePolicyEngine().authorize(
        actor=Actor(id=uuid4(), organization_id=organization_id),
        action=Action.ACTIVE_PROBE,
        target=Target(domain=args.domain, ip=args.ip),
        engagement=EngagementRef(id=engagement_id, organization_id=organization_id),
        scope=Scope(
            engagement_id=engagement_id,
            domains=frozenset(args.allow_domain),
            networks=tuple(ip_network(value, strict=True) for value in args.allow_cidr),
            excluded_domains=frozenset(args.exclude_domain),
            excluded_networks=tuple(ip_network(value, strict=True) for value in args.exclude_cidr),
        ),
    )
    print(json.dumps({"allowed": decision.allowed, "reason": decision.reason}, sort_keys=True))
    return 0 if decision.allowed else 2


def main(argv: list[str] | None = None) -> int:
    """Run the bootstrap command-line interface."""

    args = _parser().parse_args(argv)
    if args.command == "doctor":
        compatible = sys.version_info >= (3, 13)
        print(json.dumps({"aegis": __version__, "python_compatible": compatible}, sort_keys=True))
        return 0 if compatible else 1
    return asyncio.run(_scope_check(args))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
