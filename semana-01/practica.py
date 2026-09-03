# ask user for name and say hello 
name = input("What is your name?: ")
print("Hello,", name)

# cmnd z --> borrar/undo 
# cmnd shift z --> rehacer
# para usar el print f (format string) se pone:
#  f""" --> f antes de la primera " y las variables van entre {}

name = input("What is your name?: ")
print(f"Hello, {name}")

# variable.strip() --> para borrar espacios adentro de un str
# variable.capitalize() pone la primer letra en mayuscula
# variable.title() pone todas las palabras con primera letra mayuscula

name = input("What is your name?: ")
name = name.strip().capitalize().title()
# no hace falta poner asi pero sirve solo para el nombre --> name = name.capitalize()
print(f"Hello, {name}")

# se puede poner todo junto, es la manera correcta y mas optimizadora

name = input("What is your name?: ").strip().title()
print(f"Hello,", name)

# para separar se usa .split() --> por ejemplo nombre y apellido.
# entre () se deja un espacio para que separe

first, last = name.split(" ")
print(f"hello, {first}")