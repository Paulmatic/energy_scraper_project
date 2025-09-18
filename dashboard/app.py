import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from openai import OpenAI
import os

# Load environment variables
DB_HOST = os.getenv("DB_HOST", "energy_postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "energy_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Use new OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# PostgreSQL connection
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Streamlit UI
st.title("⚡ Energy Intelligence Search")
st.write("Search energy news articles using semantic similarity (OpenAI + pgvector).")

query = st.text_input("Enter your query:", "OPEC production cuts")
top_k = st.slider("Number of results", 1, 10, 5)

if st.button("Search"):
    with st.spinner("Generating embedding & searching..."):
        # 1. Get embedding
        embedding = client.embeddings.create(
            input=query,
            model="text-embedding-3-small"
        ).data[0].embedding

        # ✅ Convert embedding list to Postgres vector format
        embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"

        # 2. Query database
        sql = text("""
            SELECT article, article_category, article_description, date_, 
                   1 - (embedding <=> (:query_embedding)::vector) AS similarity
            FROM energy_intelligence_vectors
            ORDER BY embedding <=> (:query_embedding)::vector
            LIMIT :top_k;
        """)

        with engine.connect() as conn:
            results = conn.execute(sql, {"query_embedding": embedding_str, "top_k": top_k})
            df = pd.DataFrame(results.fetchall(), columns=results.keys())

        st.success(f"Top {top_k} results for: {query}")
        st.dataframe(df)
