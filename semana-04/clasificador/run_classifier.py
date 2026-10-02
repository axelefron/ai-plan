from classifier import classify   # <- lo unico que de verdad hace falta
import csv

# Estas 4 lineas sobran: al importar classify, Python ya ejecuto classifier.py
# entero, que ya hizo load_dotenv() y ya creo su propio cliente. Aca se crea
# un segundo cliente que nunca se usa. No rompe nada, pero se puede borrar.
model = "claude-haiku-4-5"


# ---------- Leer los 200 mensajes ----------
# DictReader usa la primera fila del archivo como nombres de columna, asi que
# cada fila se accede por nombre: row["text"].
#
# list(...) / la comprehension tienen que estar ADENTRO del with: el reader
# lee del archivo abierto, y al salir del with el archivo se cierra.
# Ademas el reader se consume: una vez recorrido, queda vacio.

with open("messages.csv") as file:
    reader = csv.DictReader(file)
    all_texts = [row["text"] for row in reader]   # list comprehension: un for compacto


# ---------- Clasificar los 200 ----------

results = []   # afuera del for, si no se resetea en cada vuelta

# enumerate devuelve (indice, elemento) juntos. start=1 para contar desde 1
# en el print en vez de desde 0.
for i, message in enumerate(all_texts, start=1):
    try:
        result = classify(message)       # dict con category/sentiment/priority/summary
        result["text"] = message         # se agrega una 5a clave: el mensaje original,
                                         # para poder revisar el CSV despues
        results.append(result)           # append (no extend): se agrega UN dict
    except Exception as e:
        # El try/except es lo que hace que la fila 147 rota no mate a las otras 199.
        # Puede fallar por json.JSONDecodeError (el modelo no devolvio JSON valido)
        # o por un error de la API (429 rate limit, red).
        # Se imprime cual fila fallo y el loop SIGUE.
        print(f"Row {i} failed: {e}")

    # Progreso cada 20 vueltas. Sin esto son varios minutos de terminal muerta
    # sin saber si avanza o se colgo. Cada 20 y no cada 1 para no llenar de ruido.
    if i % 20 == 0:
        print(f"{i}/200")

# Cuantas sobrevivieron. Si no dice 200 classified / 0 failed, hubo filas perdidas.
print(f"{len(results)} classified, {len(all_texts) - len(results)} failed")


# ---------- Escribir el resultado ----------
# Aca si va DictWriter (no csv.writer): el contenido son diccionarios.

with open("results.csv", "w", newline="") as file:
    # fieldnames define el ORDEN de las columnas. Manda esto, no el orden de las
    # claves del dict: por eso "text" puede ir primero aunque se agrego ultimo.
    # Tienen que coincidir EXACTO con las claves que devuelve classify().
    writer = csv.DictWriter(file, fieldnames=["text", "category", "sentiment", "priority", "summary"])

    # writeheader() escribe la fila de nombres de columna sola. No existe en
    # csv.writer, donde el encabezado hay que escribirlo a mano con writerow.
    writer.writeheader()

    for row in results:
        writer.writerow(row)   # el dict entero: DictWriter mapea clave -> columna