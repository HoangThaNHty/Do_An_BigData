[CmdletBinding(PositionalBinding=$false)]
param(
    [Parameter(Mandatory=$true,Position=0)][string]$Module,
    [ValidatePattern('^$|^[1-9][0-9]*[gm]$')][string]$DriverMemory='',
    [Parameter(ValueFromRemainingArguments=$true)][string[]]$ModuleArgs
)
$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path $PSScriptRoot -Parent
$JavaHomeFile = Join-Path $ProjectRoot '.runtime/java_home.txt'
if (-not (Test-Path -LiteralPath $JavaHomeFile)) { throw 'Run scripts/bootstrap_data.py --jdk first.' }
$env:JAVA_HOME = (Get-Content -LiteralPath $JavaHomeFile -Raw).Trim()
$env:PATH = "$env:JAVA_HOME\bin;$env:PATH"
$env:TEMP = Join-Path $ProjectRoot '.runtime/temp'
$env:TMP = $env:TEMP
$env:SPARK_LOCAL_DIRS = Join-Path $ProjectRoot '.runtime/spark-tmp'
$env:SPARK_LOCAL_IP = '127.0.0.1'
$env:PYSPARK_PYTHON = Join-Path $ProjectRoot '.venv/Scripts/python.exe'
$env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON
$ResolvedDriverMemory = if($DriverMemory){$DriverMemory}elseif($Module -in @('src.api.serve','src.models.predict')){'2g'}else{'4g'}
$env:PYSPARK_SUBMIT_ARGS = "--driver-memory $ResolvedDriverMemory pyspark-shell"
$env:PYTHONIOENCODING = 'utf-8'
$env:REAL_ESTATE_ROOT = $ProjectRoot
$env:HF_HOME = Join-Path $ProjectRoot '.cache/huggingface'
New-Item -ItemType Directory -Force -Path $env:TEMP,$env:SPARK_LOCAL_DIRS | Out-Null
Push-Location $ProjectRoot
try {
    # Windows PowerShell 5.1 turns native stderr (including normal server logs)
    # into error records when run in a background job. Check the exit code
    # instead of terminating on informational stderr output.
    $ErrorActionPreference = 'Continue'
    & $env:PYSPARK_PYTHON -m $Module @ModuleArgs
    $ErrorActionPreference = 'Stop'
    if ($LASTEXITCODE -ne 0) { throw "Module failed: $Module (exit $LASTEXITCODE)" }
} finally { Pop-Location }
