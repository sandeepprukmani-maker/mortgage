# Pre-flight checks before starting Valargen (Windows)

$ErrorActionPreference = "Stop"
$script:exitCode = 0

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "Running pre-flight checks..." -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
try {
    $null = Get-Command docker -ErrorAction Stop
    Write-Host "[OK] Docker is installed" -ForegroundColor Green
} catch {
    Write-Host "[X] Docker is not installed" -ForegroundColor Red
    Write-Host "    Install Docker Desktop: https://docs.docker.com/desktop/install/windows-install/"
    exit 1
}

# Check if Docker is running
try {
    $null = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not running"
    }
    Write-Host "[OK] Docker is running" -ForegroundColor Green
} catch {
    Write-Host "[X] Docker is not running" -ForegroundColor Red
    Write-Host "    Please start Docker Desktop"
    exit 1
}

# Check if Docker Compose is available
try {
    $null = docker compose version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Docker Compose not available"
    }
    Write-Host "[OK] Docker Compose is available" -ForegroundColor Green
} catch {
    Write-Host "[X] Docker Compose is not available" -ForegroundColor Red
    Write-Host "    Docker Compose should be included with Docker Desktop"
    exit 1
}

# Check Docker Buildx configuration (fix for Windows EOF error)
Write-Host "[..] Checking Docker Buildx configuration..." -ForegroundColor Gray
try {
    $builderInfo = docker buildx inspect 2>&1
    if ($builderInfo -match "Driver:\s+docker-container") {
        Write-Host "[!] Docker Buildx using docker-container driver" -ForegroundColor Yellow
        Write-Host "    This may cause EOF errors on Windows."
        Write-Host "    The start script will automatically switch to default builder."
    } else {
        Write-Host "[OK] Docker Buildx configuration OK" -ForegroundColor Green
    }
} catch {
    Write-Host "[OK] Docker Buildx using default configuration" -ForegroundColor Green
}

# Check if .env.local or .env exists
$envLocal = Join-Path $ProjectRoot "app\server\.env.local"
$envFile = Join-Path $ProjectRoot "app\server\.env"
$envSample = Join-Path $ProjectRoot "app\server\.env.sample"

if (Test-Path $envLocal) {
    Write-Host "[OK] Environment file exists (.env.local)" -ForegroundColor Green
} elseif (Test-Path $envFile) {
    Write-Host "[OK] Environment file exists (.env)" -ForegroundColor Green
} elseif (Test-Path $envSample) {
    Write-Host "[!] No .env file found, but .env.sample exists" -ForegroundColor Yellow
    Write-Host "    The start script will create .env from .env.sample"
} else {
    Write-Host "[!] No environment file found" -ForegroundColor Yellow
    Write-Host "    The start script will create a default .env"
}

# Check available disk space (Docker needs space for images)
try {
    $drive = (Get-Item $ProjectRoot).PSDrive.Name
    $freeSpace = (Get-PSDrive $drive).Free / 1GB
    if ($freeSpace -lt 5) {
        Write-Host "[!] Low disk space: $([math]::Round($freeSpace, 1)) GB free" -ForegroundColor Yellow
        Write-Host "    Docker images may require several GB of space"
    } else {
        Write-Host "[OK] Disk space: $([math]::Round($freeSpace, 1)) GB free" -ForegroundColor Green
    }
} catch {
    # Ignore disk space check errors
}

# Check if ports are available
$portsToCheck = @(
    @{Port = 8000; Service = "Server API"},
    @{Port = 5173; Service = "Client (Vite)"},
    @{Port = 5432; Service = "PostgreSQL"},
    @{Port = 6432; Service = "PgBouncer"},
    @{Port = 6379; Service = "Redis"}
)

$portsInUse = @()
foreach ($portInfo in $portsToCheck) {
    $connection = Get-NetTCPConnection -LocalPort $portInfo.Port -ErrorAction SilentlyContinue
    if ($connection) {
        $portsInUse += $portInfo
    }
}

if ($portsInUse.Count -gt 0) {
    Write-Host "[!] Some ports are already in use:" -ForegroundColor Yellow
    foreach ($portInfo in $portsInUse) {
        Write-Host "    Port $($portInfo.Port) ($($portInfo.Service))" -ForegroundColor Yellow
    }
    Write-Host "    This may be from a previous run. Try: .\scripts\stop_local.ps1"
} else {
    Write-Host "[OK] Required ports are available" -ForegroundColor Green
}

Write-Host ""
Write-Host "[OK] All pre-flight checks passed!" -ForegroundColor Green
Write-Host ""

exit 0
