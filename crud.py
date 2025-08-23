from sqlalchemy.orm import Session
import models
from sqlalchemy import func
from datetime import date

def create_user(db: Session, name: str, email: str, consent: bool, password_hash: str = None):
    user = models.User(name=name, email=email, consent=consent, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def add_blink_data(db: Session, user_id: int, blink_count: int = 1):
    """
    Increment today's blink count for the user if exists,
    otherwise create a new record.
    """
    # Check if a record exists today
    today = date.today()
    blink = (
        db.query(models.BlinkData)
        .filter(
            models.BlinkData.user_id == user_id,
            func.date(models.BlinkData.timestamp) == today
        )
        .first()
    )

    if blink:
        blink.blink_count += blink_count
    else:
        blink = models.BlinkData(user_id=user_id, blink_count=blink_count)
        db.add(blink)

    db.commit()
    db.refresh(blink)
    return blink

def get_blink_data_for_user(db: Session, user_id: int):
    """
    Returns all blink counts for the user aggregated by day
    """
    results = (
        db.query(
            func.date(models.BlinkData.timestamp).label("date"),
            func.sum(models.BlinkData.blink_count).label("total_blinks")
        )
        .filter(models.BlinkData.user_id == user_id)
        .group_by(func.date(models.BlinkData.timestamp))
        .order_by(func.date(models.BlinkData.timestamp))
        .all()
    )

    return [{"date": r.date, "blink_count": r.total_blinks} for r in results]

def add_blink_data(db: Session, user_id: int, blink_count: int = 1):
    """
    Increment today's blink count for the user if exists,
    otherwise create a new record.
    """
    # Check if a record exists today
    today = date.today()
    blink = (
        db.query(models.BlinkData)
        .filter(
            models.BlinkData.user_id == user_id,
            func.date(models.BlinkData.timestamp) == today
        )
        .first()
    )

    if blink:
        blink.blink_count += blink_count
    else:
        blink = models.BlinkData(user_id=user_id, blink_count=blink_count)
        db.add(blink)

    db.commit()
    db.refresh(blink)
    return blink
