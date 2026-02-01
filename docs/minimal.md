# Minimal Setup Guide

## Prerequisites

| Requirement | Linux/Mac | Windows |
|-------------|-----------|---------|
| Docker | `curl -fsSL https://get.docker.com \| sudo sh` | [Docker Desktop](https://www.docker.com/products/docker-desktop/) |
| Git | `sudo apt install git` | `winget install Git.Git` |

**Windows additional:**
- PowerShell 5.1+ (included in Windows 10/11)
- OpenSSH Client (pre-installed on Windows 10/11, verify with `ssh -V`)

## Quick Start (Linux/Mac)

```bash
# 1. Start Docker services
./scripts/start_local.sh

# 2. Run migrations (create tables)
docker exec valargen-server .venv/bin/alembic upgrade head

# 3. Seed roles, permissions, admin user
docker exec valargen-server .venv/bin/python scripts/seed_data.py

# 4. Seed sample customers
docker exec valargen-server .venv/bin/python scripts/seed_customers.py
```

## Quick Start (Windows)

```powershell
# 0. Set execution policy (one-time)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 1. Start Docker services
.\scripts\start_local.ps1

# 2. Run migrations (create tables)
docker exec valargen-server .venv/bin/alembic upgrade head

# 3. Seed roles, permissions, admin user
docker exec valargen-server .venv/bin/python scripts/seed_data.py

# 4. Seed sample customers
docker exec valargen-server .venv/bin/python scripts/seed_customers.py
```

### Windows Options
```powershell
.\scripts\start_local.ps1 -Fresh    # Full rebuild
.\scripts\start_local.ps1 -Client   # Refresh frontend deps
.\scripts\start_local.ps1 -Help     # Show help
```

## Login Credentials

| Field    | Value                |
|----------|----------------------|
| Email    | admin@valargen.com   |
| Password | Admin123             |

## URLs

| Service   | URL                         |
|-----------|-----------------------------|
| Client    | http://localhost:5173       |
| API       | http://localhost:8000       |
| API Docs  | http://localhost:8000/docs  |

## Database (DBeaver)

| Setting  | Value      |
|----------|------------|
| Host     | localhost  |
| Port     | 5432       |
| Database | valargen   |
| Username | valargen   |
| Password | valargen   |

## SSH Tunnel (for Staging API Access)

**Linux/Mac:**
```bash
./scripts/tunnel.sh
```

**Windows:**
```powershell
.\scripts\tunnel.ps1
```

**If issues, reset and try again:**
```bash
./scripts/tunnel.sh reset    # Linux/Mac
.\scripts\tunnel.ps1 reset   # Windows
```

## Stop Services

```bash
./scripts/stop_local.sh      # Linux/Mac
.\scripts\stop_local.ps1     # Windows
```

## Reset Everything

```bash
# Remove all containers and data
docker compose down -v --remove-orphans

# Reset SSH tunnel (removes keys and config)
./scripts/tunnel.sh reset    # Linux/Mac
.\scripts\tunnel.ps1 reset   # Windows

# Then run Quick Start steps again
```
