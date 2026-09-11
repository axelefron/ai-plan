def main():
    print_column(3)
    print()
    print_row(4)
    print()
    print_square(2)

def print_column(height):
    for _ in range(height):
        print("#")

def print_row(width):
    print("?" * width)

def print_square(size):
    for i in range(size):
        print("#" * size)

""" --> se puede hacer asi tambien si es mas comod y facil de leer pero es menos compacto el codigo
def print_square(size):
    # for each row in square
    for i in range(size):
        # for each brick in row (uso la o como otra letra en vez de i para que sea algo distinto)
        for o in range(size):
            # print brick
            print("#", end="") # en with no new line
        print() # new blank line at the END of the row
""" 
main()

