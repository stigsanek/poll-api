from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from poll_api.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True if settings.DEBUG else False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
