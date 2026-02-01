#!/bin/bash
# Stop Valargen production environment
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "=== Stopping Valargen Production ==="

# Load environment if exists
if [ -f ".env.prod" ]; then
    export $(grep -v '^#' .env.prod | xargs)
fi

# Graceful shutdown
echo "Stopping services gracefully..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml down --timeout 30

echo ""
echo "Production environment stopped."
echo ""
echo "WARNING: To remove all data (DANGEROUS): docker compose -f docker-compose.yml -f docker-compose.prod.yml down -v"
