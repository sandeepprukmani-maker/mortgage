# Valargen Local Development Setup

Complete setup guide for running Valargen locally.

## Prerequisites

- Docker and Docker Compose v2+
- Ubuntu/Debian Linux (for UFW firewall fix)
- Twingate (for UWM API access - optional)

## Initial Setup

### 1. Environment Configuration

Create local environment file:

```bash
cp app/server/.env.sample app/server/.env.local
```

**Required environment variables in `.env.local`:**

```bash
# Database (auto-configured by docker-compose.override.yml)
DATABASE_URL=postgresql://valargen:valargen@postgres:5432/valargen

# Redis
REDIS_URL=redis://redis:6379

# Google OAuth (for Google authentication)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost/api/auth/google/callback

# UWM API (optional - set UWM_USE_REAL_API=0 to use mocks)
UWM_USE_REAL_API=0
UWM_CLIENT_ID=your-uwm-client-id
UWM_CLIENT_SECRET=your-uwm-client-secret
UWM_USERNAME=your-uwm-username
UWM_PASSWORD=your-uwm-password
UWM_SSO_URL=https://sso.uwm.com/adfs/oauth2/token
UWM_API_URL=https://stg.api.uwm.com/instantpricequote/v1/pricequote
UWM_ENVIRONMENT=staging
UWM_PROXY_URL=socks5://172.17.0.1:1080

# Environment
ENVIRONMENT=development
```

### 2. Fix Docker Networking with UFW (One-time Setup)

**CRITICAL:** If you're running Ubuntu/Debian with UFW firewall enabled, Docker containers won't be able to access external networks (Google OAuth, UWM API, etc.) without this fix.

Run the UFW fix script:

```bash
sudo ./scripts/fix_docker_ufw.sh
```

This script:
- Adds Docker network rules to UFW
- Sets UFW to allow forwarded/routed traffic
- Restarts Docker daemon

**Verify the fix:**

```bash
# Start containers
./scripts/start_local.sh

# Test external connectivity from container
docker exec valargen-server python -c "import urllib.request; urllib.request.urlopen('https://www.google.com', timeout=5); print('✓ Network working')"
```

### 3. Build Docker Images

Build local development images:

```bash
# Build server image
docker build -t valargen-local-server:latest ./app/server

# Build client image
docker build -t valargen-local-client:latest ./app/client
```

### 4. Start the Application

```bash
./scripts/start_local.sh
```

Wait for all services to be healthy. The script will show:
- Server: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Client: http://localhost

### 5. Seed Database (Optional)

```bash
# Seed customer data
docker exec valargen-server /app/.venv/bin/python scripts/seed_customers.py
```

## UWM API Access (Optional)

If you need to test with the real UWM API (`UWM_USE_REAL_API=1`), you need to set up a SOCKS5 proxy tunnel.

### Option 1: SSH Tunnel (Recommended)

Create SSH tunnel through staging server:

```bash
# Start tunnel (keep this terminal running)
ssh -D 1080 -N -C valargen-staging
```

The container will automatically use the proxy at `172.17.0.1:1080`.

### Option 2: Use Mock API

Set in `.env.local`:

```bash
UWM_USE_REAL_API=0
```

## Troubleshooting

### Google OAuth: "Unable to connect to Google OAuth service"

**Cause:** Docker containers can't access external networks due to UFW blocking forwarded traffic.

**Solution:** Run `sudo ./scripts/fix_docker_ufw.sh` and restart containers.

### Database: "pgbouncer cannot connect to server"

**Cause:** PgBouncer has DNS resolution issues with Docker's internal DNS.

**Solution:** Already fixed in `docker-compose.override.yml` - server connects directly to postgres.

### UWM OAuth: "Unable to connect to UWM OAuth service"

**Cause:** UWM requires proxy access in development mode.

**Solution:**
1. Start SSH tunnel: `ssh -D 1080 -N -C valargen-staging`
2. Or set `UWM_USE_REAL_API=0` to use mocks

### Network is unreachable from containers

**Check UFW status:**

```bash
sudo ufw status
```

If active, run the fix script:

```bash
sudo ./scripts/fix_docker_ufw.sh
docker compose restart
```

## Docker Compose Files

The project uses multiple compose files:

- `docker-compose.yml` - Base services (production-like)
- `docker-compose.override.yml` - Local development overrides
  - Connects directly to postgres (bypasses pgbouncer)
  - Exposes ports to host
  - Uses `.env.local` configuration

Docker Compose automatically merges these files when running `docker compose up`.

## Common Commands

```bash
# Start services
./scripts/start_local.sh

# Stop services
./scripts/stop_local.sh

# View logs
docker compose logs -f

# View server logs only
docker compose logs -f server

# Restart after config changes
docker compose restart server

# Rebuild after code changes
docker compose up -d --build server

# Access database
docker exec -it valargen-postgres psql -U valargen -d valargen

# Run tests
docker exec valargen-server /app/.venv/bin/pytest -v
```

## Architecture Notes

### Local Development vs Production

**Local Development:**
- Server connects directly to postgres (not pgbouncer)
  - Avoids pgbouncer DNS issues in Docker
- Uses `.env.local` for configuration
- Exposes ports to host machine
- Uses local Docker images

**Production/Staging:**
- Server connects through pgbouncer for connection pooling
- Direct network connectivity (no proxy needed for UWM)
- No exposed ports (Caddy reverse proxy)
- Uses environment-specific compose files

### Network Architecture

```
Host Machine (UFW Firewall)
├── Docker Bridge Network (172.20.0.0/16)
│   ├── valargen-postgres (172.20.0.2:5432)
│   ├── valargen-redis (172.20.0.4:6379)
│   ├── valargen-pgbouncer (172.20.0.5:6432)
│   ├── valargen-server (172.20.0.6:8000)
│   └── valargen-client (172.20.0.7:80)
│
└── SOCKS5 Proxy (optional, for UWM)
    └── localhost:1080 → valargen-staging → UWM API
```

## Files Modified from Original Setup

1. **docker-compose.override.yml**
   - Added `DATABASE_URL` override to bypass pgbouncer

2. **scripts/fix_docker_ufw.sh** (new)
   - UFW configuration for Docker networking

## Next Steps

After successful setup:

1. Access http://localhost to see the client
2. Try Google OAuth login
3. Check API docs at http://localhost:8000/docs
4. Run seed scripts to populate test data
5. Run tests to verify everything works

## Support

For issues, check:
1. Container logs: `docker compose logs -f`
2. Server health: `curl http://localhost:8000/health`
3. UFW status: `sudo ufw status verbose`
4. Docker network: `docker network inspect valargen-main_valargen-network`
