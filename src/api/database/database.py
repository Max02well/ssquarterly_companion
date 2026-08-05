from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus


print("Connecting to the database...")
from src.config import settings
password = quote_plus("Maxwell@2021")
DB_URL = f"postgresql+psycopg://postgres:{password}@localhost:5432/quaterly_companionai"
engine = create_engine(
    # settings.DATABASE_URL,
    DB_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()