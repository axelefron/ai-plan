# dictionaries --> stores keys and values (2 dimensional), key : value
# se usan {} para diccionarios, se puede poner todo en la misma linea o separarlo en lineas para que sea mas leible
# en vez de usar indexes numericos, se busca el key y te devuelve el value --> ejemplo: print(diccionario["key"]) --> imprime value
""""
friends = {
    "Luru" : "Lapis", 
    "Kike" : "Lapis", 
    "Botto" : "Aventura", 
    "Tiago" : "The one"
    }
"""

# print(friends["Luru"]) # --> esta es la manera tosca y larga, no es viable para un codigo largo
# print(friends["Kike"])
# print(friends["Botto"])
# print(friends["Tiago"])

""""
for friend in friends:
    print(friend, friends[friend], sep=", ") # --> se pone primero la key a buscar despues "," y despues diccionario[key] para que de el value (opcional usar coma e indicar como separar el key del value)
"""

# se pueden crear lists de dicitonaries

amigos = [
    {"name" : "Luru", "casa" : "Lapis", "hobbie" : "Bici"},
    {"name" : "Kike", "casa" : "Lapis", "hobbie" : "None"}, #--> None es para decir que no tiene valor y que no de error
    {"name" : "Botto", "casa" : "Aventura", "hobbie" : "Mirar futbol"},
    {"name" : "Tiago", "casa" : "The one", "hobbie" : "Piano"}
]

for amigo in amigos:
    print(amigo["name"], amigo["casa"], amigo["hobbie"], sep=", ")