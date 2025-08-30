from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import psycopg2
import psycopg2.extras

# ----------------------------
# CONFIGURATION BASE DE DONNÉES
# ----------------------------
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

# ----------------------------
# INITIALISATION DU MODÈLE
# ----------------------------
model_name = "all-MiniLM-L6-v2"  # CPU léger ~200-300MB
model = SentenceTransformer(model_name, device="cpu")

# ----------------------------
# FASTAPI
# ----------------------------
app = FastAPI(title="Embedding Server")

class QueryRequest(BaseModel):
    text: str
    top_k: int = 5  # nombre de résultats similaires

# ----------------------------
# ROUTES
# ----------------------------
@app.get("/")
def home():
    return {"message": "Embedding server is running!"}

@app.post("/query")
def query_embeddings(req: QueryRequest):
    query_vec = model.encode(req.text).tolist()  # vecteur embedding
    top_k = req.top_k

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            """
            SELECT id, name, description, embedding
            FROM products
            ORDER BY embedding <-> %s
            LIMIT %s;
            """,
            (query_vec, top_k)
        )
        results = cur.fetchall()
    return {"results": results}
