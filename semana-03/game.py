import random

while True:
    try:
        level = int(input("Level: "))
        if level > 0:
            break
    except ValueError: pass

chosen_number = random.randint(1, level)

while True:
    try:
        g = int(input("Guess: "))
        if g <= 0:
            continue
        if g == chosen_number:
            print("Just right!")
            break
        if g > chosen_number:
            print("Too large!")
        else:
            print("Too small!")
    except ValueError: pass


