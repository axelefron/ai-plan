# primero se define la funcion con "def" despues () y cuando termina ":"
# el contenido de la fucntion va indentado

def Hello(to = "FIU students"):
    print("Hello,", to)

name = input("Whats is your name?: ")

Hello(name)
Hello()

# se puede definir una funcion y que si no hay input sea el valor default
# y si se quiere un valor especifico del usuario se usa input 


def main():
    name = input("Whats is your name?: ")
    Hello(name)

def Hello(to = "FIU students"):
    print("Hello,", to)

main()

# las funciones se definen antes de usarlas, y para que el file quede mas ordenado
# se puede poner primero la funcion main y despues las demas funciones abajo y que queden
# definidas las funciones y de manera ordenada para despues usar el codigo sin estar constantemente creando funciones

# las funciones guardan variables que solo existen dentro de esa funcion, no queda guardadas para usar en cualquier momento del codigo
# esto se llama SCOPE --> variable only existing in the context which you defined it

# return en una fucntion no es lo mismo quee print, te da el valor pero no lo imprime en la pantalla/terminal necesariamente

# escrtibir exit() para volver a % en la terminal en vez de >>>

def main():
    x = int(input("Enter here the value of x: "))
    print("x squared is: ", square(x))

def square(n):
    return n * n

main()

# doble * (**) es para elevar un numero e indicar por cuanto 