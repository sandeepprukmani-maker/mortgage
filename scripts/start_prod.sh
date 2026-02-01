#!/bin/bash
# Start Valargen production environment on Azure VM (D4s v3)
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "=== Valargen Production Environment ==="
echo "VM: Azure D4s v3 (4 vCPU, 16GB RAM)"
echo ""

# Check for .env.prod
if [ ! -f ".env.prod" ]; then
    echo "ERROR: .env.prod not found"
    echo "Copy from sample: cp .env.prod.sample .env.prod"
    echo "Then configure your production settings"
    exit 1
fi

# Load environment
export $(grep -v '^#' .env.prod | xargs)

# Validate critical variables
if [ -z "$DOMAIN" ]; then
    echo "ERROR: DOMAIN not set in .env.prod"
    exit 1
fi

if [[ "$DATABASE_URL" == *"CHANGE_THIS"* ]]; then
    echo "ERROR: DATABASE_URL contains default password. Update .env.prod"
    exit 1
fi

echo "Domain: $DOMAIN"
echo ""

# Pull latest images (optional)
if [ "$1" = "--pull" ]; then
    echo "Pulling latest base images..."
    docker compose -f docker-compose.yml -f docker-compose.prod.yml pull
fi

# Build if needed
echo "Building containers..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml build

# Start services
echo "Starting services..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Wait for health checks
echo ""
echo "Waiting for services to be healthy..."
sleep 15

# Check health
echo ""
echo "Checking application health..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:80/health 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    echo "Health check: PASSED"
else
    echo "Health check: PENDING (HTTP $HTTP_CODE)"
    echo "Services may still be starting. Check logs if issue persists."
fi

# Show status
echo ""
echo "=== Service Status ==="
docker compose -f docker-compose.yml -f docker-compose.prod.yml ps

# Show resource usage
echo ""
echo "=== Resource Usage ==="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"

echo ""
echo "=== Access URLs ==="
echo "Frontend:  https://$DOMAIN"
echo "API:       https://$DOMAIN/api"
echo "Health:    https://$DOMAIN/health"

echo ""
echo "=== Useful Commands ==="
echo "View logs:    docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f"
echo "Stop:         ./scripts/stop_prod.sh"
echo "Backup:       ./scripts/backup.sh"
echo "Restart:      ./scripts/stop_prod.sh && ./scripts/start_prod.sh"
