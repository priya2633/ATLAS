"""
Database engine configuration.

Creates the SQLAlchemy engine used by Atlas.
"""

from sqlalchemy import create_engine

from app.core.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)