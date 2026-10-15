import csv
import chromadb
from chromadb.errors import NotFoundError
from rag_system import search, get_embedding_function

# config
eval_questions_csv = "eval_questions.csv"
db_path = "./rag_db"
top_k = 27

# connect to existing database
client = chromadb.PersistentClient(path=db_path)

try: 
    collection = client.get_collection(
        name="banking_docs", 
        embedding_function=get_embedding_function()
    )
except NotFoundError: 
    print("Base no encontrada, corré rag_system.py primero.") 
    exit(1)

# eval counters
hit_at_1 = 0
hit_at_3 = 0
hit_at_k = 0
total = 0

with open(eval_questions_csv, encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        question_id = row["question_id"]
        question = row["question"]
        gold_doc = row["gold_doc"]
        gold_fact = row["gold_fact"]

        # retrieve relevant documents
        results = search(collection, question, top_k=top_k)

        titles = []
        top = []

        for meta in results["metadatas"][0]:
            titles.append(meta["title"])

            doc_number = meta["title"][:2]
            part = meta["part"]

            top.append(f"{doc_number}-p{part}")

        # find correct document position
        if gold_doc in titles:
            position = titles.index(gold_doc) + 1
        else:
            position = None

        # calculate retrieval metrics
        if position == 1:
            hit_at_1 += 1
        if position is not None and position <= 3:
            hit_at_3 +=1
        if position is not None:
            hit_at_k +=1
        
        total += 1

        # display results
        print(f"{question_id} | gold {gold_doc[:2]} | position {position}")

# final eval results
print("\n" + "=" * 50)
print("RETRIEVAL EVALUATION RESULTS")
print("=" * 50)

if total > 0:
    print(f"Database path: {db_path}, Top k: {top_k}\n")
    print(f"Hit@1: {hit_at_1}/{total} ({hit_at_1 / total:.1%})")
    print(f"Hit@3: {hit_at_3}/{total} ({hit_at_3 / total:.1%})")
    print(f"Hit@k: {hit_at_k}/{total} ({hit_at_k / total:.1%})")
else:
    print("No evaluation questions found.")