from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator
import logging

from src.config import config
from src.database.models import Base

logger = logging.getLogger(__name__)

# Create engine with connection pooling
engine = create_engine(
    config.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,
    max_overflow=20,
    echo=config.ENVIRONMENT == "development",  # Log SQL in development
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)

        # Enable TimescaleDB extension and create hypertable
        with engine.connect() as conn:
            # Enable TimescaleDB
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;"))

            # Check if hypertable already exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM timescaledb_information.hypertables
                    WHERE hypertable_name = 'usage_records'
                );
            """))
            hypertable_exists = result.scalar()

            if not hypertable_exists:
                # Create hypertable for usage_records
                conn.execute(text("""
                    SELECT create_hypertable(
                        'usage_records',
                        'date',
                        if_not_exists => TRUE
                    );
                """))
                logger.info("Created TimescaleDB hypertable for usage_records")

            conn.commit()

        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Context manager for database sessions

    Usage:
        with get_db() as db:
            sim = db.query(SIMCard).first()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db_session() -> Session:
    """Get database session (for dependency injection)"""
    return SessionLocal()
