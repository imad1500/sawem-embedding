# embedding_server.py
import os
import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import uvicorn

# Charger le modèle (MiniLM, léger pour CPU)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Connexion à la base de données (Supabase Postgres)
DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# FastAPI app
app = FastAPI()

# Schéma pour la requête
class EmbedRequest(BaseModel):
    text: str
    product_id: int

@app.post("/embed")
def create_embedding(req: EmbedRequest):
    # Générer embedding
    embedding = model.encode(req.text).tolist()

    # Insérer dans la base (colonne embedding de type vector(384))
    cursor.execute(
        "UPDATE products SET embedding = %s WHERE id = %s",
        (embedding, req.product_id),
    )
    conn.commit()

    return {"status": "ok", "product_id": req.product_id}

# Point de test
@app.get("/")
def root():
    return {"message": "Embedding server is running!"}

# Pour lancer localement (Render utilise gunicorn)
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
