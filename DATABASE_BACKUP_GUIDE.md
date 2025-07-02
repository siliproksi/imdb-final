# Database Backup & Restore Guide

This guide explains how to backup and restore the IMDB Clone PostgreSQL database.

## 📁 Setup

The project includes:
- `export_db.sh` - Export/backup database script
- `import_db.sh` - Import/restore database script  
- `dumps/` - Directory for storing database dump files
- Docker volume mapping for seamless container access

## 🔧 Prerequisites

1. **Docker containers must be running:**
   ```bash
   docker compose up -d
   ```

2. **Scripts are executable** (already set up):
   ```bash
   chmod +x export_db.sh import_db.sh
   ```

## 📤 Export Database

To create a backup of your current database:

```bash
./export_db.sh
```

**What it does:**
- Creates timestamped dump file: `imdb_clone_backup_YYYYMMDD_HHMMSS.sql`
- Includes complete schema and all data
- Shows file size and lists available dumps
- Saves to `./dumps/` directory

**Example output:**
```
✅ Database export completed successfully!
📁 Dump file saved to: ./dumps/imdb_clone_backup_20231215_143022.sql
📊 File size: 215K
```

## 📥 Import Database

To restore from a backup:

```bash
./import_db.sh
```

**Interactive mode:**
- Shows list of available dump files
- Select by number (1, 2, 3, etc.)
- Confirms before proceeding
- **⚠️ WARNING: Completely replaces existing data!**

**Direct file mode:**
```bash
./import_db.sh filename.sql
```

**Example:**
```bash
./import_db.sh imdb_clone_backup_20231215_143022.sql
```

## 📋 Features

### Export Script Features:
- ✅ Automatic timestamping
- ✅ Container health check
- ✅ File size reporting
- ✅ Colorized output
- ✅ Error handling

### Import Script Features:
- ✅ Interactive file selection
- ✅ File validation
- ✅ Safety confirmations
- ✅ Database statistics after import
- ✅ Support for direct file specification

## 🗂️ File Structure

```
project/
├── export_db.sh           # Export script
├── import_db.sh           # Import script
├── dumps/                 # Dump files directory
│   ├── README.md          # Dumps directory info
│   └── *.sql             # Database dump files
└── docker-compose.yml    # Updated with dumps volume
```

## 🔄 Workflow Examples

### Daily Backup:
```bash
./export_db.sh
```

### Restore Production Data:
```bash
./import_db.sh production_backup.sql
```

### Reset to Clean State:
```bash
./import_db.sh clean_install_backup.sql
```

## ⚙️ Technical Details

### Docker Integration:
- Uses `docker exec` to run commands inside database container
- Volume mapping: `./dumps:/dumps` in docker-compose.yml
- Container name: `imdb_db`
- Database: `imdb_clone`
- User: `imdb_user`

### Database Info:
- **Tables**: users, movies, actors, ratings, watchlist, movie_actors
- **Relationships**: Full foreign key constraints
- **Indexes**: Optimized for queries
- **Data**: Complete user data, ratings, and movie information

## 🚨 Important Notes

1. **Data Loss Warning**: Import completely replaces existing database
2. **Container Dependency**: Requires running Docker containers
3. **File Permissions**: Scripts need execute permissions
4. **Disk Space**: Consider dump file sizes for large databases
5. **Backup Strategy**: Regular exports recommended for production

## 🎯 Quick Commands

```bash
# Export current database
./export_db.sh

# Import with file selection
./import_db.sh

# Import specific file
./import_db.sh backup_file.sql

# List available dumps
ls -la dumps/

# Check container status
docker ps | grep imdb_db
```