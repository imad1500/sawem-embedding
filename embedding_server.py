from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

app = FastAPI(title="Embedding Server")

# Chargement du modèle MiniLM CPU
model = SentenceTransformer("all-MiniLM-L6-v2")

class EmbeddingRequest(BaseModel):
    texts: list[str]

class EmbeddingResponse(BaseModel):
    embeddings: list[list[float]]

@app.post("/embed", response_model=EmbeddingResponse)
async def embed(request: EmbeddingRequest):
    embeddings = model.encode(request.texts, convert_to_numpy=True).tolist()
    return EmbeddingResponse(embeddings=embeddings)

@app.get("/")
async def root():
    return {"message": "Embedding server is running."}
