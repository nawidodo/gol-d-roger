"""Database configuration and connection management."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Create base class for models
Base = declarative_base()

# Database configuration
TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

# Create engine
if TURSO_DATABASE_URL and TURSO_AUTH_TOKEN:
    # Turso connection string format
    engine = create_engine(
        f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}",
        connect_args={"check_same_thread": False},
        echo=False
    )
else:
    # Fallback to local SQLite for development
    engine = create_engine(
        "sqlite:///gold_tracker.db",
        connect_args={"check_same_thread": False},
        echo=True
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
