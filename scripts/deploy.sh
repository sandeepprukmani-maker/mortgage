#!/bin/bash
# Deploy latest code to Valargen VM (staging)
# Usage: ./scripts/deploy.sh
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "=== Valargen Deployment: staging ==="
echo ""

# Compose files for staging
COMPOSE_FILES="--env-file .env.staging -f docker-compose.yml -f docker-compose.staging.yml"
ENV_FILE=".env.staging"

# Check env file
if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: $ENV_FILE not found"
    exit 1
fi

echo "1. Pulling latest code..."
git pull origin $(git branch --show-current)

echo ""
echo "2. Building containers..."
docker compose $COMPOSE_FILES build

echo ""
echo "3. Stopping old containers..."
docker compose $COMPOSE_FILES down --timeout 30

echo ""
echo "4. Starting new containers..."
docker compose $COMPOSE_FILES up -d

echo ""
echo "5. Waiting for health check..."

# Retry health check with timeout (server needs time to build/start)
MAX_ATTEMPTS=20
ATTEMPT=1
while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    echo "Health check attempt $ATTEMPT/$MAX_ATTEMPTS..."
    HTTP_CODE=$(docker exec valargen-server python -c "import urllib.request; r=urllib.request.urlopen('http://localhost:8000/health'); print(r.status)" 2>/dev/null || echo "000")
    if [ "$HTTP_CODE" = "200" ]; then
        echo "Health check: PASSED"
        break
    fi
    if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
        echo "Health check: FAILED after $MAX_ATTEMPTS attempts (last HTTP $HTTP_CODE)"
        echo "Rolling back..."
        docker compose $COMPOSE_FILES logs --tail=50
        exit 1
    fi
    sleep 5
    ATTEMPT=$((ATTEMPT + 1))
done

echo ""
echo "6. Running database migrations..."
if docker exec valargen-server /app/.venv/bin/python -m alembic upgrade head 2>&1; then
    echo "Migrations: PASSED"
else
    echo "Migrations: FAILED"
    docker compose $COMPOSE_FILES logs --tail=50 server
    exit 1
fi

echo ""
echo "7. Cleaning up old images..."
docker image prune -f

echo ""
echo "=== Deployment Complete ==="
docker compose $COMPOSE_FILES ps
