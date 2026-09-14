# syntax errors los areglo yo desde el codigo
# try function es para prevenir errores, para chequear si hay excpeciones
# except tambien
# pass --> avoid silently and ignore 

def main():
    x = get_int()
    print(f"X is {x}")

def get_int():
    while True: # infinite loop hasta que de un error
        try:
            x = int(input("What's x?: "))
        except ValueError:
            # pass --> se podria poner aca el pass para que ignore y continue el loop si no quiero dar al usuario un mensaje
            print("x is not an integer")
        else:
            return x

main()