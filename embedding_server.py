# embedding_server.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
from sentence_transformers import SentenceTransformer

# Charger l'URL de la base depuis la variable d'environnement
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set")

# Initialiser FastAPI
app = FastAPI(title="Sawem Embedding API")

# Initialiser le modèle de embeddings
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Modèle Pydantic pour requête JSON
class TextInput(BaseModel):
    text: str

# Endpoint racine
@app.get("/")
async def root():
    return {"message": "Sawem Embedding API is running."}

# Endpoint pour générer embeddings
@app.post("/embed")
async def embed_text(input: TextInput):
    try:
        embeddings = model.encode(input.text).tolist()
        return {"text": input.text, "embedding": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint pour tester la connexion PostgreSQL
@app.get("/db-test")
async def db_test():
    try:
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 AS result;")
                row = cur.fetchone()
                return {"db_test": row["result"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("embedding_server:app", host="0.0.0.0", port=int(os.getenv("PORT", 10000)), reload=False)
