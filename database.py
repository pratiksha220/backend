import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- Add this block ---
with engine.connect() as conn:
    # Ensure queue table exists
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS queue (
            id SERIAL PRIMARY KEY,
            payload TEXT NOT NULL,
            attempts INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))

    # Ensure password_hash column exists
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN password_hash TEXT;"))
    except Exception:
        pass  # Column already exists

    # Ensure consent column exists
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN consent BOOLEAN DEFAULT FALSE;"))
    except Exception:
        pass  # Column already exists

    conn.commit()
# --- End block ---

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
