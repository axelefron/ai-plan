def slugify(text):
    return text.strip().lower().replace(" ", "-")

def main():
    print(slugify(input()))

main() 

# ==========================================================
# FUNCIONES
# ==========================================================
# def NO ejecuta nada. Define. Nada corre hasta que se llama.
# Por eso main() al final del archivo es obligatorio.
#
#   def slugify(text):
#       ^         ^
#       nombre    parámetro = etiqueta del casillero vacío
#
# El parámetro recibe su valor EN LA LLAMADA, lo pone quien llama.
# Adentro trabajo con el parámetro (text), nunca con el nombre
# de la función.
#
# SCOPE: el parámetro solo existe adentro de la función.
#        Afuera -> NameError.
#
# return -> devuelve el resultado a quien llamó (para el programa)
# print  -> muestra en pantalla (para el usuario)
#
# División de tareas:
#   funcion de logica = recibe, transforma, RETURN. No habla con nadie.
#   main              = pide input, la llama, IMPRIME.
# Se separan para poder testear la lógica sin teclado.
#
# ENCADENAR MÉTODOS: cada uno opera sobre el resultado del anterior.
#   text.strip().lower().replace(" ", "-")
# EL ORDEN IMPORTA: strip antes que replace, o los espacios de los
# extremos ya se convirtieron en guiones y no se pueden sacar.
#
# Los métodos de texto NO modifican el original: devuelven uno nuevo.
#
# Vocabulario: parámetro = el nombre en el def
#              argumento = el valor real que paso al llamar