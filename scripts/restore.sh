#!/bin/bash
# Restore Valargen staging database from backup
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$PROJECT_DIR/backups"

cd "$PROJECT_DIR"

if [ -z "$1" ]; then
    echo "Usage: ./scripts/restore.sh <backup_file>"
    echo ""
    echo "Available backups:"
    ls -lh "$BACKUP_DIR"/*.dump 2>/dev/null || echo "No backups found"
    exit 1
fi

BACKUP_FILE="$1"

# Check if file exists (with or without path)
if [ -f "$BACKUP_FILE" ]; then
    BACKUP_PATH="$BACKUP_FILE"
elif [ -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
    BACKUP_PATH="$BACKUP_DIR/$BACKUP_FILE"
else
    echo "ERROR: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "=== Valargen Database Restore ==="
echo "Backup: $BACKUP_PATH"
echo ""
echo "WARNING: This will OVERWRITE the current database!"
read -p "Are you sure? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

# Load environment
if [ -f ".env.staging" ]; then
    export $(grep -v '^#' .env.staging | xargs)
fi

echo ""
echo "Restoring database..."

# Drop and recreate database
docker compose -f docker-compose.yml -f docker-compose.staging.yml exec -T postgres \
    psql -U valargen -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'valargen' AND pid <> pg_backend_pid();" postgres

docker compose -f docker-compose.yml -f docker-compose.staging.yml exec -T postgres \
    dropdb -U valargen --if-exists valargen

docker compose -f docker-compose.yml -f docker-compose.staging.yml exec -T postgres \
    createdb -U valargen valargen

# Restore from backup
cat "$BACKUP_PATH" | docker compose -f docker-compose.yml -f docker-compose.staging.yml exec -T postgres \
    pg_restore -U valargen -d valargen --no-owner --no-privileges

echo ""
echo "=== Restore Complete ==="
echo ""
echo "Restart the application: ./scripts/stop_staging.sh && ./scripts/start_staging.sh"
