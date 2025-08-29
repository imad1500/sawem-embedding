# embedding_server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import psycopg2
import psycopg2.extras

# --- CONFIG PostgreSQL Supabase ---
DB_URL = os.getenv("DATABASE_URL")  # Mettre l'URL de ta BDD Supabase
conn = psycopg2.connect(DB_URL, sslmode="require")
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# --- FASTAPI APP ---
app = FastAPI(title="Embedding Server")

# --- CHARGER MODELE EMBEDDING CPU ---
model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

# --- SCHEMA POUR LA REQUETE ---
class Query(BaseModel):
    query: str
    top_k: int = 10  # nombre de produits retournés

# --- ENDPOINT DE RECHERCHE ---
@app.post("/search")
def semantic_search(q: Query):
    try:
        # Calculer embedding de la requête
        query_vec = model.encode(q.query).tolist()

        # Requête SQL avec pgvector
        cursor.execute(
            """
            SELECT *, embedding <-> %s AS distance
            FROM products
            ORDER BY distance ASC
            LIMIT %s
            """,
            (query_vec, q.top_k)
        )
        results = cursor.fetchall()
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
