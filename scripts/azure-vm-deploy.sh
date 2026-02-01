#!/bin/bash
# Azure VM Deployment Script
# Called by Azure Pipeline via az vm run-command invoke
# Parameters: GIT_BRANCH, ENVIRONMENT

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}  Valargen Azure VM Deployment${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Parse parameters (passed from Azure Pipeline)
GIT_BRANCH="${1:-master}"
ENVIRONMENT="${2:-staging}"

echo -e "${BLUE}Configuration:${NC}"
echo "  Git Branch: $GIT_BRANCH"
echo "  Environment: $ENVIRONMENT"
echo ""

# Navigate to project directory
PROJECT_DIR="/home/valargen/valargen-main"
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}ERROR: Project directory not found: $PROJECT_DIR${NC}"
    exit 1
fi

cd "$PROJECT_DIR"

# Set compose files based on environment
if [ "$ENVIRONMENT" = "production" ]; then
    COMPOSE_FILES="--env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml"
    ENV_FILE=".env.prod"
    DOMAIN="app.valargen.com"
else
    COMPOSE_FILES="--env-file .env.staging -f docker-compose.yml -f docker-compose.staging.yml"
    ENV_FILE=".env.staging"
    DOMAIN="app.staging.valargen.com"
fi

# Check env file
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${RED}ERROR: $ENV_FILE not found${NC}"
    exit 1
fi

echo -e "${GREEN}[1/8] Pulling latest code...${NC}"
git fetch origin
git checkout "$GIT_BRANCH"
git pull origin "$GIT_BRANCH"
COMMIT_HASH=$(git rev-parse --short HEAD)
echo "  Deployed commit: $COMMIT_HASH"
echo ""

echo -e "${GREEN}[2/8] Building containers...${NC}"
docker compose $COMPOSE_FILES build --no-cache
echo ""

echo -e "${GREEN}[3/8] Backing up database...${NC}"
BACKUP_FILE="backups/pre-deploy-$(date +%Y%m%d-%H%M%S).sql"
mkdir -p backups
docker compose $COMPOSE_FILES exec -T postgres pg_dump -U valargen valargen > "$BACKUP_FILE" 2>/dev/null || echo "  Warning: Backup failed (might be first deployment)"
if [ -f "$BACKUP_FILE" ]; then
    echo "  Backup saved: $BACKUP_FILE"
fi
echo ""

echo -e "${GREEN}[4/8] Stopping old containers...${NC}"
docker compose $COMPOSE_FILES down --timeout 30
echo ""

echo -e "${GREEN}[5/8] Starting new containers...${NC}"
docker compose $COMPOSE_FILES up -d
echo ""

echo -e "${GREEN}[6/8] Waiting for health check...${NC}"
MAX_ATTEMPTS=30
ATTEMPT=1
HEALTH_OK=false

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    echo "  Health check attempt $ATTEMPT/$MAX_ATTEMPTS..."

    if docker exec valargen-server python -c "import urllib.request; r=urllib.request.urlopen('http://localhost:8000/health', timeout=5); exit(0 if r.status == 200 else 1)" 2>/dev/null; then
        echo -e "  ${GREEN}✓ Health check: PASSED${NC}"
        HEALTH_OK=true
        break
    fi

    if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
        echo -e "  ${RED}✗ Health check: FAILED after $MAX_ATTEMPTS attempts${NC}"
        echo ""
        echo "Rolling back to backup..."
        docker compose $COMPOSE_FILES down
        # Restore backup if exists
        if [ -f "$BACKUP_FILE" ]; then
            docker compose $COMPOSE_FILES up -d postgres
            sleep 10
            cat "$BACKUP_FILE" | docker compose $COMPOSE_FILES exec -T postgres psql -U valargen valargen
            docker compose $COMPOSE_FILES up -d
        fi
        docker compose $COMPOSE_FILES logs --tail=100
        exit 1
    fi

    sleep 5
    ATTEMPT=$((ATTEMPT + 1))
done
echo ""

if [ "$HEALTH_OK" = true ]; then
    echo -e "${GREEN}[7/8] Running database migrations...${NC}"
    if docker exec valargen-server /app/.venv/bin/python -m alembic upgrade head 2>&1; then
        echo -e "  ${GREEN}✓ Migrations: PASSED${NC}"
    else
        echo -e "  ${RED}✗ Migrations: FAILED${NC}"
        docker compose $COMPOSE_FILES logs --tail=50 server
        exit 1
    fi
    echo ""

    echo -e "${GREEN}[8/8] Cleaning up old images...${NC}"
    docker image prune -f
    echo ""

    echo -e "${GREEN}=========================================${NC}"
    echo -e "${GREEN}  Deployment Complete!${NC}"
    echo -e "${GREEN}=========================================${NC}"
    echo ""
    echo "Environment: $ENVIRONMENT"
    echo "Commit: $COMMIT_HASH"
    echo "URL: https://$DOMAIN"
    echo ""
    echo "Running containers:"
    docker compose $COMPOSE_FILES ps
    echo ""
    echo -e "${GREEN}✓ Deployment successful!${NC}"
else
    echo -e "${RED}Deployment failed - health check did not pass${NC}"
    exit 1
fi
