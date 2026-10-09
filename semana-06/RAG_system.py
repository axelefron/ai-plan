from pypdf import PdfReader
from pathlib import Path
import chromadb
 
# Load PDFs
def load_pdfs(docs_folder="docs"):
    """Load all PDF files from the specified folder and extract text."""
    documents = []
    pdf_files = sorted(Path(docs_folder).glob("*.pdf"))
 
    if not pdf_files:
        print(f"❌ Error: No PDF files found in '{docs_folder}'")
        return documents
 
    print(f"Loading {len(pdf_files)} PDF files...\n")
 
    for idx, pdf_path in enumerate(pdf_files, 1):
        try:
            reader = PdfReader(str(pdf_path))
            text = ""
 
            # extract text from all pages
            for page in reader.pages:
                text += page.extract_text() + "\n"
 
            # clean up text
            text = text.strip()
 
            if text:
                document = {
                    "id": f"doc_{idx:02d}",
                    "title": pdf_path.stem,
                    "content": text,
                    "source": str(pdf_path)
                }
                documents.append(document)
                print(f"  ✅ [{idx:2d}] {pdf_path.name} ({len(text)} chars)")
            else:
                print(f"  ⚠️  [{idx:2d}] {pdf_path.name} (empty)")
 
        except Exception as e:
            print(f"  ❌ [{idx:2d}] {pdf_path.name} - Error: {e}")
 
    print(f"\nSuccessfully loaded: {len(documents)} documents\n")
    return documents
 
 
def create_chunks(documents, chunk_size=512, overlap=128):
    """Split documents into chunks with overlap for better context preservation."""
    chunks = []
    chunk_id = 0
 
    print("Creating chunks...")
 
    for doc in documents:
        content = doc["content"]
        source = doc["source"]
        title = doc["title"]
 
        # Split content into chunks with overlap
        start = 0
        while start < len(content):
            end = min(start + chunk_size, len(content))
            chunk_text = content[start:end].strip()
 
            # Skip very small chunks (noise)
            if len(chunk_text) >= 50:
                chunk = {
                    "id": f"chunk_{chunk_id:04d}",
                    "content": chunk_text,
                    "source": source,
                    "title": title,
                    "char_count": len(chunk_text)
                }
                chunks.append(chunk)
                chunk_id += 1
 
            # Move forward with overlap
            start += (chunk_size - overlap)
 
    print(f"Created {len(chunks)} chunks\n")
    return chunks
 
 
def create_rag_database(chunks, db_path="./rag_db"):
    """Initialize Chroma vector database and add chunks with embeddings."""
    print("Initializing vector database...")
 
    # Create directory if it doesn't exist
    Path(db_path).mkdir(exist_ok=True)
 
    # Initialize Chroma client with persistent storage (NEW API)
    client = chromadb.PersistentClient(path=db_path)
 
    # Create or get collection
    collection = client.get_or_create_collection(
        name="banking_docs",
        metadata={"hnsw:space": "cosine"}
    )
 
    print(f"Adding {len(chunks)} chunks to database...")
 
    # Add chunks to collection
    ids = []
    documents = []
    metadatas = []
 
    for chunk in chunks:
        ids.append(chunk["id"])
        documents.append(chunk["content"])
        metadatas.append({
            "source": chunk["source"],
            "title": chunk["title"],
            "char_count": str(chunk["char_count"])
        })
 
    # Add all chunks at once
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
 
    print(f"✅ Database created at: {db_path}\n")
    return collection
 
 
def search(collection, query, top_k=3):
    """Perform semantic search on the vector database."""
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    return results
 
 
def display_results(results, query):
    """Format and display search results with relevance scores."""
    print("=" * 80)
    print(f"🔍 Query: {query}")
    print("=" * 80)
 
    if not results["documents"] or not results["documents"][0]:
        print("❌ No results found.")
        return
 
    for idx, (doc, distance, metadata) in enumerate(
        zip(results["documents"][0],
            results["distances"][0],
            results["metadatas"][0]),
        1
    ):
        # Convert distance to relevance score (0-100%)
        relevance = round((1 - distance) * 100, 2)
 
        print(f"\n📄 Result {idx} - Relevance: {relevance}%")
        print(f"   Source: {metadata['source']}")
        print(f"   Title: {metadata['title']}")
        print(f"   Content: {doc[:250]}...")
        print("-" * 80)
 
 
# ==================== EXECUTION ====================
 
if __name__ == "__main__":
    try:
        print("\n" + "=" * 80)
        print("🚀 RAG System - Banking and Finance Documents")
        print("=" * 80 + "\n")
 
        # Step 1: Load PDFs
        documents = load_pdfs("docs")
 
        if not documents:
            print("❌ No documents loaded. Exiting.")
            exit(1)
 
        # Step 2: Create chunks
        chunks = create_chunks(documents, chunk_size=512, overlap=128)
 
        if not chunks:
            print("❌ No chunks created. Exiting.")
            exit(1)
 
        # Step 3: Create vector database
        collection = create_rag_database(chunks, db_path="./rag_db")
 
        # Step 4: Test with banking-specific queries
        test_queries = [
            "What is my credit limit and how does it work?",
            "What is the maximum liability in case of fraud?",
            "How are interest rates calculated on my account?",
            "What are my rights regarding disputed transactions?",
            "How do I protect my account from identity theft?",
            "What fees apply to my account?",
            "How do I consolidate my debt?",
            "What is a balance transfer and when should I use it?"
        ]
 
        print("\n" + "=" * 80)
        print("Running Banking-Specific Test Queries")
        print("=" * 80 + "\n")
 
        for query in test_queries:
            results = search(collection, query, top_k=3)
            display_results(results, query)
            print()
 
        print("=" * 80)
        print("RAG system is ready for use!")
        print("=" * 80 + "\n")
 
    except ModuleNotFoundError as e:
        print(f"❌ Missing module: {e}")
        print("\nInstall required packages:")
        print("  python3 -m pip install pypdf chromadb sentence-transformers")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()