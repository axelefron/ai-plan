def main():
    name = input("WHat's your name? ")
    print(hello(name))

def hello(to="world"): # --> si no hay input saluda a world
    return f"hello, {to}"

if __name__ == "__main__":
    main()