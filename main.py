from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, crud
from database import engine, Base, get_db
from auth import router as auth_router
from auth import get_current_user
from passlib.context import CryptContext
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import uvicorn
# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")
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

# ✅ Catch-all: serve React index.html for any unmatched route
@app.get("/{full_path:path}")
async def serve_react(full_path: str):
    index_path = os.path.join("dist", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="Frontend not built yet")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway injects PORT
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)