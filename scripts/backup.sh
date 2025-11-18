### File: scripts/backup.sh

#!/bin/bash

# STEP: Database Backup Script
# Creates timestamped backups of PostgreSQL database

set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/astraeum_backup_$TIMESTAMP.sql"

mkdir -p $BACKUP_DIR

echo "Creating database backup..."
docker exec astraeum-postgres pg_dump -U astraeum astraeum_game > $BACKUP_FILE

gzip $BACKUP_FILE

echo "Backup created: $BACKUP_FILE.gz"

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete

echo "Old backups cleaned up"