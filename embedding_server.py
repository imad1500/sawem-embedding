from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np

app = FastAPI()

# Modèle léger pour CPU
model = SentenceTransformer('all-MiniLM-L6-v2')  # ~384 dimensions, rapide et petit

# Input du POST pour générer un embedding
class TextItem(BaseModel):
    text: str

@app.post("/embedding")
def get_embedding(item: TextItem):
    vector = model.encode(item.text)
    return {"embedding": vector.tolist()}  # conversion en liste pour JSON
