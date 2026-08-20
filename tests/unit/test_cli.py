import json
from unittest.mock import patch

from aegis.cli import main


def test_cli_entrypoint_displays_help_without_a_command(capsys):
    assert main([]) == 0
    assert "server" in capsys.readouterr().out


def test_doctor(capsys):
    assert main(["doctor"]) == 0
    assert json.loads(capsys.readouterr().out)["python_compatible"] is True


def test_scope_check_denies_by_default(capsys):
    assert main(["scope-check", "--domain", "public.example"]) == 2
    assert json.loads(capsys.readouterr().out) == {
        "allowed": False,
        "reason": "target_not_allowlisted",
    }


def test_server_command_starts_configured_listener(capsys):
    with patch("aegis.server.uvicorn.run") as run:
        assert main(["server", "--host", "127.0.0.2", "--port", "8765"]) == 0

    run.assert_called_once_with("aegis.api:app", host="127.0.0.2", port=8765)
    assert "AEGIS starting..." in capsys.readouterr().out
