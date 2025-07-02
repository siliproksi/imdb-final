# Database Dumps Directory

This directory contains PostgreSQL database dump files for the IMDB Clone project.

## Usage

### Export Database
To create a backup of the current database:
```bash
./export_db.sh
```

This will create a timestamped dump file in this directory.

### Import Database
To restore a database from a dump file:
```bash
./import_db.sh
```

This will show you a list of available dump files to choose from.

You can also specify a dump file directly:
```bash
./import_db.sh filename.sql
```

## File Naming Convention

Export files are automatically named with timestamps:
- Format: `imdb_clone_backup_YYYYMMDD_HHMMSS.sql`
- Example: `imdb_clone_backup_20231215_143022.sql`

## Notes

- Make sure Docker containers are running before using the scripts
- Import will completely replace the existing database
- Export files include schema and data
- Files are stored with `.sql` extension