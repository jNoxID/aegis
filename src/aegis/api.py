"""HTTP application exposing the AEGIS control plane and web console."""

from __future__ import annotations

from pathlib import Path
from typing import Literal, TypedDict

from fastapi import APIRouter, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from aegis import __version__


class HealthResponse(TypedDict):
    """Stable response contract for service health checks."""

    status: Literal["ok"]
    service: Literal["aegis"]


class StatusResponse(HealthResponse):
    """Public runtime metadata returned by the status endpoint."""

    version: str


WEB_ROOT = Path(__file__).with_name("web")


def system_router() -> APIRouter:
    """Create the versioned API routes consumed by operators and the web UI."""

    router = APIRouter(tags=["system"])

    @router.get("/health")
    async def health() -> HealthResponse:
        return {"status": "ok", "service": "aegis"}

    @router.get("/api/v1/status")
    async def status() -> StatusResponse:
        return {"status": "ok", "service": "aegis", "version": __version__}

    return router


def create_app() -> FastAPI:
    """Build the AEGIS ASGI application without starting a network listener."""

    app = FastAPI(
        title="AEGIS API",
        description="Policy-gated control plane for authorized security operations.",
        version=__version__,
    )
    app.include_router(system_router())
    app.mount("/static", StaticFiles(directory=WEB_ROOT / "static"), name="static")

    @app.get("/", include_in_schema=False)
    async def web_console() -> FileResponse:
        return FileResponse(WEB_ROOT / "index.html", media_type="text/html")

    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon() -> FileResponse:
        return FileResponse(WEB_ROOT / "static" / "favicon.svg", media_type="image/svg+xml")

    return app


app = create_app()
