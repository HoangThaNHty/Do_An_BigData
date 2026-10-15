$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path $PSScriptRoot -Parent
$JdkRoot = (Get-Content -LiteralPath (Join-Path $ProjectRoot '.runtime/java_home.txt') -Raw).Trim()
$BuildRoot = Join-Path $ProjectRoot '.runtime/java-classes'
$SparkJars = Join-Path $ProjectRoot '.venv/Lib/site-packages/pyspark/jars/*'
$OutputJar = Join-Path $ProjectRoot '.runtime/project-local-fs.jar'
New-Item -ItemType Directory -Force -Path $BuildRoot | Out-Null
& "$JdkRoot/bin/javac.exe" -encoding UTF-8 -cp $SparkJars -d $BuildRoot (Join-Path $ProjectRoot 'src/java/ProjectLocalFileSystem.java')
if ($LASTEXITCODE -ne 0) { throw 'Java adapter compilation failed.' }
& "$JdkRoot/bin/jar.exe" --create --file $OutputJar -C $BuildRoot .
if ($LASTEXITCODE -ne 0) { throw 'Java adapter packaging failed.' }
Write-Output $OutputJar
