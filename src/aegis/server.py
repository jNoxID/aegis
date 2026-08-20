"""Production server adapter for the AEGIS ASGI application."""

from __future__ import annotations

import uvicorn


def run(*, host: str = "127.0.0.1", port: int = 8000) -> int:
    """Run AEGIS until interrupted by the operator."""

    print(f"AEGIS starting...\nHost: {host}\nPort: {port}", flush=True)
    uvicorn.run("aegis.api:app", host=host, port=port)
    return 0
