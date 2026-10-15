param([switch]$Lan,[int]$Port=3000,[ValidatePattern('^[1-9][0-9]*[gm]$')][string]$DriverMemory='2g')
$ErrorActionPreference='Stop'
$ApiPort=8000
$ProjectRoot=Split-Path $PSScriptRoot -Parent
foreach($ServicePort in @($Port,$ApiPort)) {
    $Listener=[System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any,$ServicePort)
    try { $Listener.Start() } catch { throw "Port $ServicePort is occupied. Stop the existing instance or select other ports." } finally { $Listener.Stop() }
}
if (-not (Test-Path -LiteralPath "$ProjectRoot/web/.next/BUILD_ID")) { throw 'Build the frontend first: cd web; npm ci; npm run build' }
$ApiJob=Start-Job -ArgumentList $ProjectRoot,$ApiPort,$DriverMemory -ScriptBlock {
    param($Root,$ServicePort,$Heap)
    & "$Root/scripts/run.ps1" -Module src.api.serve -DriverMemory $Heap --port $ServicePort
}
try {
    Write-Host "Loading saved Spark models (demo driver $DriverMemory). This can take about one minute..."
    $Ready=$false
    for($Attempt=0;$Attempt -lt 150;$Attempt++) {
        if($ApiJob.State -eq 'Failed' -or $ApiJob.State -eq 'Completed') { Receive-Job $ApiJob -ErrorAction Continue; throw 'API exited during startup.' }
        try { $Health=Invoke-RestMethod "http://127.0.0.1:$ApiPort/api/v1/health" -TimeoutSec 1; $Ready=$Health.status -eq 'ready' } catch {}
        if($Ready){break}; Start-Sleep -Seconds 1
    }
    if(-not $Ready) { Receive-Job $ApiJob -ErrorAction Continue; throw 'API did not become ready.' }
    $env:API_BASE_URL="http://127.0.0.1:$ApiPort"
    $BindAddress=if($Lan){'0.0.0.0'}else{'127.0.0.1'}
    Write-Host "Open http://localhost:$Port/ . Press Ctrl+C in this terminal to stop."
    if($Lan){Write-Host "LAN: open http://<this-machine-LAN-IP>:$Port/ from a device on the same trusted network."}
    Push-Location "$ProjectRoot/web"
    try { & npm.cmd exec -- next start --hostname $BindAddress --port $Port } finally { Pop-Location }
} finally {
    Stop-Job $ApiJob -ErrorAction SilentlyContinue
    Receive-Job $ApiJob -ErrorAction SilentlyContinue
    Remove-Job $ApiJob -Force -ErrorAction SilentlyContinue
}
