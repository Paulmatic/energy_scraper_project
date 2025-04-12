import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    # Load environment variables from .env file
    db_user = os.getenv("DB_USERNAME", "postgres")  # Default to 'postgres' if not set
    db_pass = os.getenv("DB_PASSWORD", "pos1234data")  # Default password
    db_host = os.getenv("DB_HOST", "localhost")  # Default to 'localhost' for Docker
    db_port = os.getenv("DB_PORT", "5432")  # Default PostgreSQL port
    db_name = os.getenv("DB_NAME", "postgres")  # Default to 'postgres' database

    # Construct the PostgreSQL connection URL
    db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    # Create and return the database engine
    return create_engine(db_url)
