# se usa la lista en los () y despues [] y adentro el index number del valor deseado, empezado por index 0
# se indica el index [] teniendo en cuenta que va a imprimir o devolver el numero que se use -1 ( si quiero tener los primeros 3 pongo 3 que seria del 0 al 2)
# for i in range() --> se usa solo con numeros, si la variable es un str no funciona
# len --> lenght de la list o lo que se quiera medir

friends = ["Luru", "Kike", "Botto"]

# print(friends[0:3]) --> asi se imprime la lista, no imprime los valores de la lista en renglones separados

for friend in friends:
    print(friend)

for i in range(len(friends)):
    print(i + 1, friends[i]) # --> pone el index number primero y despues el vaalor de la lista, con todos los valores de la lista (+ 1 para que empieze en 1 en vez de 0)
    