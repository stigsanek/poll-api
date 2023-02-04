from typing import Generator

from poll_api.db import SessionLocal


def get_db() -> Generator:
    """Return database session

    Yields:
        Generator: Database session
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
