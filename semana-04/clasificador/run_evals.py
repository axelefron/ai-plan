import csv

with open("labels.csv") as file:
    reader = csv.DictReader(file)
    my_labels = list(reader)

# 2. Las del modelo, indexadas por texto para poder buscarlas
with open("eval_results.csv") as file:
    reader = csv.DictReader(file)
    model_answers = {}
    for row in reader:
        model_answers[row["text"]] = row


category_count = 0
sentiment_count = 0
priority_count = 0
missunderstandings = []

# 4. El loop sobre mis 20 filas
for label in my_labels:
    text = label["text"]

    if text not in model_answers:
        print(f"NOT FOUND: {text[:60]}")
        continue

    model = model_answers[text]

    if label["category"] == model["category"]:
        category_count += 1
    else:
        missunderstandings.append({
            "field": "category",
            "mine": label["category"],
            "model": model["category"],
            "text": text,
        })

    if label["sentiment"] == model["sentiment"]:
        sentiment_count += 1
    else:
        missunderstandings.append({
            "field": "sentiment",
            "mine": label["sentiment"],
            "model": model["sentiment"],
            "text": text,
        })

    if label["priority"] == model["priority"]:
        priority_count += 1
    else:
        missunderstandings.append({
            "field": "priority",
            "mine": label["priority"],
            "model": model["priority"],
            "text": text,
        })

total = len(my_labels)
print(f"category score:  {category_count}/{total}")
print(f"sentiment score: {sentiment_count}/{total}")
print(f"priority score:  {priority_count}/{total}")
print()

for m in missunderstandings:
    print(f"{m['field']:10} mine={m['mine']:20} model={m['model']:20} {m['text'][:60]}")