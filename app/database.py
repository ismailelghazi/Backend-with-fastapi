from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_DB = os.getenv("POSTGRES_DB", "talait")

encoded_user = urllib.parse.quote_plus(POSTGRES_USER)
encoded_password = urllib.parse.quote_plus(POSTGRES_PASSWORD)

DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{encoded_user}:{encoded_password}@{POSTGRES_SERVER}/{POSTGRES_DB}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"client_encoding": "utf8"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
