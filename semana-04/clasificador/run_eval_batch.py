from classifier import classify
import csv

with open("labels.csv") as file:
    reader = csv.DictReader(file)
    all_texts = [row["text"] for row in reader]

results = []

for i, message in enumerate(all_texts, start=1):
    try:
        result = classify(message)
        result["text"] = message
        results.append(result)
    except Exception as e:
        print(f"Row {i} failed: {e}")

print(f"{len(results)} classified, {len(all_texts) - len(results)} failed")

with open("eval_results.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["text", "category", "sentiment", "priority", "summary"])
    writer.writeheader()

    for row in results:
        writer.writerow(row)