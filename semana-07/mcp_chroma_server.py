import hashlib
import sys
from functools import lru_cache
from pathlib import Path

import chromadb
from chromadb.errors import NotFoundError
from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parent.parent
SEMANA_06 = ROOT / "semana-06"
DB_PATH = SEMANA_06 / "rag_db"
COLLECTION_NAME =  "banking_docs"

sys.path.insert(0, str(SEMANA_06))
from rag_system import clean_text, get_embedding_function  # noqa: E402  # type: ignore

MIN_CHARS = 50
MAX_CHARS = 20000
MAX_RESULTS = 10

mcp =FastMCP("DocumentMCP", log_level="ERROR")

@lru_cache(maxsize=1)
def embedding_fn():
    # cargar el modelo tarda unos segundos, se hace una sola vez
    return get_embedding_function()

def open_collection():
    """Devuelve la coleccion banking_docs o None si no existe."""
    if not DB_PATH.exists():
        return None
    client = chromadb.PersistentClient(path=str(DB_PATH))
    try:
        return client.get_collection(name=COLLECTION_NAME, embedding_function=embedding_fn())
    except NotFoundError:
        return None


@mcp.tool(
    name="search_docs",
    description=(
        "Busca por significado en los documentos del banco (APRs, categorías de "
        "crédito, procedimientos, responsabilidad en caso de fraude). Usala antes de "
        "responder cualquier pregunta sobre el banco y citá la fuente que devuelve. "
        "No modifica nada."
    ),
)

def search_docs(consultation: str, n_results: int = 3) -> str:
    consultation = consultation.strip()
    if not consultation:
        return "La consulta no puede estar vacía."

    collection = open_collection()
    if collection is None:
        return "Base no encontrada. Corré rag_system.py primero."

    total = collection.count()
    if total == 0:
        return("La base está vacía. Agregá documentos antes de buscar.")

    n = max(1, min(n_results, MAX_RESULTS, total))
    results = collection.query(query_texts=[consultation], n_results=n)

    blocks = []
    for text, meta in zip(results["documents"][0], results["metadatas"][0]):
        blocks.append(f"[Fuente: {meta['title']}]\n{text}")
    return "\n\n".join(blocks)


@mcp.tool(
    name="add_document",
    description=(
        "Agrega un documento nuevo a la base del banco. MODIFICA la base: usala solo "
        "cuando el usuario pida explícitamente agregar un documento. Rechaza títulos "
        "o contenidos que ya existan."
    ),
)

def add_document(title: str, content: str) -> str:
    title = title.strip()
    content = clean_text(content)

    if not title or not content:
        return "El título y el contenido no pueden estar vacíos."
    if len(content) < MIN_CHARS:
        return f"El contenido es demasiado corto para indexarlo (mínimo {MIN_CHARS} caracteres)."
    if len(content) > MAX_CHARS:
        return f"El contenido es demasiado largo (máximo {MAX_CHARS} caracteres)."

    collection = open_collection()
    if collection is None:
        return "Base no encontrada. Corré rag_system.py primero."

    if collection.get(where={"title": title}, limit=1)["ids"]:
        return f"El documento {title} ya existe en la base. No se agregó."

    chunk_id = "doc_" + hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
    existent = collection.get(ids=[chunk_id])
    if existent["ids"]:
        other = existent["metadatas"][0]["title"]
        return f"Ese contenido ya existe en la base bajo el título {other}. No se agregó."

    text = f"Tema: {title.replace("_", " ")}\n\nContenido:\n{content}"
    collection.add(
        ids=[chunk_id],
        documents=[text],
        metadatas=[
            {
                "source":"mcp",
                "title": title,
                "char_count": str(len(text)),
                "part": 0,
            }
        ],
    )
    return f"Documento agregado: {title} (id {chunk_id}, {len(text)} caracteres)."

if __name__ == "__main__":
    mcp.run(transport="stdio")