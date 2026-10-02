from dotenv import load_dotenv
from anthropic import Anthropic
import json

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5"


# ---------- El system prompt: el criterio de clasificacion ----------
# Va en system y no en el mensaje de usuario porque es lo FIJO: se repite
# identico en las 200 llamadas y lo unico que cambia es el mensaje del cliente.
# Tenerlo separado significa que para experimentar (dia 12) se toca solo esto,
# sin tocar el loop.
#
# Los valores permitidos se listan explicitos: sin eso el modelo inventa
# "urgent" o "very_negative" y el CSV queda inservible para contar o filtrar.
#
# OJO - bug conocido: "the card ending in XXXX" se escribio como marcador de
# posicion pero el modelo lo lee como plantilla. Resultado: unos summaries
# copian los digitos reales y otros escriben "XXXX" literal. Hay que reescribir
# la regla diciendo que NO hacer, sin dar una frase rellenable.

system_prompt = """
    You classify messages that customers send to the support team of a
    credit/debit card issuer in the United States.

    For each message, output exactly these four fields:

    category — use exactly one of these values:
    lost_stolen_card
    charge_dispute
    account_locked
    account_reactivation
    general_inquiry

    sentiment — the customer's TONE, not the severity of their situation.
    Use exactly one of these values:
    positive  thanks, praise, or satisfaction with the service
    neutral   states the problem factually; may be worried or urgent,
                but is not angry at the company
    negative  frustrated, angry, sarcastic, complains about the company
                or the process, uses all caps or insults

    A customer reporting a stolen card calmly is neutral, even though the
    situation itself is bad.

    priority — use exactly one of these values:
    high    money is at risk right now, or the customer cannot access their funds
    medium  a real problem, but no immediate urgency
    low     an informational question

    summary — one sentence, 15 words maximum, describing what the customer needs.

    Rules:
    - Use only the exact values listed above. Never invent new ones.
    - If the message mentions a lost or stolen card, use lost_stolen_card as the category, 
    even if the customer also reports a locked account, a disputed charge, or anything else.
    - Never include card numbers, SSNs, names or any other personal data in the summary. 
    Do not include card digits at all, not even the last four — refer to it simply as "the card"

    Return ONLY a JSON object with the keys category, sentiment, priority and
    summary. No commentary, no explanation, no extra keys.
"""


# ---------- Helpers de conversacion ----------
# Sin return: las listas son mutables y se pasan por referencia, asi que
# .append() modifica la lista de afuera en el lugar.

def add_user_message(messages, text):
    user_message = {"role" : "user", "content" : text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role" : "assistant", "content" : text}
    messages.append(assistant_message)


# ---------- chat() con dos parametros opcionales ----------
# El patron params + if existe porque la API NO acepta system=None ni
# stop_sequences=None. No alcanza con ponerlos en la firma: hay que decidir
# si la clave entra al diccionario o no.
#
# Clave: las opcionales NO van en el dict inicial. Si estuvieran ahi, el if
# no agregaria nada y se mandaria None igual.

def chat(messages, system=None, stop_sequences=None):
    params = {
        "model": model,
        "max_tokens": 8000,
        "messages": messages,
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    # ** desarma el diccionario en argumentos con nombre:
    # {"model": x, "max_tokens": y} se convierte en model=x, max_tokens=y
    message = client.messages.create(**params)
    return message.content[0].text


# ---------- classify(): un mensaje -> un dict de 4 claves ----------

def classify(text):
    # Conversacion nueva por cada mensaje: no se arrastra nada del anterior.
    messages = []

    # Las etiquetas <message> marcan donde empieza y termina el DATO.
    # Si el cliente escribio algo que parece una orden ("ignore the above..."),
    # queda claramente encerrado y el modelo lo trata como texto a clasificar,
    # no como instruccion. Es seguridad, no estetica.
    add_user_message(messages, f"<message>{text}</message>")

    # Prefill + stop sequence: la misma tecnica del generador.
    add_assistant_message(messages, "```json")

    # Se llama "response" y no "text" para no pisar el parametro de la funcion,
    # que tiene el mensaje del cliente.
    response = chat(messages, system=system_prompt, stop_sequences=["```"])

    # Si esto no explota, la tecnica funciono: lo que volvio es JSON de verdad.
    clean_json = json.loads(response.strip())
    return clean_json


# ---------- Tests ----------
# El if __name__ == "__main__" separa lo que este archivo OFRECE (las funciones)
# de lo que HACE al ejecutarlo (correr los tests).
#
# python classifier.py                      -> corre los tests
# from classifier import classify           -> define todo, NO corre los tests
#
# Sin esta guarda, importar classify desde run_classifier.py dispararia las
# 5 llamadas a la API cada vez.
#
# Los 5 tests cubren modos de falla distintos:
#   test1 - sin informacion: que priority inventa?
#   test2 - ambiguo: disputa vs tarjeta nueva, prueba la regla de desempate
#   test3 - pregunta, no pedido: deberia ser priority low
#   test4 - caso facil, control
#   test5 - pedido de feature: no entra bien en ninguna categoria (hueco en la taxonomia)

if __name__ == "__main__":
    test1 = "lost card"
    test2 = "Someone must have taken my card ending in 5493 from the university library. I didn't notice until I tried to pay for lunch. There's a charge for $34.99 at a gas station. I want dispute this charge but I also need new card immediately."
    test3 = "my card ending in 5491 - account was paused, how long does it take to reactive"
    test4 = "lost card ending 7834 in Denver. need replacement sent to my home address in Boston ASAP"
    test5 = "Can you push a software update to automatically transfer recurring charges to new card numbers like other financial institutions do? This manual process is ridiculous."

    print(classify(test1))
    print(classify(test2))
    print(classify(test3))
    print(classify(test4))
    print(classify(test5))