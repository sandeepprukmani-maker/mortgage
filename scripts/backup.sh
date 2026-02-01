#!/bin/bash
# Backup Valargen staging database
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$PROJECT_DIR/backups"

cd "$PROJECT_DIR"

# Load environment
if [ -f ".env.staging" ]; then
    export $(grep -v '^#' .env.staging | xargs)
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="valargen_${TIMESTAMP}.dump"
RETENTION_DAYS=${BACKUP_RETENTION_DAYS:-30}

echo "=== Valargen Database Backup ==="
echo "Timestamp: $TIMESTAMP"
echo ""

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# PostgreSQL backup
echo "Backing up PostgreSQL..."
docker compose -f docker-compose.yml -f docker-compose.staging.yml exec -T postgres \
    pg_dump -U valargen -Fc valargen > "$BACKUP_DIR/$BACKUP_FILE"

BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
echo "Created: $BACKUP_DIR/$BACKUP_FILE ($BACKUP_SIZE)"

# Redis backup (RDB snapshot)
echo ""
echo "Triggering Redis snapshot..."
docker compose -f docker-compose.yml -f docker-compose.staging.yml exec -T redis \
    redis-cli BGSAVE

# Cleanup old backups
echo ""
echo "Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "valargen_*.dump" -mtime +$RETENTION_DAYS -delete 2>/dev/null || true

# List current backups
echo ""
echo "=== Current Backups ==="
ls -lh "$BACKUP_DIR"/*.dump 2>/dev/null || echo "No backups found"

echo ""
echo "=== Backup Complete ==="
echo ""
echo "To restore: ./scripts/restore.sh $BACKUP_FILE"
