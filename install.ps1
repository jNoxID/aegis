Set-Location C:\Users\neoth\BAZE\aegis

if ((git rev-parse --show-toplevel) -ne "C:/Users/neoth/BAZE/aegis") {
    throw "Mauvaise racine Git : arrêt."
}

if (-not (Test-Path .\pyproject.toml)) {
    throw "pyproject.toml absent : arrêt."
}

if (-not (Test-Path .\.venv\Scripts\python.exe)) {
    py -3.13 -m venv .venv
}

.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\aegis.exe doctor