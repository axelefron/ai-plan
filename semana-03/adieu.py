import inflect
p = inflect.engine()

names = []

while True:
    try:
        names.append(input("Name: "))
    except EOFError:
        break

print(f"\nAdieu, adieu, to {p.join(names)}")
    