$ErrorActionPreference = 'Continue'
$Log = Join-Path (Get-Location) 'python-venv-diagnostic.txt'

Start-Transcript -Path $Log -Force

Write-Host "`n=== HORODATAGE ET EMPLACEMENT ==="
Get-Date -Format o
Get-Location

Write-Host "`n=== RESOLUTION DES INTERPRETEURS ==="
where.exe python 2>&1
where.exe python3 2>&1
where.exe py 2>&1
Get-Command python -All -ErrorAction SilentlyContinue |
    Format-List Name, CommandType, Source, Definition
Get-Command python3 -All -ErrorAction SilentlyContinue |
    Format-List Name, CommandType, Source, Definition
Get-Command py -All -ErrorAction SilentlyContinue |
    Format-List Name, CommandType, Source, Definition

Write-Host "`n=== VERSIONS ET ARCHITECTURE ==="
python --version
python -c "import sys, platform, struct; print('executable=', sys.executable); print('version=', sys.version); print('bits=', struct.calcsize('P') * 8); print('machine=', platform.machine())"
python3 --version 2>&1
python3 -c "import sys; print(sys.executable); print(sys.version)" 2>&1
py -0p 2>&1

Write-Host "`n=== VARIABLES PYTHON/PIP/PROXY/TEMP ==="
Get-ChildItem Env: |
    Where-Object {
        $_.Name -match '^(PYTHON|PIP|HTTP_PROXY|HTTPS_PROXY|NO_PROXY|TMP|TEMP)$' -or
        $_.Name -match '^(PYTHON|PIP)'
    } |
    Sort-Object Name |
    Format-Table -AutoSize

Write-Host "`n=== PREFIXES ET CHEMINS PYTHON ==="
python -c "import sys, sysconfig; print('executable=', sys.executable); print('prefix=', sys.prefix); print('base_prefix=', sys.base_prefix); print('exec_prefix=', sys.exec_prefix); print('base_exec_prefix=', sys.base_exec_prefix); print('paths=', sysconfig.get_paths())"

Write-Host "`n=== ENSUREPIP : MODULE ET RESSOURCES ==="
python -c "import ensurepip, pathlib; p=pathlib.Path(ensurepip.__file__).resolve(); print('ensurepip=', p); print('directory=', p.parent); print('bundled_exists=', (p.parent / '_bundled').is_dir()); print('bundled_files='); [print(x.name, x.stat().st_size) for x in sorted((p.parent / '_bundled').glob('*'))]"
python -m ensurepip --version

Write-Host "`n=== PIP GLOBAL ==="
python -m pip --version
python -m pip config debug
python -m pip config list -v

Write-Host "`n=== VENV PARTIEL EXISTANT ==="
if (Test-Path .venv) {
    Get-Item .venv | Format-List FullName, Attributes, CreationTime, LastWriteTime
    Get-ChildItem .venv -Force -Recurse -ErrorAction SilentlyContinue |
        Select-Object -First 200 FullName, Length, Attributes, LastWriteTime
    if (Test-Path .venv\pyvenv.cfg) {
        Write-Host "--- .venv\pyvenv.cfg ---"
        Get-Content .venv\pyvenv.cfg
    }
} else {
    Write-Host ".venv absent"
}

Write-Host "`n=== ENSUREPIP GLOBAL VERBEUX ==="
$globalEnsurepip = Start-Process `
    -FilePath (Get-Command python).Source `
    -ArgumentList @('-X', 'faulthandler', '-m', 'ensurepip', '--upgrade', '--default-pip', '-v') `
    -NoNewWindow -PassThru -Wait `
    -RedirectStandardOutput "$PWD\ensurepip-global.stdout.txt" `
    -RedirectStandardError "$PWD\ensurepip-global.stderr.txt"
Write-Host "ExitCode=$($globalEnsurepip.ExitCode)"
Get-Content "$PWD\ensurepip-global.stdout.txt" -ErrorAction SilentlyContinue
Get-Content "$PWD\ensurepip-global.stderr.txt" -ErrorAction SilentlyContinue

Write-Host "`n=== TEST VENV SANS PIP ==="
if (Test-Path .venv-test) {
    Remove-Item -Recurse -Force .venv-test
}
python -m venv .venv-test --without-pip
Write-Host "venv --without-pip ExitCode=$LASTEXITCODE"

if (Test-Path .venv-test\Scripts\python.exe) {
    .\.venv-test\Scripts\python.exe --version
    .\.venv-test\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.prefix); print(sys.base_prefix)"

    Write-Host "`n=== ENSUREPIP DANS LE VENV DIAGNOSTIQUE ==="
    $venvEnsurepip = Start-Process `
        -FilePath "$PWD\.venv-test\Scripts\python.exe" `
        -ArgumentList @('-X', 'faulthandler', '-m', 'ensurepip', '--upgrade', '--default-pip', '-v') `
        -NoNewWindow -PassThru -Wait `
        -RedirectStandardOutput "$PWD\ensurepip-venv.stdout.txt" `
        -RedirectStandardError "$PWD\ensurepip-venv.stderr.txt"
    Write-Host "ExitCode=$($venvEnsurepip.ExitCode)"
    Get-Content "$PWD\ensurepip-venv.stdout.txt" -ErrorAction SilentlyContinue
    Get-Content "$PWD\ensurepip-venv.stderr.txt" -ErrorAction SilentlyContinue
}

Write-Host "`n=== PROCESSUS ENCORE PRESENTS ==="
Get-CimInstance Win32_Process |
    Where-Object {
        $_.Name -match '^python(w)?\.exe$' -or
        $_.CommandLine -match 'ensurepip'
    } |
    Select-Object ProcessId, ParentProcessId, Name, ExecutablePath, CommandLine |
    Format-List

Stop-Transcript

Write-Host "`nDiagnostic terminé : $Log"