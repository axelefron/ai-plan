import os
from pathlib import Path
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Tiene que ser el MISMO modelo con el que semana-06 indexó, si no la búsqueda devuelve basura
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
DEFAULT_DB = Path(__file__).parent.parent / "semana-06" / "rag_db"
DB_PATH = Path(os.getenv("RAG_DB_PATH", DEFAULT_DB))

_collection = None

def get_collection():
    global _collection
    if _collection is None:   # el modelo pesa y no hace falta al importar
        client = chromadb.PersistentClient(path=str(DB_PATH))
        _collection = client.get_collection(
            name="banking_docs",
            embedding_function=SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL),
        )
    return _collection

def search_docs(query, top_k=3):
    results = get_collection().query(query_texts=[query], n_results=top_k)
    parts = []
    for text, meta in zip(results["documents"][0], results["metadatas"][0]):
        parts.append(f"[Fuente: {meta['title']}]\n{text}")
    return "\n\n".join(parts) if parts else "No documents found."
