# Stop local Docker environment (Windows)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "Stopping Valargen Local Environment..." -ForegroundColor Blue

Set-Location $ProjectRoot

# Check if any containers are running
$runningContainers = docker compose ps -q 2>$null
if (-not $runningContainers) {
    Write-Host "No containers running" -ForegroundColor Yellow
    exit 0
}

# Stop containers
docker compose down

Write-Host ""
Write-Host "Local environment stopped" -ForegroundColor Green
Write-Host ""
Write-Host "Options:" -ForegroundColor Blue
Write-Host "  Remove volumes:  docker compose down -v"
Write-Host "  Remove images:   docker compose down --rmi local"
Write-Host "  Start again:     .\scripts\start_local.ps1"
