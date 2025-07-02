# IMDB Clone

A full-stack movie database application with Vue.js frontend and FastAPI backend, deployed with Docker and automatic HTTPS.

## Features

- **Movie Database**: Browse and search movies with detailed information
- **User Authentication**: Register/login with email or Google OAuth
- **Ratings & Reviews**: Rate movies and write reviews with country-based statistics
- **Watchlist**: Save movies to watch later
- **Search**: Search movies by title, summary, or actors
- **Multi-language**: Support for English and Turkish content

## Tech Stack

**Frontend**: Vue.js 3, Vue Router, Vuex, Axios  
**Backend**: FastAPI, SQLAlchemy, PostgreSQL, JWT Authentication  
**Deployment**: Docker, nginx-proxy, Let's Encrypt SSL

## Quick Start

```bash
# Start all services with HTTPS
./up.sh

# Stop services
./down.sh
```

**Live URLs**:
- Frontend: https://imdbfinal.codeise.com
- Backend API: https://imdbfinalb.codeise.com

## Database Management

```bash
# Import database backup
./import_db.sh

# Export database backup  
./export_db.sh
```

## Key API Endpoints

- `GET /movies?lang=en|tr` - Get movies (with language support)
- `GET /movies/{id}?lang=en|tr` - Get movie details
- `GET /search?q={query}&lang=en|tr` - Search movies/actors
- `POST /register` - Register user
- `POST /login` - Login user
- `POST /auth/google` - Google OAuth
- `POST /movies/{id}/rate` - Rate movie
- `POST /watchlist/{movie_id}` - Add to watchlist

## Configuration

Backend environment variables in `docker-compose.yml`:
- `DATABASE_URL` - PostgreSQL connection
- `GOOGLE_CLIENT_ID/SECRET` - Google OAuth credentials
- `VIRTUAL_HOST/LETSENCRYPT_HOST` - Domain configuration

Frontend automatically uses `https://imdbfinalb.codeise.com` as API base URL.

## Architecture

```
├── frontend/          # Vue.js app
├── backend/           # FastAPI app  
├── docker-compose.yml # All services + SSL proxy
├── up.sh / down.sh    # Management scripts
└── dumps/             # Database backups
```

The app uses nginx-proxy with Let's Encrypt for automatic HTTPS certificates and domain routing.