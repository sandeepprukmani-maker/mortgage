#!/bin/bash
# Start local development environment with Docker Compose
# Simulates Azure architecture locally
#
# Usage:
#   ./start_local.sh           # Normal start
#   ./start_local.sh --fresh   # Rebuild images and refresh dependencies
#   ./start_local.sh --client  # Refresh client dependencies only

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

# Parse arguments
FRESH_BUILD=false
REFRESH_CLIENT=false

for arg in "$@"; do
    case $arg in
        --fresh)
            FRESH_BUILD=true
            REFRESH_CLIENT=true
            ;;
        --client)
            REFRESH_CLIENT=true
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --fresh    Rebuild images and refresh all dependencies"
            echo "  --client   Refresh client dependencies (npm install)"
            echo "  --help     Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0              # Normal start"
            echo "  $0 --fresh      # Full rebuild"
            echo "  $0 --client     # Refresh client deps"
            exit 0
            ;;
    esac
done

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}  Valargen Local Development Environment${NC}"
echo -e "${BLUE}==========================================${NC}"

# Run pre-flight checks
if [ -f "$SCRIPT_DIR/preflight-check.sh" ]; then
    bash "$SCRIPT_DIR/preflight-check.sh" || exit 1
    echo ""
fi

# Check Docker
if ! docker info &>/dev/null; then
    echo -e "${RED}Error: Docker is not running${NC}"
    echo "Please start Docker and try again"
    exit 1
fi

# Create .env if missing
if [ ! -f "$PROJECT_ROOT/app/server/.env" ]; then
    if [ -f "$PROJECT_ROOT/app/server/.env.local" ]; then
        echo -e "${YELLOW}Copying .env.local to .env...${NC}"
        cp "$PROJECT_ROOT/app/server/.env.local" "$PROJECT_ROOT/app/server/.env"
    elif [ -f "$PROJECT_ROOT/app/server/.env.sample" ]; then
        echo -e "${YELLOW}Creating .env from .env.sample...${NC}"
        cp "$PROJECT_ROOT/app/server/.env.sample" "$PROJECT_ROOT/app/server/.env"
    else
        echo -e "${YELLOW}Creating default .env...${NC}"
        cat > "$PROJECT_ROOT/app/server/.env" << 'EOF'
# Local development - Key Vault disabled, uses env vars
DATABASE_URL=postgresql://valargen:valargen@localhost:6432/valargen
REDIS_URL=redis://localhost:6379
KEY_VAULT_NAME=
EOF
    fi
    echo -e "${GREEN}Created app/server/.env${NC}"
fi

cd "$PROJECT_ROOT"

# Fresh build - rebuild images and clear volumes
if [ "$FRESH_BUILD" = true ]; then
    echo -e "${YELLOW}Fresh build requested - removing containers and volumes...${NC}"
    docker compose -f docker-compose.yml -f docker-compose.override.yml down -v 2>/dev/null || true
    echo -e "${YELLOW}Rebuilding images with --no-cache...${NC}"
    docker compose -f docker-compose.yml -f docker-compose.override.yml build --no-cache
    echo -e "${GREEN}Images rebuilt${NC}"
    echo ""
fi

# Start services with local override
echo -e "${GREEN}Starting Docker services with local override...${NC}"
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d

# Wait for services to be healthy
echo -e "${BLUE}Waiting for services to be healthy...${NC}"
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -s http://localhost:8000/health 2>/dev/null | grep -q "connected\|disconnected"; then
        break
    fi
    attempt=$((attempt + 1))
    echo -n "."
    sleep 2
done
echo ""

# Check health
health_response=$(curl -s http://localhost:8000/health 2>/dev/null || echo '{"status":"error"}')

if echo "$health_response" | grep -q '"status":"connected"'; then
    echo -e "${GREEN}Server healthy - Database connected${NC}"
elif echo "$health_response" | grep -q '"status":"disconnected"'; then
    echo -e "${YELLOW}Server running - Database not connected${NC}"
    echo "  Check logs: docker compose logs postgres"
else
    echo -e "${YELLOW}Server starting... check logs with:${NC}"
    echo "  docker compose logs -f server"
fi

# Refresh client dependencies if requested
if [ "$REFRESH_CLIENT" = true ]; then
    echo ""
    echo -e "${BLUE}Refreshing client dependencies...${NC}"
    docker exec valargen-client npm install 2>/dev/null && \
        echo -e "${GREEN}Client dependencies refreshed${NC}" || \
        echo -e "${YELLOW}Could not refresh client dependencies${NC}"
fi

# Wait for client to be ready
echo ""
echo -e "${BLUE}Waiting for client to be ready...${NC}"
client_attempts=0
client_max=15
while [ $client_attempts -lt $client_max ]; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:5173 2>/dev/null | grep -q "200"; then
        echo -e "${GREEN}Client ready${NC}"
        break
    fi
    client_attempts=$((client_attempts + 1))
    echo -n "."
    sleep 2
done
if [ $client_attempts -eq $client_max ]; then
    echo ""
    echo -e "${YELLOW}Client may still be starting... check logs:${NC}"
    echo "  docker compose logs -f client"
fi

echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}  Local environment started!${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo -e "${BLUE}Services:${NC}"
echo "  Server:     http://localhost:8000"
echo "  API Docs:   http://localhost:8000/docs"
echo "  Client:     http://localhost:5173"
echo ""
echo -e "${BLUE}Database:${NC}"
echo "  PostgreSQL: localhost:5432"
echo "  Redis:      localhost:6379"
echo ""
echo -e "${BLUE}Commands:${NC}"
echo "  Logs:       docker compose logs -f"
echo "  Server log: docker compose logs -f server"
echo "  Client log: docker compose logs -f client"
echo "  Stop:       ./scripts/stop_local.sh"
echo ""
echo -e "${BLUE}Options:${NC}"
echo "  Refresh client:  ./scripts/start_local.sh --client"
echo "  Full rebuild:    ./scripts/start_local.sh --fresh"
echo ""
