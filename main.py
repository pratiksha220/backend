from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, crud
from database import engine, Base, get_db
from auth import router as auth_router
from auth import get_current_user
from passlib.context import CryptContext

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@app.post("/register")
def register_user(name: str, email: str, consent: bool, password: str, db: Session = Depends(get_db)):
    # Check if user already exists
    user = crud.get_user_by_email(db, email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    password_hash = hash_password(password)

    # Create user
    return crud.create_user(db, name, email, consent, password_hash=password_hash)

@app.post("/blink")
def add_blink(blink_count: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Add blink data for the authenticated user (JWT protected).
    """
    return crud.add_blink_data(db, current_user.id, blink_count)

@app.get("/user/me")
def get_user_me(current_user: models.User = Depends(get_current_user)):
    """
    Return details of the authenticated user.
    """
    return {"name": current_user.name, "email": current_user.email, "consent": current_user.consent}
