# Start local development environment with Docker Compose (Windows)
# Simulates Azure architecture locally
#
# Usage:
#   .\start_local.ps1           # Normal start
#   .\start_local.ps1 -Fresh    # Rebuild images and refresh dependencies
#   .\start_local.ps1 -Client   # Refresh client dependencies only
#   .\start_local.ps1 -Help     # Show help

param(
    [switch]$Fresh,
    [switch]$Client,
    [Alias('h')]
    [switch]$Help
)

$ErrorActionPreference = "Stop"

# Show help
if ($Help) {
    Write-Host "Usage: .\start_local.ps1 [OPTIONS]" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Fresh    Rebuild images and refresh all dependencies"
    Write-Host "  -Client   Refresh client dependencies (npm install)"
    Write-Host "  -Help     Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\start_local.ps1              # Normal start"
    Write-Host "  .\start_local.ps1 -Fresh       # Full rebuild"
    Write-Host "  .\start_local.ps1 -Client      # Refresh client deps"
    exit 0
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Colors for output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-Host "==========================================" -ForegroundColor Blue
Write-Host "  Valargen Local Development Environment" -ForegroundColor Blue
Write-Host "  (Windows)" -ForegroundColor Blue
Write-Host "==========================================" -ForegroundColor Blue
Write-Host ""

# Run pre-flight checks
$preflightScript = Join-Path $ScriptDir "preflight-check.ps1"
if (Test-Path $preflightScript) {
    & $preflightScript
    if ($LASTEXITCODE -ne 0) {
        exit 1
    }
    Write-Host ""
}

# Check Docker is running
try {
    $null = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Docker not running"
    }
} catch {
    Write-Host "Error: Docker is not running" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again"
    exit 1
}

# Fix Docker Buildx issue on Windows - switch to default builder
Write-Host "Configuring Docker builder for Windows..." -ForegroundColor Yellow
try {
    # Check current builder
    $currentBuilder = docker buildx inspect 2>&1
    if ($currentBuilder -match "docker-container") {
        Write-Host "Switching to default Docker builder (fixes EOF error)..." -ForegroundColor Yellow
        docker buildx use default 2>&1 | Out-Null
    }
} catch {
    # Ignore errors, continue with default
}
Write-Host "Docker builder configured" -ForegroundColor Green

# Create .env if missing
$envFile = Join-Path $ProjectRoot "app\server\.env"
$envSample = Join-Path $ProjectRoot "app\server\.env.sample"
$envLocal = Join-Path $ProjectRoot "app\server\.env.local"

if (-not (Test-Path $envFile)) {
    if (Test-Path $envLocal) {
        Write-Host "Copying .env.local to .env..." -ForegroundColor Yellow
        Copy-Item $envLocal $envFile
    } elseif (Test-Path $envSample) {
        Write-Host "Creating .env from .env.sample..." -ForegroundColor Yellow
        Copy-Item $envSample $envFile
    } else {
        Write-Host "Creating default .env..." -ForegroundColor Yellow
        @"
# Local development - Key Vault disabled, uses env vars
DATABASE_URL=postgresql://valargen:valargen@localhost:6432/valargen
REDIS_URL=redis://localhost:6379
KEY_VAULT_NAME=
"@ | Out-File -FilePath $envFile -Encoding utf8
    }
    Write-Host "Created app/server/.env" -ForegroundColor Green
}

# Change to project root
Set-Location $ProjectRoot

# Fresh build - rebuild images and clear volumes
if ($Fresh) {
    Write-Host "Fresh build requested - removing containers and volumes..." -ForegroundColor Yellow
    docker compose -f docker-compose.yml -f docker-compose.override.yml down -v 2>$null
    Write-Host "Rebuilding images with --no-cache..." -ForegroundColor Yellow
    docker compose -f docker-compose.yml -f docker-compose.override.yml build --no-cache
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Build failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "Images rebuilt" -ForegroundColor Green
    Write-Host ""
}

