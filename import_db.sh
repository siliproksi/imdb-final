#!/bin/bash

# Database import script for IMDB Clone project
# This script imports a PostgreSQL dump file into the database

set -e

# Configuration
CONTAINER_NAME="imdb_db"
DB_NAME="imdb_clone"
DB_USER="imdb_user"
DUMP_DIR="./dumps"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Database Import Tool for IMDB Clone${NC}"
echo -e "${BLUE}======================================${NC}"

# Check if dumps directory exists
if [ ! -d "$DUMP_DIR" ]; then
    echo -e "${RED}Error: Dumps directory '$DUMP_DIR' does not exist!${NC}"
    echo -e "${YELLOW}Please create the dumps directory and add some dump files.${NC}"
    exit 1
fi

# Check if container is running
if ! docker ps | grep -q "$CONTAINER_NAME"; then
    echo -e "${RED}Error: Container $CONTAINER_NAME is not running!${NC}"
    echo -e "${YELLOW}Please start the containers with: docker compose up -d${NC}"
    exit 1
fi

# List available dump files
echo -e "${YELLOW}📋 Available dump files:${NC}"
DUMP_FILES=($(ls "$DUMP_DIR"/*.sql 2>/dev/null))

if [ ${#DUMP_FILES[@]} -eq 0 ]; then
    echo -e "${RED}No dump files found in $DUMP_DIR${NC}"
    echo -e "${YELLOW}Please add some .sql dump files to the dumps directory.${NC}"
    exit 1
fi

# Display files with numbers
for i in "${!DUMP_FILES[@]}"; do
    FILE_NAME=$(basename "${DUMP_FILES[$i]}")
    FILE_SIZE=$(ls -lh "${DUMP_FILES[$i]}" | awk '{print $5}')
    FILE_DATE=$(ls -l "${DUMP_FILES[$i]}" | awk '{print $6, $7, $8}')
    echo -e "${BLUE}[$((i+1))]${NC} $FILE_NAME ${YELLOW}($FILE_SIZE, $FILE_DATE)${NC}"
done

# If dump file is provided as argument, use it
if [ $# -eq 1 ]; then
    DUMP_FILE="$DUMP_DIR/$1"
    if [ ! -f "$DUMP_FILE" ]; then
        echo -e "${RED}Error: Dump file '$DUMP_FILE' not found!${NC}"
        exit 1
    fi
    echo -e "${GREEN}Using provided dump file: $1${NC}"
else
    # Prompt user to select a file
    echo ""
    read -p "$(echo -e ${YELLOW}"Enter the number of the dump file to import (1-${#DUMP_FILES[@]}): "${NC})" SELECTION

    # Validate selection
    if ! [[ "$SELECTION" =~ ^[0-9]+$ ]] || [ "$SELECTION" -lt 1 ] || [ "$SELECTION" -gt ${#DUMP_FILES[@]} ]; then
        echo -e "${RED}Invalid selection. Please enter a number between 1 and ${#DUMP_FILES[@]}.${NC}"
        exit 1
    fi

    # Get selected file
    DUMP_FILE="${DUMP_FILES[$((SELECTION-1))]}"
fi

DUMP_FILENAME=$(basename "$DUMP_FILE")
echo -e "${YELLOW}Selected file: $DUMP_FILENAME${NC}"

# Warning about data loss
echo ""
echo -e "${RED}⚠️  WARNING: This will completely replace the current database!${NC}"
echo -e "${RED}⚠️  All existing data will be lost!${NC}"
echo ""
read -p "$(echo -e ${YELLOW}"Are you sure you want to continue? (yes/no): "${NC})" CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${YELLOW}Import cancelled.${NC}"
    exit 0
fi

echo -e "${YELLOW}Starting database import...${NC}"

# Import database
echo -e "${YELLOW}📥 Importing $DUMP_FILENAME into database...${NC}"

# Copy dump file to container and import
docker exec -i "$CONTAINER_NAME" psql -U "$DB_USER" -d postgres < "$DUMP_FILE"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Database import completed successfully!${NC}"
    echo -e "${GREEN}📊 Imported from: $DUMP_FILENAME${NC}"
    
    # Show some basic stats
    echo -e "${YELLOW}📈 Database statistics:${NC}"
    docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "
        SELECT 
            'Users' as table_name, COUNT(*) as record_count 
        FROM users
        UNION ALL
        SELECT 
            'Movies' as table_name, COUNT(*) as record_count 
        FROM movies
        UNION ALL
        SELECT 
            'Ratings' as table_name, COUNT(*) as record_count 
        FROM ratings
        UNION ALL
        SELECT 
            'Actors' as table_name, COUNT(*) as record_count 
        FROM actors;
    "
else
    echo -e "${RED}❌ Database import failed!${NC}"
    exit 1
fi

echo -e "${GREEN}🎉 Import process completed!${NC}"