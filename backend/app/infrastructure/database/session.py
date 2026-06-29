"""
Database session management.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database.config import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Yield a database session.

    Ensures every session is properly closed.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()