"""
with open("students.csv") as file:
    for line in file:
        name, university = line.rstrip().split(",") # strips the blanks bewteen lines and splits the values with the commas as separate values as a list
        print(f"{name} studies in {university}") # print the positoin 0 which would be the name and the position 1 which is the univ (0 is before the comma and 1 right after it)
"""


"""
students = []

with open("students.csv") as file:
    for line in file:
        name, university = line.rstrip().split(",")
        students.append(f"{name} studies in {university}") # appendind the whole line in the list

for student in sorted(students):
    print(student)
"""

"""
students = []

with open("students.csv") as file:
    for line in file:
        name, university = line.rstrip().split(",")
        student = {"name" : name, "university" : university}
        students.append(student)

def get_name(student):
    return student["name"]

for student in sorted(students, key=get_name): # arguments can be functions. I am specifying python to sort by the key within the dictionary student
    print(f"{student['name']} studies in {student['university']}")

# for student in sorted(students, key=lambda student: student["name"]): --> if i dont define a function that wont be used again i use this default statemnt with the desired key
# lamba is a function not defined, an anonymus function
"""

"""
import csv

students = []

with open("students.csv") as file:
    reader = csv.DictReader(file) # --> reads the csv file and anlyze where are the commas, potential errors and more. it reads as a dictiomary instead of a list
    for row in reader:
        students.append({"name" : row["name"], "university" : row["university"]})

for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} studies in {student['university']}")
"""

import csv

name = input("What's your name? ")
university = input("In which university are you studying? ")

with open("students.csv", "a") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "university"])# writes the new file and handles the input with comma and separates it correctly in the csv. it works with dictionaries and you must indicate the field names in a list
    writer.writerow({"name" : name, "university" : university}) # no importa el orden mientras sea el correcto key value pair por que arriba defino los fieldnames