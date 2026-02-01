# Valargen

Vue 3 + FastAPI + PostgreSQL application with Docker Compose.

## First-Time Setup

### 1. Install Docker (if not installed)

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker --version
```

### 2. Clone & Setup

```bash
git clone https://dev.azure.com/vivantify-devops/valargen-main/_git/valargen-main
cd valargen-main
cp app/server/.env.sample app/server/.env.local
```

### 3. Setup SSH Tunnel (for UWM API)

```bash
./scripts/tunnel.sh setup
```
This will generate SSH key and configure access. Share the public key with admin.

### 4. Start Services

```bash
./scripts/start_local.sh
```

### Daily Workflow

**Terminal 1:** Start tunnel
```bash
./scripts/tunnel.sh
```

**Terminal 2:** Start app
```bash
./scripts/start_local.sh
```

### URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

## Commands

```bash
# Start/Stop
./scripts/start_local.sh      # Start all services
./scripts/stop_local.sh       # Stop all services
./scripts/tunnel.sh           # Start SSH tunnel
./scripts/tunnel.sh kill      # Stop tunnel

# Logs
docker compose logs -f        # All logs
docker compose logs -f server # Server only

# Database
docker exec -it valargen-postgres psql -U valargen -d valargen

# Tests
docker exec valargen-server /app/.venv/bin/pytest -v
```

## Project Structure

```
app/
├── server/          # FastAPI backend
└── client/          # Vue 3 frontend

scripts/
├── start_local.sh   # Start local env
├── stop_local.sh    # Stop local env
└── tunnel.sh        # SSH tunnel management

docker-compose.yml            # Base config
docker-compose.override.yml   # Local overrides
docker-compose.staging.yml    # Staging config
```

## Troubleshooting

**Containers not starting:**
```bash
docker compose logs -f
./scripts/stop_local.sh && ./scripts/start_local.sh
```

**Port conflicts:**
```bash
sudo lsof -i :80 -i :8000 -i :5432
```

**Tunnel not connecting:**
```bash
./scripts/tunnel.sh status
./scripts/tunnel.sh reset && ./scripts/tunnel.sh setup
```

**UFW blocking Docker (Linux):**
```bash
sudo ./scripts/fix_docker_ufw.sh
```

## License

Copyright © 2025 Vivantify Technology Solutions India Pvt Ltd. All rights reserved.
