import random

def main():
    level = get_level()
    score = 0

    for __ in range(10):
        x = generate_integer(level)
        y = generate_integer(level)
        z = x + y
            
        correct = False
        for __ in range(3):
            result = int((input(f"{x} + {y} = ")))
            if result != x + y:
                print("EEE")
            else:
                correct = True
                score += 1
                break    
        if correct == False:
            print(f"{x} + {y} = {z}")        
    print(score)

def get_level():
    while True:
        try:
            level = int(input("Level: "))
            if level in [1, 2, 3]:
                return level
        except ValueError: pass

def generate_integer(level):
    if level == 1:
        return random.randint(0,9)
    elif level == 2:
        return random.randint(10,99)
    elif level == 3:
        return random.randint(100,999)

if __name__ == "__main__":
    main()

