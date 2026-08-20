# AEGIS

AEGIS is a security operations and authorized-testing platform designed around a
single invariant: **no active capability executes without a verifiable,
auditable policy decision**.

The project is currently in **Phase 0 / first foundation increment**. It ships a
small, executable, deny-by-default scope policy kernel; it does not ship any
scanner or offensive capability.

## Quick start

AEGIS requires Python 3.13 or newer.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
aegis doctor
pytest
```

On Windows PowerShell, run the installation from the repository root (the
directory that contains this `pyproject.toml`):

```powershell
git rev-parse --show-toplevel
Set-Location (git rev-parse --show-toplevel)
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\aegis.exe doctor
.\.venv\Scripts\python.exe -m pytest
```

If pip reports that neither `setup.py` nor `pyproject.toml` was found, first
check `Test-Path .\pyproject.toml`. A `False` result means the command is being
run from the wrong directory (or from an incomplete checkout); do not create a
second packaging file there. This repository is a single Python project with a
`src/aegis` package, and its authoritative packaging configuration is the
top-level `pyproject.toml`.

`aegis scope-check` is a local, side-effect-free demonstration of scope
evaluation:

```bash
aegis scope-check --domain app.lab.example --allow-domain app.lab.example
```

See [the architecture](ARCHITECTURE.md), [threat model](THREAT_MODEL.md),
[security policy](SECURITY.md), and [contribution guide](CONTRIBUTING.md).

## Safety and status

Use AEGIS only on systems you own or are explicitly authorized to test. Scope
authorization is necessary but not sufficient: future sensitive operations will
also require RBAC, approval, quota, environment, and kill-switch checks.

AEGIS is pre-alpha. APIs and persistence formats are not stable.

## License

GNU General Public License v3.0; see [LICENSE](LICENSE).
