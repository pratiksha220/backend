from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import BaseModel
from database import get_db
from crud import get_user_by_email, create_user

# --- Constants ---
SECRET_KEY = "m9L6S2dAqV4r8Yz1F3uJ5pW7nH0xQKLB"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- Password hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Router ---
router = APIRouter()


# --- Pydantic model for JSON login ---
class LoginRequest(BaseModel):
    email: str
    password: str


# --- JWT helper ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- Register route ---
@router.post("/register")
def register(name: str, email: str, password: str, consent: bool, db: Session = Depends(get_db)):
    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email already registered")
    password_hash = pwd_context.hash(password)
    create_user(db, name, email, consent, password_hash=password_hash)
    return {"message": "User registered successfully"}


# --- Login route (accepts JSON or form data) ---
@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    # Detect request type
    content_type = request.headers.get("content-type", "")
    if content_type.startswith("application/json"):
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
    elif content_type.startswith("application/x-www-form-urlencoded"):
        form = await request.form()
        email = form.get("username")  # form key for OAuth2PasswordRequestForm
        password = form.get("password")
    else:
        raise HTTPException(status_code=400, detail="Unsupported content type")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

    user = get_user_by_email(db, email)
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# --- Current user retrieval ---
def get_current_user(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
