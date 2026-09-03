def main():
    price = money_to_float(input("Precio de venta: "))
    cost = money_to_float(input("Costo unitario: "))
    margin = (price - cost) / price
    print(f"Margen bruto: {to_percent(margin)}")


def money_to_float(m):
    money_floated = m.replace("$", "")
    return float(money_floated)


def to_percent(f):
    percent_margin = f * 100
    return f"{percent_margin:.1f}%"


main()

# ==========================================================
# MARGEN.PY — lo que me costó y por qué
# ==========================================================
#
# EL PATRÓN (igual que tip.py):
#   main()            -> pide input, llama a las funciones, imprime
#   funcion_auxiliar  -> recibe, transforma, RETURN. No imprime nada.
#   main()            -> al final del archivo, para que algo se ejecute
#
# ----------------------------------------------------------
# ERROR 1: inventar métodos
# ----------------------------------------------------------
# Escribí f.add("%")  ->  AttributeError: 'float' object has no attribute 'add'
#
# .add() NO EXISTE. Me lo inventé.
# Cada TIPO tiene sus propios métodos:
#   texto (str)  -> .replace() .strip() .lower() .title()
#   número (float/int) -> NO tiene métodos de texto
# Un número no se "concatena" con un método. Se arma un f-string.
# Si dudo qué métodos tiene algo: buscar "python <tipo> methods". No adivinar.
#
# ----------------------------------------------------------
# ERROR 2: usar str() para pegar cosas
# ----------------------------------------------------------
# Escribí str(percent_margin, "%")
#   -> TypeError: decoding to str: need a bytes-like object
# str() con UN argumento convierte a texto.
# str() con DOS argumentos hace otra cosa (decodificar bytes). No concatena.
#
# ----------------------------------------------------------
# ERROR 3 (el que más me costó): dónde va el formato
# ----------------------------------------------------------
# ANATOMÍA DEL F-STRING:
#
#   f"{percent_margin:.1f}%"
#     │              │    │
#     │              │    └─ afuera de las llaves = texto literal
#     │              └────── ADENTRO: dos puntos + formato
#     └───────────────────── adentro: la expresión a mostrar
#
# REGLA: adentro de {} se calcula. Afuera se imprime tal cual.
# El formato SIEMPRE va adentro, después de ":".
#
# Lo puse afuera dos veces:  {to_percent(margin)}:.1f   <- MAL, imprime ":.1f"
# Y lo puse en main en vez de en la función:
#   el formato va donde el valor TODAVÍA ES NÚMERO.
#   Cuando llega a main ya es texto -> no hay nada que formatear.
#
# Formatos útiles:  .1f = 1 decimal   .2f = 2 decimales (plata)
#
# ----------------------------------------------------------
# LO QUE NO ESTABA EN EL ENUNCIADO: floats mienten
# ----------------------------------------------------------
# 0.07 * 100  ->  7.000000000000001
# 0.6  * 100  ->  60.0        (este sale bien de casualidad)
#
# Los decimales se guardan en binario y algunos no tienen
# representación exacta (como 1/3 en decimal). El error aparece
# SOLO CON ALGUNOS NÚMEROS -> por eso probar con 1 caso no alcanza.
#
# REGLA: todo número calculado que se MUESTRA, va formateado.
#
# ----------------------------------------------------------
# CHECKLIST PARA LA PRÓXIMA
# ----------------------------------------------------------
# [ ] ¿Cada función devuelve (return) o solo asigna a una variable local?
# [ ] ¿Estoy usando el PARÁMETRO adentro, no el nombre de la función?
# [ ] ¿El método que uso existe para ESE tipo?
# [ ] ¿El formato está adentro de las llaves y en la función correcta?
# [ ] ¿Probé con más de un número, incluyendo uno "feo"?