def main():
    hello("world")
    goodbye("world")


def hello(name):
    print(f"Hello, {name}")

def goodbye(name):
    print(f"Goddbye, {name}")


if __name__ == "__main__": # --> __name__ value automatically set by python to be "main" when you run a file from the command line (terminal)
    main() # --> solo se llama a main() si la variable es name, si lo importo a otro documento que no diga name no se ejecuta main y se usa la funcion especififcada nada mas, no todas
    