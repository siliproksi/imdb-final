from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_, desc
from fastapi import HTTPException
import models
import schemas
import auth

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        country=user.country,
        city=user.city,
        photo_url=user.photo  # Store base64 photo data in photo_url field
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_google_user(db: Session, user_info: dict):
    """Create a new user from Google OAuth info"""
    db_user = models.User(
        email=user_info['email'],
        google_id=user_info['google_id'],
        photo_url=user_info.get('picture', ''),
        hashed_password=None  # No password for Google users
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_movies(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Movie).order_by(desc(models.Movie.popularity_score)).offset(skip).limit(limit).all()

def get_movie(db: Session, movie_id: int):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if movie:
        # Increment view count
        movie.view_count += 1
        db.commit()
        
        # Calculate average rating
        avg_rating = db.query(func.avg(models.Rating.rating)).filter(models.Rating.movie_id == movie_id).scalar()
        total_ratings = db.query(func.count(models.Rating.id)).filter(models.Rating.movie_id == movie_id).scalar()
        
        # Update popularity score based on ratings, views, and other factors
        popularity = calculate_popularity(movie, avg_rating, total_ratings)
        movie.popularity_score = popularity
        db.commit()
        
        # Add calculated fields
        movie.average_rating = avg_rating
        movie.total_ratings = total_ratings
    
    return movie

def search_movies(db: Session, query: str, search_type: str = "all", limit: int = 10):
    movies = []
    actors = []
    
    if search_type in ["all", "movies"]:
        # Match any word that starts with the query
        movies = db.query(models.Movie).filter(
            models.Movie.title.ilike(f"%{query}%")
        ).filter(
            # Ensure the query appears as a consecutive substring (not scattered letters)
            models.Movie.title.ilike(f"% {query}%") |  # " ave" - word starting with query
            models.Movie.title.ilike(f"{query}%")      # "ave" - title starting with query
        ).limit(limit).all()
    
    if search_type in ["all", "actors"]:
        actors = db.query(models.Actor).filter(
            models.Actor.name.ilike(f"%{query}%")
        ).filter(
            # Ensure the query appears as a consecutive substring (not scattered letters)
            models.Actor.name.ilike(f"% {query}%") |  # " ave" - word starting with query
            models.Actor.name.ilike(f"{query}%")      # "ave" - name starting with query
        ).limit(limit).all()
    
    return {"movies": movies, "actors": actors}

def create_rating(db: Session, rating: schemas.RatingCreate, movie_id: int, user_id: int):
    # Check if user already rated this movie
    existing_rating = db.query(models.Rating).filter(
        models.Rating.user_id == user_id,
        models.Rating.movie_id == movie_id
    ).first()
    
    if existing_rating:
        # Update existing rating
        existing_rating.rating = rating.rating
        existing_rating.comment = rating.comment
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    else:
        # Create new rating
        db_rating = models.Rating(
            user_id=user_id,
            movie_id=movie_id,
            rating=rating.rating,
            comment=rating.comment
        )
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating

def add_to_watchlist(db: Session, movie_id: int, user_id: int):
    # Check if movie exists
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Check if already in watchlist
    existing = db.query(models.Watchlist).filter(
        models.Watchlist.user_id == user_id,
        models.Watchlist.movie_id == movie_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Movie already in your watchlist")
    
    db_watchlist = models.Watchlist(user_id=user_id, movie_id=movie_id)
    db.add(db_watchlist)
    db.commit()
    db.refresh(db_watchlist)
    return {"message": "Added to watchlist"}

def get_user_watchlist(db: Session, user_id: int):
    return db.query(models.Watchlist).options(
        joinedload(models.Watchlist.movie)
    ).filter(models.Watchlist.user_id == user_id).all()

def remove_from_watchlist(db: Session, watchlist_id: int, user_id: int):
    """Remove item from user's watchlist"""
    watchlist_item = db.query(models.Watchlist).filter(
        models.Watchlist.id == watchlist_id,
        models.Watchlist.user_id == user_id
    ).first()
    
    if not watchlist_item:
        raise HTTPException(status_code=404, detail="Item not found in your watchlist")
    
    db.delete(watchlist_item)
    db.commit()
    return {"message": "Removed from watchlist"}

def calculate_popularity(movie, avg_rating, total_ratings):
    # Business logic for popularity calculation
    # Factors: average rating, number of ratings, view count, recency
    
    rating_score = (avg_rating or 0) * 10  # Scale to 100
    rating_count_score = min(total_ratings * 2, 50)  # Max 50 points for ratings count
    view_score = min(movie.view_count * 0.1, 30)  # Max 30 points for views
    recency_score = 10  # Base score for all movies
    
    return rating_score + rating_count_score + view_score + recency_score

def seed_sample_movies(db: Session):
    # Create sample movies if none exist
    if db.query(models.Movie).count() == 0:
        sample_movies = [
            {
                "title": "The Shawshank Redemption",
                "summary": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                "release_year": 1994,
                "duration": 142,
                "imdb_score": 9.3,
                "image_url": "https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=6hB3S9bIaco"
            },
            {
                "title": "The Godfather",
                "summary": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                "release_year": 1972,
                "duration": 175,
                "imdb_score": 9.2,
                "image_url": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg",
                "trailer_url": "https://www.youtube.com/watch?v=sY1S34973zA"
            }
        ]
        
        for movie_data in sample_movies:
            db_movie = models.Movie(**movie_data)
            db.add(db_movie)
        
        db.commit()