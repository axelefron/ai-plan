import csv
import sys

if len(sys.argv) > 3:
    sys.exit("Too many command-line arguments")
elif len(sys.argv) < 3:
    sys.exit("Too few command-line arguments")

hogwarts_students_checked = []

try:  
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            last, first = row["name"].split(sep=", ")
            house = row["house"]
            hogwarts_students = {"first" : first, "last" : last, "house" : house}
            hogwarts_students_checked.append(hogwarts_students)
except FileNotFoundError:
        sys.exit(f"Could not read {sys.argv[1]}")

with open(sys.argv[2], "w", newline="") as file:    
        writer = csv.DictWriter(file, fieldnames=["first", "last", "house"])
        writer.writeheader()
        for row in hogwarts_students_checked:
             writer.writerow(row)

