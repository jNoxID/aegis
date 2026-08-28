"""Black-box verification of the persistent AEGIS runtime."""

from __future__ import annotations

import json
import socket
import subprocess
import sys
import time
from contextlib import closing
from urllib.error import URLError
from urllib.request import urlopen


def _available_local_port() -> int:
    with closing(socket.socket()) as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def _get_when_ready(url: str, process: subprocess.Popen[str]) -> tuple[int, bytes]:
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            raise AssertionError(
                f"AEGIS exited before serving HTTP (exit {process.returncode}).\n"
                f"stdout:\n{stdout}\nstderr:\n{stderr}"
            )
        try:
            # The URL is constructed internally and always targets the loopback listener.
            with urlopen(url, timeout=0.5) as response:
                return response.status, response.read()
        except URLError:
            time.sleep(0.05)
    raise AssertionError(f"AEGIS did not serve {url} within 10 seconds")


def test_module_cli_starts_a_real_http_server() -> None:
    """Exercise module entry point, CLI dispatch, Uvicorn, and all public system URLs."""

    port = _available_local_port()
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "aegis",
            "server",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        root_code, root_body = _get_when_ready(f"http://127.0.0.1:{port}/", process)
        health_code, health_body = _get_when_ready(
            f"http://127.0.0.1:{port}/health", process
        )
        status_code, status_body = _get_when_ready(
            f"http://127.0.0.1:{port}/api/v1/status", process
        )
        docs_code, _ = _get_when_ready(f"http://127.0.0.1:{port}/docs", process)
        favicon_code, _ = _get_when_ready(f"http://127.0.0.1:{port}/favicon.ico", process)

        assert root_code == 200
        assert b"Security Operations Platform" in root_body
        assert health_code == 200
        assert json.loads(health_body) == {"status": "ok", "service": "aegis"}
        assert status_code == 200
        assert json.loads(status_body)["service"] == "aegis"
        assert docs_code == 200
        assert favicon_code == 200
        time.sleep(2)
        assert process.poll() is None
        repeated_health_code, _ = _get_when_ready(
            f"http://localhost:{port}/health", process
        )
        assert repeated_health_code == 200
    finally:
        process.terminate()
        try:
            process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate()
