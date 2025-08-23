import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Ensure timestamp column exists in blink_data
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='blink_data' AND column_name='timestamp'
    """))
    if result.rowcount == 0:
        conn.execute(text("ALTER TABLE blink_data ADD COLUMN timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
        conn.commit()

    result = conn.execute(text("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='blink_data' AND column_name='date'
    """))
    if result.rowcount == 0:
        conn.execute(text("ALTER TABLE blink_data ADD COLUMN date DATE DEFAULT CURRENT_DATE"))
        conn.commit()
        
# --- Ensure queue table exists ---
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS queue (
            id SERIAL PRIMARY KEY,
            payload TEXT NOT NULL,
            attempts INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    conn.commit()

# --- Ensure password_hash column exists in users table ---
with engine.connect() as conn:
    # Check if password_hash column exists
    result = conn.execute(text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='users' AND column_name='password_hash'
    """))
    if result.rowcount == 0:
        conn.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR NOT NULL DEFAULT ''"))
        conn.commit()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
