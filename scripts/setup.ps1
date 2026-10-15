param([string]$Python='python',[string]$JavaHome,[switch]$SkipWeb)
$ErrorActionPreference='Stop'
$ProjectRoot=Split-Path $PSScriptRoot -Parent
function Invoke-Checked([scriptblock]$Action,[string]$Label) {
    $ErrorActionPreference='Continue'
    & $Action
    if($LASTEXITCODE -ne 0){throw "$Label failed (exit $LASTEXITCODE)."}
}
Push-Location $ProjectRoot
try {
    Get-Command $Python -ErrorAction Stop | Out-Null
    if(-not $SkipWeb){Get-Command npm.cmd,node -ErrorAction Stop | Out-Null}
    Invoke-Checked { & $Python -c 'import sys; assert sys.version_info[:2] == (3,11), "Use Python 3.11"' } 'Python version check'
    if(-not (Test-Path -LiteralPath '.venv/Scripts/python.exe')) {
        Invoke-Checked { & $Python -m venv .venv } 'Virtual environment creation'
    }
    $ProjectPython=Join-Path $ProjectRoot '.venv/Scripts/python.exe'
    Invoke-Checked { & $ProjectPython -c 'import sys; assert sys.version_info[:2] == (3,11), "Existing .venv must use Python 3.11"' } 'Environment version check'
    Invoke-Checked { & $ProjectPython -m pip install -r requirements-api.lock.txt } 'Python installation'
    New-Item -ItemType Directory -Force -Path '.runtime' | Out-Null
    if($JavaHome) {
        $JdkPath=(Resolve-Path -LiteralPath $JavaHome).Path
        if(-not (Test-Path -LiteralPath (Join-Path $JdkPath 'bin/javac.exe'))){throw 'JavaHome must point to a JDK, not a JRE.'}
        $ErrorActionPreference='Continue'
        $JavaVersion=& (Join-Path $JdkPath 'bin/java.exe') -version 2>&1
        $ErrorActionPreference='Stop'
        if($LASTEXITCODE -ne 0 -or "$JavaVersion" -notmatch 'version "17[.]'){throw 'Use a Java 17 JDK.'}
        [System.IO.File]::WriteAllText((Join-Path $ProjectRoot '.runtime/java_home.txt'),$JdkPath)
    } else {
        Invoke-Checked { & $ProjectPython scripts/bootstrap_data.py --jdk } 'Portable JDK installation'
    }
    & "$PSScriptRoot/build_local_fs.ps1"
    Invoke-Checked { & $ProjectPython scripts/check_repo.py } 'Demo artifact verification'
    if(-not $SkipWeb) {
        Push-Location 'web'
        try {
            Invoke-Checked { & npm.cmd ci } 'Frontend installation'
            Invoke-Checked { & npm.cmd run build } 'Frontend build'
        } finally { Pop-Location }
    }
    Write-Host 'Setup complete. Run: ./scripts/start-local.ps1'
} finally { Pop-Location }
