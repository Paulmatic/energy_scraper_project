from sqlalchemy import create_engine
import os

def get_engine():
    user = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db = os.getenv("DB_NAME", "energy_db")

    return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
