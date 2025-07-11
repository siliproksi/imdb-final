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

def get_movies(db: Session, skip: int = 0, limit: int = 20, lang: str = "en"):
    movies = db.query(models.Movie).order_by(desc(models.Movie.popularity_score)).offset(skip).limit(limit).all()
    
    # Create response with appropriate language without modifying database objects
    result = []
    for movie in movies:
        movie_dict = {
            "id": movie.id,
            "title": movie.title_tr if (lang == "tr" and movie.title_tr) else movie.title,
            "summary": movie.summary_tr if (lang == "tr" and movie.summary_tr) else movie.summary,
            "release_year": movie.release_year,
            "duration": movie.duration,
            "image_url": movie.image_url,
            "trailer_url": movie.trailer_url,
            "imdb_score": movie.imdb_score,
            "popularity_score": movie.popularity_score,
            "view_count": movie.view_count,
            "created_at": movie.created_at
        }
        result.append(movie_dict)
    
    return result

def get_actor(db: Session, actor_id: int):
    actor = db.query(models.Actor).options(
        joinedload(models.Actor.movies).joinedload(models.MovieActor.movie)
    ).filter(models.Actor.id == actor_id).first()
    return actor

def get_movie(db: Session, movie_id: int, lang: str = "en"):
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
        
        # Create response with appropriate language without modifying database object
        movie_dict = {
            "id": movie.id,
            "title": movie.title_tr if (lang == "tr" and movie.title_tr) else movie.title,
            "summary": movie.summary_tr if (lang == "tr" and movie.summary_tr) else movie.summary,
            "release_year": movie.release_year,
            "duration": movie.duration,
            "image_url": movie.image_url,
            "trailer_url": movie.trailer_url,
            "imdb_score": movie.imdb_score,
            "popularity_score": movie.popularity_score,
            "view_count": movie.view_count,
            "created_at": movie.created_at,
            "average_rating": avg_rating,
            "total_ratings": total_ratings
        }
        return movie_dict
    
    return None

def search_movies(db: Session, query: str, search_type: str = "all", limit: int = 10, lang: str = "en"):
    movies = []
    actors = []
    
    if search_type in ["all", "movies"]:
        if lang == "tr":
            # Search Turkish fields: title matches first, then fill with summary matches
            # First get title matches (up to 3)
            title_matches = db.query(models.Movie).filter(
                models.Movie.title_tr.ilike(f"%{query}%")
            ).limit(3).all()
            
            # If we have less than 3 title matches, fill remaining with summary matches
            if len(title_matches) < 3:
                title_match_ids = [movie.id for movie in title_matches]
                remaining_limit = 3 - len(title_matches)
                
                summary_matches = db.query(models.Movie).filter(
                    models.Movie.summary_tr.ilike(f"%{query}%"),
                    ~models.Movie.id.in_(title_match_ids) if title_match_ids else True
                ).limit(remaining_limit).all()
                
                movies = title_matches + summary_matches
            else:
                movies = title_matches
            
            # Convert to response format with Turkish content
            movie_results = []
            for movie in movies:
                movie_dict = {
                    "id": movie.id,
                    "title": movie.title_tr if movie.title_tr else movie.title,
                    "summary": movie.summary_tr if movie.summary_tr else movie.summary,
                    "release_year": movie.release_year,
                    "duration": movie.duration,
                    "image_url": movie.image_url,
                    "trailer_url": movie.trailer_url,
                    "imdb_score": movie.imdb_score,
                    "popularity_score": movie.popularity_score,
                    "view_count": movie.view_count,
                    "created_at": movie.created_at
                }
                movie_results.append(movie_dict)
            movies = movie_results
        else:
            # Search English fields: title matches first, then fill with summary matches
            # First get title matches (up to 3)
            title_matches = db.query(models.Movie).filter(
                models.Movie.title.ilike(f"%{query}%")
            ).limit(3).all()
            
            # If we have less than 3 title matches, fill remaining with summary matches
            if len(title_matches) < 3:
                title_match_ids = [movie.id for movie in title_matches]
                remaining_limit = 3 - len(title_matches)
                
                summary_matches = db.query(models.Movie).filter(
                    models.Movie.summary.ilike(f"%{query}%"),
                    ~models.Movie.id.in_(title_match_ids) if title_match_ids else True
                ).limit(remaining_limit).all()
                
                movies = title_matches + summary_matches
            else:
                movies = title_matches
            
            # Convert to response format
            movie_results = []
            for movie in movies:
                movie_dict = {
                    "id": movie.id,
                    "title": movie.title,
                    "summary": movie.summary,
                    "release_year": movie.release_year,
                    "duration": movie.duration,
                    "image_url": movie.image_url,
                    "trailer_url": movie.trailer_url,
                    "imdb_score": movie.imdb_score,
                    "popularity_score": movie.popularity_score,
                    "view_count": movie.view_count,
                    "created_at": movie.created_at
                }
                movie_results.append(movie_dict)
            movies = movie_results
    
    if search_type in ["all", "actors"]:
        actors = db.query(models.Actor).filter(
            models.Actor.name.ilike(f"%{query}%")
        ).limit(3).all()  # Top 3 results only
    
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

def get_movie_rating_stats(db: Session, movie_id: int, country: str = None):
    """Get rating statistics for a movie including rating distribution histogram"""
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        return None
    
    # Base query for ratings with user info
    ratings_query = db.query(models.Rating).options(
        joinedload(models.Rating.user)
    ).filter(models.Rating.movie_id == movie_id)
    
    # Filter by country if specified
    if country and country != "All":
        ratings_query = ratings_query.join(models.User).filter(models.User.country == country)
    
    ratings = ratings_query.order_by(desc(models.Rating.created_at)).all()
    
    # Calculate rating distribution (1-10 stars)
    rating_distribution = {}
    total_ratings = len(ratings)
    
    # Initialize all ratings 1-10 with 0 count
    for i in range(1, 11):
        rating_distribution[i] = 0
    
    # Count ratings
    for rating in ratings:
        rating_value = int(round(rating.rating))  # Round to nearest integer
        if rating_value in rating_distribution:
            rating_distribution[rating_value] += 1
    
    # Convert to percentage and format for frontend
    distribution_data = []
    for rating_val in range(1, 11):
        count = rating_distribution[rating_val]
        percentage = (count / total_ratings * 100) if total_ratings > 0 else 0
        distribution_data.append({
            "rating": rating_val,
            "count": count,
            "percentage": round(percentage, 1)
        })
    
    # Get available countries
    countries = db.query(models.User.country).join(models.Rating).filter(
        models.Rating.movie_id == movie_id,
        models.User.country.isnot(None)
    ).distinct().order_by(models.User.country).all()
    
    country_list = ["All"] + [country[0] for country in countries]
    
    return {
        "total_ratings": total_ratings,
        "rating_distribution": distribution_data,
        "available_countries": country_list,
        "selected_country": country or "All",
        "ratings": ratings
    }

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