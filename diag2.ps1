$ErrorActionPreference = 'Stop'
$Python313 = 'C:\Users\neoth\AppData\Local\Programs\Python\Python313\python.exe'

if (-not (Test-Path $Python313 -PathType Leaf)) {
    throw "Python 3.13 introuvable : $Python313"
}

Write-Host "`n=== INTERPRETEUR SOURCE ==="
& $Python313 --version
& $Python313 -c "import platform, struct, sys; print('executable=', sys.executable); print('version=', sys.version); print('bits=', struct.calcsize('P') * 8); print('machine=', platform.machine())"

Write-Host "`n=== ENSUREPIP SOURCE ==="
& $Python313 -m ensurepip --version
if ($LASTEXITCODE -ne 0) {
    throw "ensurepip source a échoué avec le code $LASTEXITCODE"
}

Write-Host "`n=== NETTOYAGE CIBLE ==="
if (Test-Path .venv-test) {
    Remove-Item -Recurse -Force .venv-test
}
if (Test-Path .venv) {
    Remove-Item -Recurse -Force .venv
}

Write-Host "`n=== CREATION DU VENV FINAL ==="
& $Python313 -m venv .venv
if ($LASTEXITCODE -ne 0) {
    throw "Création du venv échouée avec le code $LASTEXITCODE"
}

$VenvPython = Join-Path $PWD '.venv\Scripts\python.exe'
if (-not (Test-Path $VenvPython -PathType Leaf)) {
    throw "Interpréteur du venv absent : $VenvPython"
}

Write-Host "`n=== VALIDATION PYTHON ET PIP DU VENV ==="
& $VenvPython --version
if ($LASTEXITCODE -ne 0) {
    throw "Python du venv a échoué avec le code $LASTEXITCODE"
}

& $VenvPython -c "import platform, struct, sys; print('executable=', sys.executable); print('prefix=', sys.prefix); print('base_prefix=', sys.base_prefix); print('bits=', struct.calcsize('P') * 8); print('machine=', platform.machine()); assert sys.prefix != sys.base_prefix"
if ($LASTEXITCODE -ne 0) {
    throw "L'isolation du venv n'est pas valide"
}

& $VenvPython -m pip --version
if ($LASTEXITCODE -ne 0) {
    throw "pip du venv a échoué avec le code $LASTEXITCODE"
}

Write-Host "`n=== MISE A JOUR DE PIP ==="
& $VenvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    throw "Mise à jour de pip échouée avec le code $LASTEXITCODE"
}

Write-Host "`n=== INSTALLATION OFFICIELLE DU PROJET ==="
& $VenvPython -m pip install -e '.[dev]'
if ($LASTEXITCODE -ne 0) {
    throw "Installation du projet échouée avec le code $LASTEXITCODE"
}

Write-Host "`n=== VALIDATION DES IMPORTS ==="
& $VenvPython -c "import aegis; import aegis.cli; import aegis.core.models; import aegis.scope.policy; print('aegis=', aegis.__version__)"
if ($LASTEXITCODE -ne 0) {
    throw "Validation des imports échouée avec le code $LASTEXITCODE"
}

Write-Host "`n=== VALIDATION CLI ==="
& $VenvPython -m aegis.cli doctor
if ($LASTEXITCODE -ne 0) {
    throw "aegis doctor a échoué avec le code $LASTEXITCODE"
}

Write-Host "`n=== CONTROLES QUALITE ==="
& $VenvPython -m ruff format --check .
if ($LASTEXITCODE -ne 0) {
    throw "ruff format --check a échoué avec le code $LASTEXITCODE"
}

& $VenvPython -m ruff check .
if ($LASTEXITCODE -ne 0) {
    throw "ruff check a échoué avec le code $LASTEXITCODE"
}

& $VenvPython -m mypy
if ($LASTEXITCODE -ne 0) {
    throw "mypy a échoué avec le code $LASTEXITCODE"
}

& $VenvPython -m pytest
if ($LASTEXITCODE -ne 0) {
    throw "pytest a échoué avec le code $LASTEXITCODE"
}

Write-Host "`n=== ETAT GIT ==="
git status --short

Write-Host "`n[PASS] ENVIRONNEMENT PYTHON VALIDE"