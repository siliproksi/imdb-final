from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
import re

class UserBase(BaseModel):
    email: EmailStr
    country: Optional[str] = None
    city: Optional[str] = None

class UserCreate(UserBase):
    password: str
    photo: Optional[str] = None  # Base64 encoded photo data
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least 1 number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least 1 non-alphanumeric character')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class GoogleLogin(BaseModel):
    token: str

class User(UserBase):
    id: int
    is_active: bool
    photo_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class MovieBase(BaseModel):
    title: str
    summary: Optional[str] = None
    release_year: Optional[int] = None
    duration: Optional[int] = None
    image_url: Optional[str] = None
    trailer_url: Optional[str] = None
    imdb_score: Optional[float] = None

class Movie(MovieBase):
    id: int
    popularity_score: float
    view_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ActorBase(BaseModel):
    name: str
    bio: Optional[str] = None
    photo_url: Optional[str] = None

class Actor(ActorBase):
    id: int
    
    class Config:
        from_attributes = True

class MovieActorForActor(BaseModel):
    movie: Movie
    character_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class ActorDetail(Actor):
    movies: List[MovieActorForActor] = []
    
    class Config:
        from_attributes = True

class MovieActor(BaseModel):
    actor: Actor
    character_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class RatingBase(BaseModel):
    rating: float
    comment: Optional[str] = None
    
    @validator('rating')
    def validate_rating(cls, v):
        if v < 1 or v > 10:
            raise ValueError('Rating must be between 1 and 10')
        return v

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int
    user_id: int
    movie_id: int
    created_at: datetime
    user: User
    
    class Config:
        from_attributes = True

class MovieDetail(Movie):
    actors: List[MovieActor] = []
    ratings: List[Rating] = []
    average_rating: Optional[float] = None
    total_ratings: int = 0
    
    class Config:
        from_attributes = True

class WatchlistItem(BaseModel):
    id: int
    movie: Movie
    added_at: datetime
    
    class Config:
        from_attributes = True

class SearchResult(BaseModel):
    movies: List[Movie] = []
    actors: List[Actor] = []