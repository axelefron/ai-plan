import csv
import random

random.seed(42)

with open("messages.csv") as file:
    reader = csv.DictReader(file)
    all_texts = [row["text"] for row in reader]
    sample = random.sample(all_texts, 10)

with open("labels.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["text", "category", "sentiment", "priority"])
    for message in sample:
        writer.writerow([message, "", "", ""])
    print(len(sample))
