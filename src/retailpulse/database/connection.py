import os
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

# Load database settings from .env
load_dotenv()

# Get database details
database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME")
)

# Create database engine
engine = create_engine(database_url)


def test_connection():
    try:
        with engine.connect() as connection:
            logging.info("PostgreSQL connection successful!")
            print("Connected to PostgreSQL successfully!")

    except Exception:
        logging.exception("PostgreSQL connection failed!")
        raise
