# module --> library on python with built in function and features (some must be imported)
# to creatre re-usable code 
# import "x" from -->  to use that library
# types:
# - random --> example: random.choice(seq)
# - statistics 
# command-line arguments --> python feature that allows for input when not specifically prompted 
# sys --> system (functionalities between the system)
# sys.argv --> argument vector (list of all the words the human types before hitting enter)
# sys.exit --> exit when pormpted in the code if some condition is satisfied
# slice --> a slice of a list is a subsets of a list. (or other datatypes)
# packages --> 3rd party libraries (not built in with python) that has to be installed to be used
# PyPI --> website that allows to download and install packages
# cowsay --> package that allows you to have a cow to say something
# pip --> package manager, a program that comes with pyhton for installing packages in your mac
# APIs --> Application Proggraming Interface
# - it can refer to python files and functions but often APIS refer to 3rd party servicers to use in your code and talk to 
# - pretends to be a browser, connect to the 3rd party API on a server and downloads data to use in your program
# requests --> common python package API that requests in the web with python code
# JSON --> type of value/data (Java Script Open Location) --> a language (text) format for exchanging data between computers

"""
import random
coinflip = random.choice(["Heads", "Tails"])) 

from random import choice
coinflip = choice(["Heads", "Tails"])

print(coinflip) --> prints heads or tails with 50% probability for each
"""
"""
import random

number = random.randint(1, 10)
print(number) --> prints numbers from 1 to 10 INCLUSIVE with 10% probability for each
"""
"""
import random 

cards = ["1 de basto", "3 de espada", "7 de oro"]
random.shuffle(cards) --> literally shufflys the values on the list, then you have to print the shuffled list, it does not return shuffled output if not prompted to

for card in cards:
    print(card)
"""
"""
import statistics
print(statistics.mean([100, 90])) --> prints the mean of the numbers included on the list
"""

# import sys

# if len(sys.argv) < 2:
#    print("Too few arguments") 
# elif len(sys.argv) > 2:
#    print("Too many arguments")
# else:
#    print("Hello, my name is", sys.argv[1])

#try:
#    print("Hello, my name is", sys.argv[1]) # --> inputs the 1st word of the users input in the terminal argument, it is index 1 because index 0 is the python3 namefile.py
# except IndexError:
#    print("Too few arguments") 
 
""" --> this is for exiting when there was no input or too much of it and printing the error message or the actual print of the name
if len(sys.argv) < 2:
    sys.exit("Too few arguments") 
elif len(sys.argv) > 2:
    sys.exit("Too many arguments")

print("Hello, my name is", sys.argv[1])
"""
"""
if len(sys.argv) < 2:
    sys.exit("Too few arguments")

for arg in sys.argv[1:]: # --> here im slicing the list and indicating to start from index 1 to the end, if i want ex to end at 10 --> [1:10]
    print("Hello, my name is", arg)
"""
"""
import cowsay
import sys

if len(sys.argv) == 2:
    cowsay.cow("Hello, " + sys.argv[1])
    cowsay.trex("Hello, " + sys.argv[1]) --> imprime un t rex que dice el print que se la pasa, en este caso Hello, Axel
"""

import json
import requests
import sys

if len(sys.argv) != 2:
    sys.exit()

# esto es para que python busque en la web a traves de la URL, en este caso una cancion de itunes, del usuario (que va a ser el artista escrito en la terminal osea el arg 1)
response = requests.get("https://itunes.apple.com/search?entity=song&limit=5&term=" + sys.argv[1])
# print(json.dumps(response.json(), indent=2)) --> para imprimir toda la info en JSON format de una cancion del artista del usuario

o = response.json()
for result in o["results"]:
    print(result["trackName"]) # esto es solo para imprimir los nombres de las canciones, es para fromattear el print para que sea leible en vez de JSON

