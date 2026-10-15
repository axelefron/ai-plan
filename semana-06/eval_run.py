import csv
from chatbot import collection, ask_question, PROMPT_V3
from rag_system import search

eval_questions_csv = "eval_questions.csv"
label = "v3"

hit_at_1 = 0
hit_at_3 = 0
total = 0
output_rows = []

with open(eval_questions_csv, encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        question_id = row["question_id"]
        question = row["question"]
        gold_doc = row["gold_doc"]
        gold_fact = row["gold_fact"]

        titles = []
        results = search(collection, question, top_k=3)
        for meta in results["metadatas"][0]:
            titles.append(meta["title"])

        if gold_doc in titles:
            position = titles.index(gold_doc) + 1
            if position == 1:
                hit_at_1 += 1
            if position is not None:
                hit_at_3 +=1
        else:
            position = None
        
        total += 1

        try: 
            answer = ask_question(question, PROMPT_V3)
        except Exception as e:
            answer = (f"Error: {e}")
       
        output_rows.append([question_id, gold_doc, gold_fact, position, answer, "", "", ""])

        print(gold_doc, question_id, position)

with open(f"eval_results_{label}.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["question_id", "gold_doc", "gold_fact", "position", "answer","acierta", "cita_mal", "no_se"])
    writer.writerows(output_rows)
          
            

print(f"{hit_at_1} / {total}")
print(f"{hit_at_3} / {total}")

