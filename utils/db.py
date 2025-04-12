import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Optional: Set logging level for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_engine():
    # Read environment variables
    user = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db = os.getenv("DB_NAME", "energy_db")

    # Debugging output (optional, avoid logging sensitive info in prod)
    if not user or not password:
        logger.warning("Database username or password is missing!")

    logger.info(f"Attempting to connect to PostgreSQL at {host}:{port}, DB: {db}")

    # Construct database URL
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

    try:
        engine = create_engine(db_url)
        # Optional: test connection
        with engine.connect() as conn:
            logger.info("Successfully connected to the database.")
        return engine
    except OperationalError as e:
        logger.error("Database connection failed.", exc_info=e)
        raise

# If you want to test the connection by running this script directly:
if __name__ == "__main__":
    get_engine()
