#!/bin/bash
# Pre-deployment verification script
# Run this BEFORE ./scripts/deploy.sh to catch issues early

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}  Valargen Deployment Verification${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

ERRORS=0
WARNINGS=0

# Helper functions
error() {
    echo -e "${RED}✗ ERROR: $1${NC}"
    ERRORS=$((ERRORS + 1))
}

warn() {
    echo -e "${YELLOW}⚠ WARNING: $1${NC}"
    WARNINGS=$((WARNINGS + 1))
}

ok() {
    echo -e "${GREEN}✓ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# 1. Check git status
echo -e "${BLUE}[1/10] Checking Git Status...${NC}"
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    error "Uncommitted changes detected - git pull will fail"
    git status --short
else
    ok "No uncommitted changes"
fi

# Check if behind remote
git fetch origin $(git branch --show-current) 2>/dev/null
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u} 2>/dev/null || echo "")
if [ -n "$REMOTE" ] && [ "$LOCAL" != "$REMOTE" ]; then
    error "Local branch diverged from remote - git pull will fail"
    echo "  Run: git pull origin $(git branch --show-current)"
else
    ok "Git in sync with remote"
fi
echo ""

# 2. Check environment file
echo -e "${BLUE}[2/10] Checking Environment Configuration...${NC}"
if [ ! -f ".env.staging" ]; then
    error ".env.staging not found"
    echo "  Run: cp .env.staging.sample .env.staging"
else
    ok ".env.staging exists"

    # Check critical variables
    source .env.staging

    if [ -z "$DOMAIN" ]; then
        error "DOMAIN not set in .env.staging"
    else
        ok "DOMAIN configured: $DOMAIN"
    fi

    if [ "$POSTGRES_PASSWORD" = "your-secure-password-here" ] || [ "$POSTGRES_PASSWORD" = "valargen" ]; then
        error "POSTGRES_PASSWORD not changed from default!"
    else
        ok "POSTGRES_PASSWORD configured (not showing for security)"
    fi

    if [ -z "$TWINGATE_REFRESH_TOKEN" ] || [ "$TWINGATE_REFRESH_TOKEN" = "your-connector-refresh-token-here" ]; then
        warn "TWINGATE_REFRESH_TOKEN not configured (needed for UWM API)"
    else
        ok "TWINGATE_REFRESH_TOKEN configured"
    fi
fi
echo ""

# 3. Check Docker
echo -e "${BLUE}[3/10] Checking Docker...${NC}"
if ! docker info >/dev/null 2>&1; then
    error "Docker is not running"
else
    ok "Docker is running"
fi
echo ""

# 4. Check disk space
echo -e "${BLUE}[4/10] Checking Disk Space...${NC}"
DISK_AVAIL=$(df -BG / | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$DISK_AVAIL" -lt 10 ]; then
    error "Low disk space: ${DISK_AVAIL}GB available (need 10GB+)"
else
    ok "Disk space: ${DISK_AVAIL}GB available"
fi
echo ""

# 5. Check memory
echo -e "${BLUE}[5/10] Checking Memory...${NC}"
MEM_TOTAL=$(free -g | grep Mem | awk '{print $2}')
if [ "$MEM_TOTAL" -lt 7 ]; then
    warn "Low memory: ${MEM_TOTAL}GB (8GB recommended for staging)"
else
    ok "Memory: ${MEM_TOTAL}GB available"
fi
echo ""

# 6. Check DNS (if DOMAIN is set)
echo -e "${BLUE}[6/10] Checking DNS Configuration...${NC}"
if [ -n "$DOMAIN" ] && [ "$DOMAIN" != "your-domain-here" ]; then
    DNS_IP=$(dig +short "$DOMAIN" | tail -1)
    if [ -z "$DNS_IP" ]; then
        error "DNS not configured for $DOMAIN"
    else
        ok "DNS configured: $DOMAIN → $DNS_IP"

        # Check if it points to this server
        SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s api.ipify.org 2>/dev/null)
        if [ "$DNS_IP" != "$SERVER_IP" ]; then
            warn "DNS points to $DNS_IP but server IP is $SERVER_IP"
        else
            ok "DNS points to this server"
        fi
    fi
else
    warn "DOMAIN not configured - using IP access only"
fi
echo ""

# 7. Check required ports
echo -e "${BLUE}[7/10] Checking Required Ports...${NC}"
for PORT in 80 443; do
    if lsof -i :$PORT >/dev/null 2>&1 || ss -tuln 2>/dev/null | grep -q ":$PORT "; then
        PROCESS=$(lsof -i :$PORT 2>/dev/null | tail -1 | awk '{print $1}' || echo "unknown")
        if [ "$PROCESS" != "docker-pro" ] && [ "$PROCESS" != "unknown" ]; then
            warn "Port $PORT already in use by $PROCESS (may conflict)"
        else
            ok "Port $PORT available/in use by Docker"
        fi
    else
        ok "Port $PORT available"
    fi
done
echo ""

# 8. Check compose files
echo -e "${BLUE}[8/10] Checking Docker Compose Files...${NC}"
if [ ! -f "docker-compose.yml" ]; then
    error "docker-compose.yml not found"
else
    ok "docker-compose.yml exists"
fi

if [ ! -f "docker-compose.staging.yml" ]; then
    error "docker-compose.staging.yml not found"
else
    ok "docker-compose.staging.yml exists"
fi

# Test compose config
if docker compose --env-file .env.staging -f docker-compose.yml -f docker-compose.staging.yml config >/dev/null 2>&1; then
    ok "Docker Compose configuration valid"
else
    error "Docker Compose configuration invalid"
fi
echo ""

# 9. Check migration files
echo -e "${BLUE}[9/10] Checking Database Migrations...${NC}"
if [ -d "app/server/alembic/versions" ]; then
    MIGRATION_COUNT=$(ls -1 app/server/alembic/versions/*.py 2>/dev/null | wc -l)
    if [ "$MIGRATION_COUNT" -gt 0 ]; then
        ok "Found $MIGRATION_COUNT migration file(s)"
    else
        warn "No migration files found (first deployment?)"
    fi
else
    warn "Alembic versions directory not found"
fi
echo ""

# 10. Check Google OAuth (optional)
echo -e "${BLUE}[10/10] Checking OAuth Configuration...${NC}"
if [ -f "app/server/.env" ]; then
    if grep -q "GOOGLE_CLIENT_ID" app/server/.env; then
        ok "Google OAuth configured in app/server/.env"
        if [ -n "$DOMAIN" ]; then
            EXPECTED_REDIRECT="https://$DOMAIN/api/auth/google/callback"
            info "Verify Google Console has redirect URI: $EXPECTED_REDIRECT"
        fi
    else
        info "Google OAuth not configured (optional)"
    fi
else
    warn "app/server/.env not found (Google OAuth may not work)"
fi
echo ""

# Summary
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}  Verification Summary${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo -e "${GREEN}Ready to deploy:${NC}"
    echo "  ./scripts/deploy.sh"
    echo ""
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ ${WARNINGS} warning(s) found${NC}"
    echo ""
    echo -e "${YELLOW}You can proceed with deployment, but review warnings above.${NC}"
    echo ""
    read -p "Continue with deployment? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}Proceeding with deployment...${NC}"
        echo "  ./scripts/deploy.sh"
        exit 0
    else
        echo "Deployment cancelled"
        exit 1
    fi
else
    echo -e "${RED}✗ ${ERRORS} error(s) found${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠ ${WARNINGS} warning(s) found${NC}"
    fi
    echo ""
    echo -e "${RED}Fix errors above before deploying!${NC}"
    echo ""
    exit 1
fi
