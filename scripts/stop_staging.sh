#!/bin/bash
# Stop Valargen staging environment
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "=== Stopping Valargen Staging ==="

COMPOSE_FILES="--env-file .env.staging -f docker-compose.yml -f docker-compose.staging.yml"

# Stop services
docker compose $COMPOSE_FILES down

# Optionally remove volumes (data)
if [ "$1" = "--clean" ]; then
    echo "Removing volumes (all data will be lost)..."
    docker compose $COMPOSE_FILES down -v
fi

echo ""
echo "Staging environment stopped."
echo ""
echo "To remove all data: ./scripts/stop_staging.sh --clean"
