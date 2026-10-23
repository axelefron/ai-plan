import shutil
from pathlib import Path
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from rag_tool import EMBEDDING_MODEL, DEFAULT_DB
from attack_cases import CASES

DEST = Path(__file__).parent / "rag_db_attack"

if DEST.exists():
    shutil.rmtree(DEST)
shutil.copytree(DEFAULT_DB, DEST)   # copia: rag_db real no se toca

client = chromadb.PersistentClient(path=str(DEST))
collection = client.get_collection(
    name="banking_docs",
    embedding_function=SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL),
)

collection.add(
    ids=[c["id"] for c in CASES],
    documents=[c["text"] for c in CASES],
    metadatas=[{"source": c["id"] + ".pdf", "title": c["title"],
                "char_count": str(len(c["text"])), "part": 1} for c in CASES],
)

# ¿Cada documento envenenado llega al top 3 para su pregunta?
for c in CASES:
    res = collection.query(query_texts=[c["user_query"]], n_results=3)
    ids = res["ids"][0]
    status = f"puesto {ids.index(c['id']) + 1}" if c["id"] in ids else "NO está en el top 3"
    print(f"{c['id']}: {status}")
