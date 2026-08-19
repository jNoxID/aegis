import json

from aegis.cli import main


def test_doctor(capsys):
    assert main(["doctor"]) == 0
    assert json.loads(capsys.readouterr().out)["python_compatible"] is True


def test_scope_check_denies_by_default(capsys):
    assert main(["scope-check", "--domain", "public.example"]) == 2
    assert json.loads(capsys.readouterr().out) == {
        "allowed": False,
        "reason": "target_not_allowlisted",
    }
