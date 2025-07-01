from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    country = Column(String)
    city = Column(String)
    photo_url = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    ratings = relationship("Rating", back_populates="user")
    watchlist = relationship("Watchlist", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    summary = Column(Text)
    release_year = Column(Integer)
    duration = Column(Integer)  # in minutes
    image_url = Column(String)
    trailer_url = Column(String)
    imdb_score = Column(Float)
    popularity_score = Column(Float, default=0.0)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    ratings = relationship("Rating", back_populates="movie")
    watchlist = relationship("Watchlist", back_populates="movie")
    actors = relationship("MovieActor", back_populates="movie")

class Actor(Base):
    __tablename__ = "actors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    bio = Column(Text)
    birth_date = Column(DateTime)
    photo_url = Column(String)
    
    movies = relationship("MovieActor", back_populates="actor")

class MovieActor(Base):
    __tablename__ = "movie_actors"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    actor_id = Column(Integer, ForeignKey("actors.id"))
    character_name = Column(String)
    
    movie = relationship("Movie", back_populates="actors")
    actor = relationship("Actor", back_populates="movies")

class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    rating = Column(Float, nullable=False)  # 1-10 scale
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")

class Watchlist(Base):
    __tablename__ = "watchlist"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="watchlist")
    movie = relationship("Movie", back_populates="watchlist")