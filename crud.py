from sqlalchemy.orm import Session
import models

def create_user(db: Session, name: str, email: str, consent: bool):
    user = models.User(name=name, email=email, consent=consent)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def add_blink_data(db: Session, user_id: int, blink_count: int):
    blink = models.BlinkData(user_id=user_id, blink_count=blink_count)
    db.add(blink)
    db.commit()
    db.refresh(blink)
    return blink