# Start services with explicit build
Write-Host "Building and starting Docker services..." -ForegroundColor Green
Write-Host "(This may take a few minutes on first run)" -ForegroundColor Gray

# Build with default driver (fixes EOF error) - skip if Fresh already built
if (-not $Fresh) {
    docker compose -f docker-compose.yml -f docker-compose.override.yml build
}
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed. Trying with --no-cache..." -ForegroundColor Yellow
    docker compose -f docker-compose.yml -f docker-compose.override.yml build --no-cache
}

# Start services with local override
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to start services" -ForegroundColor Red
    Write-Host "Check logs with: docker compose logs"
    exit 1
}

# Wait for services to be healthy
Write-Host "Waiting for services to be healthy..." -ForegroundColor Blue
$maxAttempts = 30
$attempt = 0

while ($attempt -lt $maxAttempts) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.Content -match "connected|disconnected") {
            break
        }
    } catch {
        # Service not ready yet
    }
    $attempt++
    Write-Host -NoNewline "."
    Start-Sleep -Seconds 2
}
Write-Host ""

# Check health
try {
    $healthResponse = (Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5 -ErrorAction SilentlyContinue).Content
} catch {
    $healthResponse = '{"status":"error"}'
}

if ($healthResponse -match '"status":"connected"') {
    Write-Host "Server healthy - Database connected" -ForegroundColor Green
} elseif ($healthResponse -match '"status":"disconnected"') {
    Write-Host "Server running - Database not connected" -ForegroundColor Yellow
    Write-Host "  Check logs: docker compose logs postgres"
} else {
    Write-Host "Server starting... check logs with:" -ForegroundColor Yellow
    Write-Host "  docker compose logs -f server"
}

# Refresh client dependencies if requested
if ($Fresh -or $Client) {
    Write-Host ""
    Write-Host "Refreshing client dependencies..." -ForegroundColor Blue
    try {
        docker exec valargen-client npm install 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Client dependencies refreshed" -ForegroundColor Green
        } else {
            Write-Host "Could not refresh client dependencies" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "Could not refresh client dependencies" -ForegroundColor Yellow
    }
}

# Wait for client to be ready
Write-Host ""
Write-Host "Waiting for client to be ready..." -ForegroundColor Blue
$clientAttempts = 0
$clientMax = 15

while ($clientAttempts -lt $clientMax) {
    try {
        $clientResponse = Invoke-WebRequest -Uri "http://localhost:5173" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($clientResponse.StatusCode -eq 200) {
            Write-Host "Client ready" -ForegroundColor Green
            break
        }
    } catch {
        # Client not ready yet
    }
    $clientAttempts++
    Write-Host -NoNewline "."
    Start-Sleep -Seconds 2
}

if ($clientAttempts -eq $clientMax) {
    Write-Host ""
    Write-Host "Client may still be starting... check logs:" -ForegroundColor Yellow
    Write-Host "  docker compose logs -f client"
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  Local environment started!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Services:" -ForegroundColor Blue
Write-Host "  Server:     http://localhost:8000"
Write-Host "  API Docs:   http://localhost:8000/docs"
Write-Host "  Client:     http://localhost:5173"
Write-Host ""
Write-Host "Database:" -ForegroundColor Blue
Write-Host "  PostgreSQL: localhost:5432"
Write-Host "  Redis:      localhost:6379"
Write-Host ""
Write-Host "Commands:" -ForegroundColor Blue
Write-Host "  Logs:       docker compose logs -f"
Write-Host "  Server log: docker compose logs -f server"
Write-Host "  Client log: docker compose logs -f client"
Write-Host "  Stop:       .\scripts\stop_local.ps1"
Write-Host ""
Write-Host "Options:" -ForegroundColor Blue
Write-Host "  Refresh client:  .\scripts\start_local.ps1 -Client"
Write-Host "  Full rebuild:    .\scripts\start_local.ps1 -Fresh"
Write-Host ""
