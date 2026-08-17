# ============================================================
# DATABASE CONFIGURATION
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# ============================================================
# DATABASE URL
# ============================================================

# SQLite will create a file called student_predictions.db
# inside the backend folder.

DATABASE_URL = "sqlite:///./student_predictions.db"


# ============================================================
# CREATE DATABASE ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# ============================================================
# CREATE DATABASE SESSION
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============================================================
# BASE CLASS
# ============================================================

# All database tables will inherit from this Base class.

Base = declarative_base()