from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, crud
from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

def read_root():
    return {"message": "Blink counter backend is running!"}

@app.post("/register")
def register_user(name: str, email: str, consent: bool, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, name, email, consent)

@app.post("/blink")
def add_blink(email: str, blink_count: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.add_blink_data(db, user.id, blink_count)

@app.get("/user/{email}")
def get_user(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"name": user.name, "email": user.email, "consent": user.consent}
