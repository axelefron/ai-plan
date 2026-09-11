def main():
    coin_counter()

def coin_counter():
    amount_due = 50
    while amount_due > 0: 
        print("Amount due:", amount_due)
        cents = int(input("Insert coins here: "))
        if cents == 5 or cents == 10 or cents == 25:
            amount_due -= int(cents)
    print("Change Owed:",abs(amount_due))

main()