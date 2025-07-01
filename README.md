# IMDB Clone - Slimmed Down Movie Database

A modern web application built with Vue.js frontend, FastAPI backend, and PostgreSQL database, all containerized with Docker.

## Features

### 🎬 Core Functionality
- **Movie Database**: Browse a collection of popular movies with ratings, summaries, and trailers
- **Search System**: 
  - Generic search across movies, summaries, and actors
  - Dropdown search filters (movies, actors, all)
  - Real-time autocomplete (shows top 3 results after 3+ characters)
- **Movie Details**: Individual movie pages with ratings, comments, popularity metrics, and cast information

### 👤 User Management
- **Authentication**: Email/password login with secure password hashing
- **Registration**: Email, password (8+ chars, 1 number, 1 special char), country, city
- **Profile Photos**: Optional photo upload during registration
- **Google OAuth**: Ready for Google authentication integration

### 🌐 Internationalization
- **Multi-language Support**: English/Turkish support for home page
- **Browser Detection**: Automatically detects browser language (defaults to English)
- **Language Toggle**: Easy switching between EN/TR in header

### 📝 User Features (Authenticated)
- **Watchlist**: Add/remove movies from personal watchlist
- **Rating System**: Rate movies (1-10 scale) with optional comments
- **User Dashboard**: View personal watchlist and ratings

### 📊 Advanced Features
- **Popularity Algorithm**: Custom business logic combining ratings, views, and comments
- **Rating Distribution**: Visual representation of ratings by country
- **Movie Statistics**: View count, average rating, popularity ranking

## Tech Stack

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vue Router** - Client-side routing
- **Vuex** - State management
- **Vue I18n** - Internationalization
- **Axios** - HTTP client
- **Lodash** - Utility library

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation
- **JWT** - JSON Web Tokens for authentication
- **Bcrypt** - Password hashing

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd se335_final
   ```

2. **Start the application**
   ```bash
   npm run dev
   ```
   This will start all services:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - PostgreSQL: localhost:5433 (mapped to avoid conflicts)

3. **Access the application**
   - Open your browser and navigate to `http://localhost:3000`
   - The database will be automatically seeded with sample movies

## Development

### Project Structure
```
se335_final/
├── frontend/                # Vue.js application
│   ├── src/
│   │   ├── components/     # Reusable Vue components
│   │   ├── views/          # Page components
│   │   ├── router/         # Vue Router configuration
│   │   ├── store/          # Vuex store
│   │   └── services/       # API services
│   ├── public/             # Static assets
│   └── Dockerfile
├── backend/                # FastAPI application
│   ├── main.py            # FastAPI app entry point
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # Database operations
│   ├── auth.py            # Authentication logic
│   ├── database.py        # Database configuration
│   ├── seed_data.py       # Sample data seeding
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile
├── docker-compose.yml     # Multi-container setup
└── README.md
```

### Environment Variables

The application uses the following environment variables (set in docker-compose.yml):

**Backend:**
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `GOOGLE_CLIENT_ID`: Google OAuth client ID (optional)
- `GOOGLE_CLIENT_SECRET`: Google OAuth secret (optional)

**Frontend:**
- `VUE_APP_API_URL`: Backend API URL

### API Endpoints

**Authentication:**
- `POST /register` - User registration
- `POST /login` - User login
- `POST /upload-photo` - Profile photo upload

**Movies:**
- `GET /movies` - Get paginated movies list
- `GET /movies/{id}` - Get movie details
- `GET /search` - Search movies and actors
- `POST /movies/{id}/rate` - Rate a movie
- `POST /movies/{id}/watchlist` - Add to watchlist

**User:**
- `GET /me/watchlist` - Get user's watchlist

### Database Schema

**Users Table:**
- id, email, hashed_password, country, city, photo_url, is_active, created_at

**Movies Table:**
- id, title, summary, release_year, duration, image_url, trailer_url, imdb_score, popularity_score, view_count

**Actors Table:**
- id, name, bio, birth_date, photo_url

**Ratings Table:**
- id, user_id, movie_id, rating, comment, created_at

**Watchlist Table:**
- id, user_id, movie_id, added_at

**MovieActor Table:**
- id, movie_id, actor_id, character_name

## Features Implementation

### Password Security
- Minimum 8 characters
- At least 1 number
- At least 1 non-alphanumeric character
- Bcrypt hashing with salt

### Search Functionality
- Full-text search across movie titles and summaries
- Actor name search
- Dropdown filter options
- 3-character minimum for autocomplete
- Maximum 3 results for autocomplete

### Popularity Algorithm
The popularity score is calculated using:
- Average rating (weighted 10x, max 100 points)
- Number of ratings (2 points each, max 50 points)
- View count (0.1 points each, max 30 points)
- Base recency score (10 points)

### Rating System
- 1-10 scale with decimal support
- Optional text comments
- One rating per user per movie (updates existing)
- Display average rating and total count

## Production Considerations

### Security
- Environment variables for sensitive data
- JWT token expiration
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy ORM
- CORS configuration

### Performance
- Database indexing on frequently queried fields
- Pagination for large datasets
- Image optimization recommendations
- Caching strategies for popular content

### Deployment
- Docker containers for easy deployment
- Environment-specific configurations
- Database migrations with Alembic
- Static file serving optimization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes and follows standard software development practices for a modern web application.