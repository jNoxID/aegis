"""Allow the official CLI to be invoked with ``python -m aegis``."""

from aegis.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
