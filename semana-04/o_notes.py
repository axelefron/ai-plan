"""
I/O --> Input and Output of files
Use info from files rather tgan previous code stored in the memory of that code and can not be re used whenever we want

With files we can save data persistently rather than in memory

Lists ---> stored as memory, info lost when exit the program

Open --> python function to open a file, letting me write to the file or read it

with --> in this context, i want to automatically open or close a file, as x which is how to name/store the file

CSV --> comma sepaprated values type of file
python has the CSV module
I can put in the first row of the csv the value,value para predeterminar el orden de los valores separados por comas y reducir los errores en mi codigo para acceder a los valores

Binary files --> 0 an 1, stores any type of data in values of 0 and 1

pillow --> image files and operate filters on those files (like instagram)

"""
"""
name = input("What is your name?  ")

with open("names.txt", "a") as file: # --> creates/re-creates and opens the file names.txt and "w" is indicated that i want to write, while "a" is for append and stores not only the last value passed but everything
    file.write(f"{name}\n") # write the name list into the file
    # file.close() --> close the file with the updated info if we dont use the with
"""
""" --> noob approach that works but it makes python review and do more
with open("names.txt", "r") as file: # r is for indicating that i want to read the file
    lines = file.readlines() # reads all the lines from the files and returns me the info in a list

for line in lines:
    print("Hello,", line.rstrip()) # --> prints hello to every name in the names.txt file but does not create a blank line between each print due to the rstrip
"""

""" --> correct approach but is not retieving sorted output
with open("names.txt", "r") as file:
    for line in file: # --> iterates and reads every line in the file and updates the info (in this case the names)
        print("Hello,", line.rstrip())
"""

names = []

with open("names.txt") as file: # --> default is read, the "r" is not needed
    for line in file:
        names.append(line.rstrip()) # --> load the info in memory before sorting and retrievieng the desired formatted output

for name in sorted(names, reverse=True):# the data is printed in descending order (z to a), the default is ascending and need no second argument
    print(f"Hello, {name}")

