# utils/vector_store.py
import os
import openai
import pandas as pd
from sqlalchemy import text
from utils.db import get_engine

openai.api_key = os.getenv("OPENAI_API_KEY")

def embed_text(text: str) -> list:
    """Generate embedding for a given text."""
    if not text:
        return []
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def upload_vectors(df: pd.DataFrame, table_name="energy_intelligence_vectors"):
    """Upload embeddings + metadata to Postgres (pgvector)."""
    if df.empty:
        return

    engine = get_engine()
    with engine.begin() as conn:
        # Create table if not exists
        conn.execute(text(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            article TEXT,
            article_category TEXT,
            article_description TEXT,
            date_ DATE,
            embedding VECTOR(1536) -- size depends on model used
        );
        """))

        for _, row in df.iterrows():
            content = f"{row['article']} {row['article_description'] or ''}"
            embedding = embed_text(content)

            conn.execute(
                text(f"""
                INSERT INTO {table_name} 
                (article, article_category, article_description, date_, embedding)
                VALUES (:article, :article_category, :article_description, :date_, :embedding)
                """),
                {
                    "article": row["article"],
                    "article_category": row["article_category"],
                    "article_description": row["article_description"],
                    "date_": row["date_"],
                    "embedding": embedding,
                }
            )
