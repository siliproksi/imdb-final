from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db, engine
import models
import schemas
import auth
import crud
import google_auth

models.Base.metadata.create_all(bind=engine)

# Seed sample data
try:
    from seed_data import seed_movies
    seed_movies()
except Exception as e:
    print(f"Error seeding data: {e}")

app = FastAPI(title="IMDB Clone API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

@app.get("/")
def read_root():
    return {"message": "IMDB Clone API"}

@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email is already registered
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="An account with this email already exists. Please use a different email or try logging in."
        )
    
    try:
        return crud.create_user(db=db, user=user)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to create account. Please try again later."
        )

@app.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No account found with this email address"
        )
    
    # Check password
    if not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    # Check if account is active
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is disabled. Please contact support."
        )
    
    access_token = auth.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": schemas.User.from_orm(db_user)}

@app.post("/auth/google")
def google_login(google_data: schemas.GoogleLogin, db: Session = Depends(get_db)):
    try:
        # Verify Google token and get user info
        user_info = google_auth.verify_google_token(google_data.token)
        
        # Check if user exists
        db_user = crud.get_user_by_email(db, email=user_info['email'])
        
        if not db_user:
            # Create new user from Google info
            try:
                db_user = crud.create_google_user(db, user_info)
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to create account with Google authentication. Please try again."
                )
        else:
            # Update existing user with Google info if needed
            if not db_user.google_id:
                db_user.google_id = user_info['google_id']
                if user_info.get('picture'):
                    db_user.photo_url = user_info['picture']
                db.commit()
        
        # Check if account is active
        if not db_user.is_active:
            raise HTTPException(
                status_code=401,
                detail="Account is disabled. Please contact support."
            )
        
        # Create access token
        access_token = auth.create_access_token(data={"sub": db_user.email})
        return {"access_token": access_token, "token_type": "bearer", "user": schemas.User.from_orm(db_user)}
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail="Invalid Google authentication token. Please try again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Google authentication failed. Please try again later."
        )

@app.get("/movies", response_model=list[schemas.Movie])
def get_movies(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_movies(db, skip=skip, limit=limit)

@app.get("/movies/{movie_id}", response_model=schemas.MovieDetail)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = crud.get_movie(db, movie_id=movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.get("/search")
def search_movies(q: str, search_type: str = "all", limit: int = 10, db: Session = Depends(get_db)):
    if len(q) < 3:
        limit = 3
    return crud.search_movies(db, query=q, search_type=search_type, limit=limit)

@app.post("/movies/{movie_id}/rate")
def rate_movie(
    movie_id: int, 
    rating: schemas.RatingCreate, 
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = auth.get_current_user(db, credentials.credentials)
    return crud.create_rating(db, rating=rating, movie_id=movie_id, user_id=current_user.id)

@app.post("/movies/{movie_id}/watchlist")
def add_to_watchlist(
    movie_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = auth.get_current_user(db, credentials.credentials)
    return crud.add_to_watchlist(db, movie_id=movie_id, user_id=current_user.id)

@app.get("/me/watchlist", response_model=list[schemas.WatchlistItem])
def get_watchlist(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = auth.get_current_user(db, credentials.credentials)
    return crud.get_user_watchlist(db, user_id=current_user.id)

@app.delete("/watchlist/{watchlist_id}")
def remove_from_watchlist(
    watchlist_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = auth.get_current_user(db, credentials.credentials)
    return crud.remove_from_watchlist(db, watchlist_id=watchlist_id, user_id=current_user.id)

@app.post("/upload-photo")
async def upload_photo(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    current_user = auth.get_current_user(db, credentials.credentials)
    # Simple file upload logic
    content = await file.read()
    filename = f"user_{current_user.id}_{file.filename}"
    # In production, save to cloud storage
    return {"filename": filename, "message": "Photo uploaded successfully"}