"""
notes on the conditionals video

common conditional characters:
>
>=
<
<=
==
!=

commong keys:
if
elif
else
or
and

"""
"""
x = int(input("Whats the value of x?: "))
y = int(input("Whats the value of y?: "))
"""

"""
if x < y:
    print("x is less than y")

elif x > y:
    print("x is greather than y")

else:
    print("x is equal to y")

"""
"""
if x > y or x < y:
    print("x is not equal to y")

else:
    print("x is equal to y")

# mismo pero mas facil
if x != y:
    print("x is not equal to y")

else:
    print("x is equal to y")
"""
"""
score = int(input("Score: "))

if 90 <= score <= 100:
    print("Grade: A")

elif 80 <= score < 90:
    print("Grade: B")

elif 70 <= score < 80:
    print("Grade: C")

elif 60 <= score < 70:
    print("Grade: D")

else:
    print("Grade: F")
"""
"""
# se puede usar asi en vez de poner and y ambas conditions
# pero la mejor manera o mas simple para leer es la siguiente en eset ejemplo:

score = int(input("Score: "))

if score >= 90:
    print("Grade: A")

elif score >= 80:
    print("Grade: B")

elif score >= 70:
    print("Grade: C")

elif score >= 60:
    print("Grade: D")

else:
    print("Grade: F")

"""
"""
Esto seria para codearlo manuelmente y funciona, pero cuando tengo un programa largo es ineficiente y van a haber errores
si cada vez que tengo que testear algo lo codeo, por eso se crean funciones y se evita todo el tiempo codear condiciones

x = int(input("Enter the value of x here: "))

if x % 2 == 0: # --> aca se lee como "si divido (con division de remainder) x entre 2 y no sobra nada"
    print("x is even")
else:
    print("x is odd")
"""

def main():
    x = int(input("Enter the value of x here: "))
    if is_even(x):
        print(f"{x} is Even")
    else:
        print(f"{x} is Odd")

# def is_even(n):
#    if n % 2 == 0:
#        return True # --> tiene que ser en mayuscula True o False para que actue como variable boolean
#    else:
#       return False
#
# esta es la manera vieja, "noobie". La manera mas pythonica seria colapsando 4 lineas en 1 sola de esta manera:

def is_even(n):
    return n % 2 == 0 # --> no hace falta poner if x True o False por que "==" busca una equivalencia y evalua si es True o False, no hace falta codearlo xq python lo hace sin que se vea

main()
