from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()  # charge le .env si nécessaire

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')

# Connexion à la base PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/postgres")
conn = psycopg.connect(DATABASE_URL)

@app.get("/")
def read_root():
    return {"message": "Embedding service is up!"}

@app.post("/embed/")
def embed_text(text: str):
    embedding = model.encode(text).tolist()
    return {"embedding": embedding}

@app.get("/testdb/")
def test_db():
    with conn.cursor() as cur:
        cur.execute("SELECT 1;")
        result = cur.fetchone()
    return {"db_result": result}
