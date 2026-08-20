import subprocess
import sys


def test_python_module_exposes_cli():
    result = subprocess.run(
        [sys.executable, "-m", "aegis"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "AEGIS control-plane" in result.stdout
    assert "server" in result.stdout
