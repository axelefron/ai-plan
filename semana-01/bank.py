greet = input("Greeting: ").strip().casefold()

if greet.startswith("hello"):
    print("$0")
elif greet.startswith("h"): # se pone primero el if mas especifico y despues el elif mas "vago", para que python corra correctamente y haga los chequeos de si la condicion es True que deje de evaluar ahi y si es False que pase a la siguiente prueba
    print("$20")
else:
    print("$100")

