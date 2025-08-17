from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    consent = Column(Boolean, default=False)
    blinks = relationship("BlinkData", back_populates="user")


class BlinkData(Base):
    __tablename__ = "blink_data"

    id = Column(Integer, primary_key=True, index=True)
    blink_count = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="blinks")
