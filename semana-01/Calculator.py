x = input("What is the value of x?: ")
y = input("What is the value of y?: ")

z = x + y

print(z)

# hay que indicar que es un int, si no se concatenan strings

x = int(input("What is the value of x?: "))
y = int(input("What is the value of y?: "))

print(x + y)

# se puede poner int(input()) o directo en el resultado z = int(x) + int(y)
# para que sea un decimal se usa float()

# se puede usar round() para que redondee el numero decimal
# round(number [, ndigits]) --> 1er argumento es el numero y oblitatorio, 
# despues entre [] es opcional, se especifica cuantos decimales usar para redondear

x = float(input("What is the value of x?: "))
y = float(input("What is the value of y?: "))

z = round(x + y)
print(f"{z:,}") # se le indica a python que use la , para separar los 000

# otros ejemplos

x = float(input("What is the value of x?: "))
y = float(input("What is the value of y?: "))

z = round(x / y, 2)

print(z)

# todo junto

x = float(input("What is the value of x?: "))
y = float(input("What is the value of y?: "))

z = (x / y)

print(f"{z:.2f}") # --> asi se usa para indicar cuantos decimales redondear con un f string