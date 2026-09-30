from dotenv import load_dotenv
from anthropic import Anthropic
from classifier import classify
import json
import csv

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5"

with open("messages.csv") as file:
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
    if i % 20 == 0:
        print(f"{i}/200")

print(f"{len(results)} classified, {len(all_texts) - len(results)} failed")

# escribir
with open("results.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["text", "category", "sentiment", "priority", "summary"])
    writer.writeheader()
    for row in results:
        writer.writerow(row)
