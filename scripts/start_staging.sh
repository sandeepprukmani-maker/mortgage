#!/bin/bash
# Start Valargen staging environment on Azure VM (D2s v3)
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "=== Valargen Staging Environment ==="
echo "VM: Azure D2s v3 (2 vCPU, 8GB RAM)"
echo ""

# Check for .env.staging
if [ ! -f ".env.staging" ]; then
    echo "Warning: .env.staging not found"
    echo "Copy from sample: cp .env.staging.sample .env.staging"
    echo "Continuing with defaults..."
    echo ""
fi

# Load environment if exists
if [ -f ".env.staging" ]; then
    export $(grep -v '^#' .env.staging | xargs)
fi

# Check domain is set
if [ -z "$DOMAIN" ]; then
    echo "Note: DOMAIN not set, using default 'staging.valargen.com'"
    echo "Set DOMAIN in .env.staging or edit Caddyfile for IP-only access"
    echo ""
fi

# Pull latest images (optional)
if [ "$1" = "--pull" ]; then
    echo "Pulling latest base images..."
    docker compose -f docker-compose.yml -f docker-compose.staging.yml pull
fi

# Build if needed
echo "Building containers..."
docker compose -f docker-compose.yml -f docker-compose.staging.yml build

# Start services
echo "Starting services..."
docker compose -f docker-compose.yml -f docker-compose.staging.yml up -d

# Wait for health checks
echo ""
echo "Waiting for services to be healthy..."
sleep 10

# Show status
echo ""
echo "=== Service Status ==="
docker compose -f docker-compose.yml -f docker-compose.staging.yml ps

# Show resource usage
echo ""
echo "=== Resource Usage ==="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"

echo ""
echo "=== Access URLs ==="
if [ -n "$DOMAIN" ]; then
    echo "Frontend:  https://$DOMAIN"
    echo "API:       https://$DOMAIN/api"
    echo "API Docs:  https://$DOMAIN/docs"
else
    echo "Frontend:  http://<VM-IP>"
    echo "API:       http://<VM-IP>/api"
    echo "API Docs:  http://<VM-IP>/docs"
fi

echo ""
echo "=== Useful Commands ==="
echo "View logs:    docker compose -f docker-compose.yml -f docker-compose.staging.yml logs -f"
echo "Stop:         ./scripts/stop_staging.sh"
echo "Restart:      ./scripts/stop_staging.sh && ./scripts/start_staging.sh"
