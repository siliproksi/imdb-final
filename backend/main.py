from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db, engine
import models
import schemas
import auth
import crud

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
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = auth.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token = auth.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": schemas.User.from_orm(db_user)}

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

@app.get("/me/watchlist")
def get_watchlist(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    current_user = auth.get_current_user(db, credentials.credentials)
    return crud.get_user_watchlist(db, user_id=current_user.id)

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