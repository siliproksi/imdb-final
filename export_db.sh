#!/bin/bash

# Database export script for IMDB Clone project
# This script exports the PostgreSQL database to a dump file

set -e

# Configuration
CONTAINER_NAME="imdb_db"
DB_NAME="imdb_clone"
DB_USER="imdb_user"
DUMP_DIR="./dumps"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DUMP_FILE="imdb_clone_backup_${TIMESTAMP}.sql"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting database export...${NC}"

# Check if dumps directory exists, create if not
if [ ! -d "$DUMP_DIR" ]; then
    echo -e "${YELLOW}Creating dumps directory...${NC}"
    mkdir -p "$DUMP_DIR"
fi

# Check if container is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo -e "${RED}Error: Container $CONTAINER_NAME is not running!${NC}"
    echo -e "${YELLOW}Please start the containers with: docker compose up -d${NC}"
    exit 1
fi

echo -e "${YELLOW}Exporting database to: $DUMP_DIR/$DUMP_FILE${NC}"

# Export database
docker exec "$CONTAINER_NAME" pg_dump -U "$DB_USER" -d "$DB_NAME" --verbose --clean --if-exists --create > "$DUMP_DIR/$DUMP_FILE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Database export completed successfully!${NC}"
    echo -e "${GREEN}📁 Dump file saved to: $DUMP_DIR/$DUMP_FILE${NC}"
    
    # Show file size
    FILE_SIZE=$(ls -lh "$DUMP_DIR/$DUMP_FILE" | awk '{print $5}')
    echo -e "${GREEN}📊 File size: $FILE_SIZE${NC}"
    
    # List all dump files
    echo -e "${YELLOW}📋 Available dump files:${NC}"
    ls -la "$DUMP_DIR"/*.sql 2>/dev/null || echo "No previous dump files found"
else
    echo -e "${RED}❌ Database export failed!${NC}"
    exit 1
fi

echo -e "${GREEN}🎉 Export process completed!${NC}"