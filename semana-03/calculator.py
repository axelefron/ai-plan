def main():
    x = int(input("What's x?: "))
    print("x sqaured is", square(x))

def square(num):
    return num * num

if __name__ == "__main__":
    main()