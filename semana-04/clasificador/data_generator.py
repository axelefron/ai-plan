from dotenv import load_dotenv
from anthropic import Anthropic
import json
import csv

# Lee el .env de la raiz de ai-plan (load_dotenv sube por el arbol buscandolo)
# y mete ANTHROPIC_API_KEY en las variables de entorno del proceso.
load_dotenv()

# Anthropic() lee ANTHROPIC_API_KEY del entorno solo. Por eso load_dotenv va antes.
client = Anthropic()
model = "claude-haiku-4-5"   # Haiku porque generar texto falso no necesita un modelo caro


# ---------- Helpers de conversacion ----------
# Las listas son mutables y se pasan por referencia: estas funciones modifican
# la lista de afuera en el lugar, por eso no necesitan return.

def add_user_message(messages, text):
    user_message = {"role" : "user", "content" : text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role" : "assistant", "content" : text}
    messages.append(assistant_message)


def chat(messages, stop_sequences=None):
    # stop_sequences: lista de strings que cortan la generacion apenas aparecen.
    # Aca se usa para que el modelo no cierre el bloque markdown ni explique nada.
    message = client.messages.create(
    model=model,
    max_tokens=8000,          # techo, no pedido: solo se paga lo que genera.
                              # 8000 porque 20 mensajes largos no entran en 1000.
    messages=messages,
    stop_sequences=stop_sequences
    )
    # La respuesta viene como lista de bloques. [0] es el primero, .text su contenido.
    return message.content[0].text


# ---------- El prompt fijo ----------
# Se escribe una sola vez y se reusa en las 10 vueltas.
# Las instrucciones de variedad (largo, tono, typos, ambiguos) son lo que hace
# que el dataset sirva para evaluar: 200 mensajes identicos no prueban nada.
# La ultima linea es critica: sin ella la respuesta no es parseable con json.loads.

prompt_generator = """
    Generate 20 realistic messages that customers send to the support team
    of a credit/debit card issuer in the United States.

    Cover a mix of these situations:
    - a card was lost or stolen
    - a charge on the statement the customer does not recognize or disputes
    - the account got locked or frozen and the customer cannot log in
    - the customer wants a closed or paused account reactivated
    - a general question about fees, limits, statements or replacement cards

    Make them look like real people wrote them:
    - vary the length a lot: some are 5 words, some are a full paragraph
    - vary the tone: calm, confused, frustrated, angry, polite
    - include typos, lowercase, run-on sentences and missing punctuation in some
    - a few should be written by non-native English speakers
    - include just 3 or 4 that are genuinely ambiguous: the customer mixes two
    problems, or it is unclear what they actually want

    Never include full card numbers, SSNs, full addresses or any other data
    that could look like real private information. Use only last 4 digits,
    like "the card ending in 4412".

    Return ONLY a JSON array of strings. No numbering, no keys, no objects,
    no commentary. Just a list of 20 message strings.
"""


# Acumulador. Va AFUERA del for: si se creara adentro, cada vuelta lo resetearia.
all_messages = []


# ---------- Los 10 angulos ----------
# Sin esto, las 10 vueltas mandan el mismo prompt y devuelven variaciones del
# mismo puñado de mensajes. Cada angulo es un escenario concreto de cliente
# (no una metrica ni una pregunta de investigacion), 2 por categoria.

angles = [
    "customers whose card was lost or stolen while traveling out of town or abroad",
    "customers whose card was lost or stolen at a restaurant, a shopping mall or a university campus in the US",
    "customers complaining about the fees charged for a replacement card or expedited shipping",
    "customers whose account got locked or frozen within hours of reporting the card lost or stolen",
    "customers trying to reactivate an account that was paused or closed, some happy with the process and some not",
    "customers asking what happens to their autopays and subscriptions when the card number is cancelled",
    "customers who are not sure whether the card was lost or actually stolen, and do not know how to report it",
    "customers asking whether they can keep the same card number instead of getting a brand new one",
    "customers unsure whether to open a new account or just request a replacement card after losing theirs",
    "customers frustrated about having to re-link every subscription and payment after receiving a new card number",
]


# ---------- El loop: 10 vueltas x 20 mensajes = 200 ----------

for i in range(10):
    # Lista NUEVA en cada vuelta. Si se reusara, la vuelta 2 arrastraria la
    # conversacion de la 1: se pagaria por esos tokens y el modelo generaria
    # variaciones de lo que ya dijo.
    messages = []

    # f-string: pega el prompt fijo + el angulo de esta vuelta. i va de 0 a 9,
    # que es justo el rango de indices de la lista angles.
    add_user_message(messages, f"{prompt_generator}\n\nFor this batch: {angles[i]}")

    # PREFILL: se le escribe el principio de su propia respuesta. El modelo no
    # responde, continua. Y lo que sigue despues de abrir un bloque ```json es
    # el JSON, sin "Claro, aca va:" adelante.
    add_assistant_message(messages, "```json")

    # El stop sequence son los mismos backticks: cuando el modelo intenta cerrar
    # el bloque, la generacion se corta. La explicacion de abajo nunca existe.
    text = chat(messages, stop_sequences=["```"])

    # .strip() porque despues del prefill suele venir un salto de linea.
    # json.loads convierte el string en una lista de Python de verdad.
    batch = json.loads(text.strip())

    # .extend() y NO .append(): append meteria la lista entera como 1 elemento
    # (quedarian 10 elementos). extend recorre batch y agrega los 20 sueltos.
    all_messages.extend(batch)

    print(f"Batch {i +1}/10 - {len(all_messages)} so far")


# ---------- Escribir el CSV ----------
# Va DESPUES del for, con todo acumulado. Adentro del loop reescribiria el
# archivo 10 veces y solo quedaria el ultimo batch.

with open("messages.csv", "w", newline="") as file:
    # "w" = write (crea o pisa). newline="" evita lineas en blanco entre filas.
    # csv.writer (no DictWriter) porque aca hay strings sueltos, no diccionarios.
    writer = csv.writer(file)

    # Encabezado: una sola vez, antes del for. Es el nombre de la columna.
    writer.writerow(["text"])

    for message in all_messages:
        # writerow espera UNA LISTA de celdas. Si se le pasa el string pelado,
        # lo trata como secuencia de caracteres y escribe una letra por columna.
        writer.writerow([message])

print(len(all_messages))   # tiene que decir 200