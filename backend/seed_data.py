from sqlalchemy.orm import Session
from database import SessionLocal
import models

def seed_movies():
    db = SessionLocal()
    
    # Check if movies already exist
    if db.query(models.Movie).count() > 0:
        print("Movies already exist, skipping seed")
        db.close()
        return
    
    sample_movies = [
        {
            "title": "The Shawshank Redemption",
            "summary": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
            "release_year": 1994,
            "duration": 142,
            "imdb_score": 9.3,
            "popularity_score": 95.0,
            "image_url": "https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
            "trailer_url": "https://www.youtube.com/watch?v=6hB3S9bIaco"
        },
        {
            "title": "The Godfather",
            "summary": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
            "release_year": 1972,
            "duration": 175,
            "imdb_score": 9.2,
            "popularity_score": 92.0,
            "image_url": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
            "trailer_url": "https://www.youtube.com/watch?v=sY1S34973zA"
        },
        {
            "title": "The Dark Knight",
            "summary": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.",
            "release_year": 2008,
            "duration": 152,
            "imdb_score": 9.0,
            "popularity_score": 94.0,
            "image_url": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg",
            "trailer_url": "https://www.youtube.com/watch?v=EXeTwQWrcwY"
        },
        {
            "title": "Pulp Fiction",
            "summary": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
            "release_year": 1994,
            "duration": 154,
            "imdb_score": 8.9,
            "popularity_score": 89.0,
            "image_url": "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
            "trailer_url": "https://www.youtube.com/watch?v=s7EdQ4FqbhY"
        },
        {
            "title": "Forrest Gump",
            "summary": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man.",
            "release_year": 1994,
            "duration": 142,
            "imdb_score": 8.8,
            "popularity_score": 91.0,
            "image_url": "https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMzXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
            "trailer_url": "https://www.youtube.com/watch?v=bLvqoHBptjg"
        },
        {
            "title": "Inception",
            "summary": "A thief who enters the dreams of others to steal secrets from their minds gets the chance to have his crimes forgiven in exchange for an impossible task.",
            "release_year": 2010,
            "duration": 148,
            "imdb_score": 8.8,
            "popularity_score": 93.0,
            "image_url": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg",
            "trailer_url": "https://www.youtube.com/watch?v=YoHD9XEInc0"
        },
        {
            "title": "The Matrix",
            "summary": "A computer programmer discovers reality isn't what it seems when mysterious rebels reveal the world is an elaborate deception.",
            "release_year": 1999,
            "duration": 136,
            "imdb_score": 8.7,
            "popularity_score": 90.0,
            "image_url": "https://m.media-amazon.com/images/M/MV5BNzQzOTk3OTAtNDQ0Zi00ZTVkLWI0MTEtMDllZjNkYzNjNTc4L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg",
            "trailer_url": "https://www.youtube.com/watch?v=vKQi3bBA1y8"
        },
        {
            "title": "Goodfellas",
            "summary": "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners.",
            "release_year": 1990,
            "duration": 146,
            "imdb_score": 8.7,
            "popularity_score": 86.0,
            "image_url": "https://m.media-amazon.com/images/M/MV5BY2NkZjEzMDgtN2RjYy00YzM1LWI4ZmQtMjA4YTQyYzZlMjg1XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
            "trailer_url": "https://www.youtube.com/watch?v=qo5jJpHtI0E"
        },
        {
            "title": "The Lord of the Rings: The Return of the King",
            "summary": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
            "release_year": 2003,
            "duration": 201,
            "imdb_score": 8.9,
            "popularity_score": 88.0,
            "image_url": "https://m.media-amazon.com/images/M/MV5BNzA5ZDNlZWMtM2NhNS00NDJjLTk4NDItYTRmY2EwMWI5MTktXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
            "trailer_url": "https://www.youtube.com/watch?v=r5X-hFf6Bwo"
        },
        {
            "title": "Fight Club",
            "summary": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into an underground anarchist organization.",
            "release_year": 1999,
            "duration": 139,
            "imdb_score": 8.8,
            "popularity_score": 87.0,
            "image_url": "https://m.media-amazon.com/images/M/MV5BMmEzNTkxYjQtZTc0MC00YTVjLTg5ZTEtZWMwOWVlYzY0NWIwXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
            "trailer_url": "https://www.youtube.com/watch?v=qtRKdVHc-cE"
        },
        {
            "title": "Interstellar",
            "summary": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
            "release_year": 2014,
            "duration": 169,
            "imdb_score": 8.6,
            "popularity_score": 92.0,
            "image_url": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
            "trailer_url": "https://www.youtube.com/watch?v=zSWdZVtXT7E"
        },
        {
            "title": "The Avengers",
            "summary": "Earth's mightiest heroes must come together and learn to fight as a team if they are going to stop the mischievous Loki and his alien army from enslaving humanity.",
            "release_year": 2012,
            "duration": 143,
            "imdb_score": 8.0,
            "popularity_score": 95.0,
            "image_url": "https://m.media-amazon.com/images/M/MV5BNDYxNjQyMjAtNTdiOS00NGYwLWFmNTAtNThmYjU5ZGI2YTI1XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
            "trailer_url": "https://www.youtube.com/watch?v=eOrNdBpGMv8"
        }
    ]
    
    # Add sample actors
    sample_actors = [
        {"name": "Morgan Freeman", "bio": "American actor and film narrator"},
        {"name": "Tim Robbins", "bio": "American actor and filmmaker"},
        {"name": "Marlon Brando", "bio": "American actor and film director"},
        {"name": "Al Pacino", "bio": "American actor and filmmaker"},
        {"name": "Christian Bale", "bio": "English actor"},
        {"name": "Heath Ledger", "bio": "Australian actor and music video director"},
        {"name": "John Travolta", "bio": "American actor and singer"},
        {"name": "Samuel L. Jackson", "bio": "American actor and producer"},
        {"name": "Tom Hanks", "bio": "American actor and filmmaker"},
        {"name": "Leonardo DiCaprio", "bio": "American actor and film producer"}
    ]
    
    # Create actors
    for actor_data in sample_actors:
        actor = models.Actor(**actor_data)
        db.add(actor)
    
    db.commit()
    
    # Create movies
    for movie_data in sample_movies:
        movie = models.Movie(**movie_data)
        db.add(movie)
    
    db.commit()
    
    print(f"Seeded {len(sample_movies)} movies and {len(sample_actors)} actors")
    db.close()

if __name__ == "__main__":
    seed_movies()