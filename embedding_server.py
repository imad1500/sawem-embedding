from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# Charger le modèle MiniLM
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

@app.route("/embed", methods=["POST"])
def embed():
    data = request.get_json()
    sentences = data.get("sentences", [])
    embeddings = model.encode(sentences).tolist()
    return jsonify({"embeddings": embeddings})

@app.route("/")
def home():
    return "✅ Embedding server is running with all-MiniLM-L6-v2"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
