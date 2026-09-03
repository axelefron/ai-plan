def convert(faces):
    return faces.replace(":)", "🙂").replace(":(", "🙁")

def main():
    print(convert(input()))

main()

# ==========================================================
# FUNCIONES CON PARÁMETRO Y RETURN  (faces.py, PS0)
# ==========================================================
# def NO ejecuta. Define. Nada corre hasta que alguien llama.
# Por eso main() al final del archivo es obligatorio.
#
# def convert(faces):
#     ^        ^
#     nombre   parámetro: el nombre que le doy a lo que ENTRE.
#              Adentro trabajo con "faces", no con "convert".
#
# return  -> le devuelve el resultado a quien la llamó.
# print   -> le muestra algo al usuario.
# No son lo mismo. convert devuelve, main imprime.
#
# División de tareas:
#   convert = la lógica. Recibe, transforma, devuelve. No habla con nadie.
#   main    = la interacción. Pide, llama a convert, imprime.
# Se separan para poder TESTEAR la lógica sin teclado (semana 5).
#
# Encadenar métodos: cada uno opera sobre lo que devolvió el anterior.
#   texto.replace(a, b).replace(c, d)
# El segundo replace actúa sobre el resultado del primero, no sobre texto.
#
# .replace() NO modifica el original: devuelve uno nuevo.