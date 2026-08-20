"""HTTP application exposing the initial AEGIS control-plane status API."""

from __future__ import annotations

from typing import Literal, TypedDict

from fastapi import FastAPI

from aegis import __version__


class HealthResponse(TypedDict):
    """Stable response contract for service health checks."""

    status: Literal["ok"]
    service: Literal["aegis"]


class StatusResponse(HealthResponse):
    """Public runtime metadata returned by the status endpoint."""

    version: str


def create_app() -> FastAPI:
    """Build the AEGIS ASGI application without starting a network listener."""

    app = FastAPI(
        title="AEGIS API",
        description="Policy-gated control plane for authorized security operations.",
        version=__version__,
    )

    @app.get("/", tags=["system"])
    async def root() -> StatusResponse:
        return {"status": "ok", "service": "aegis", "version": __version__}

    @app.get("/health", tags=["system"])
    async def health() -> HealthResponse:
        return {"status": "ok", "service": "aegis"}

    @app.get("/api/v1/status", tags=["system"])
    async def status() -> StatusResponse:
        return {"status": "ok", "service": "aegis", "version": __version__}

    return app


app = create_app()
