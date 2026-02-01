#!/bin/bash
# Stop local Docker environment

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo -e "${BLUE}Stopping Valargen Local Environment...${NC}"

cd "$PROJECT_ROOT"

# Check if any containers are running
if ! docker compose ps -q 2>/dev/null | grep -q .; then
    echo -e "${YELLOW}No containers running${NC}"
    exit 0
fi

# Stop containers
docker compose down

echo ""
echo -e "${GREEN}Local environment stopped${NC}"
echo ""
echo -e "${BLUE}Options:${NC}"
echo "  Remove volumes:  docker compose down -v"
echo "  Remove images:   docker compose down --rmi local"
echo "  Start again:     ./scripts/start_local.sh"
