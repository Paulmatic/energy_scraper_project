import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    # Load environment variables from .env file
    db_user = os.getenv("DB_USER", "postgres")       # Matches .env
    db_pass = os.getenv("DB_PASSWORD", "pos1234data")  # Matches .env
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "postgres")

    # Construct the PostgreSQL connection URL
    db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    # Create and return the database engine
    return create_engine(db_url)
