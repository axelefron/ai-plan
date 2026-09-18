# Día 8 — Notas: APIs, JSON y keys

## 1. ¿Qué es una API?
Un servidor que tiene datos deja una puerta abierta para que otros programas le pidan cosas, en vez de dejarla abierta solo para personas con un navegador. Yo le mando un pedido a una URL y me devuelve datos, sin pantalla ni botones en el medio.

Mi programa hace lo mismo que hace Chrome cuando abro una página: se conecta a un servidor y se baja lo que hay ahí. La diferencia es que lo que baja no está pensado para que lo lea yo, sino para que lo use el código. En Python eso lo hace el paquete
`requests`: `requests.get(url)` es el pedido, y lo que vuelve lo guardo en una variable.

## 2. ¿Qué es JSON y por qué no es un diccionario de Python?
JSON = JavaScript Object Notation. Es un formato de texto para intercambiar datos entre computadoras. Existe porque las dos puntas pueden estar escritas en lenguajes distintos: el servidor de CoinCap no sabe nada de Python, así que me manda texto plano
con una estructura acordada, y de mi lado yo lo traduzco.

Por eso no es un diccionario: se parece a uno (llaves, dos puntos, valores) pero es texto. La traducción es `response.json()` — si fuera ya un diccionario, ese método no haría falta.

La prueba de que son cosas distintas la vi hoy: el precio venía como `"323186.4"`, con comillas. Para JSON eso está bien, es texto. Para Python es un str, y si lo multiplico por 2 me repite el texto en vez de hacer la cuenta. Por eso tuve que pasarlo a `float()`.

## 3. ¿Qué significa un status code 200, 401 y 429?
Son códigos de estado: la respuesta del servidor trae un número que dice cómo le fue al pedido, aparte de los datos.

- **200 — OK.** Salió bien, los datos vienen adjuntos. Es el único caso en que puedo confiar en lo que leo.
- **401 — Unauthorized.** El servidor entendió el pedido pero no me reconoce. Falta la key, está mal escrita, o ya no existe. Es lo que pasaría ahora si usara la key vieja, la que borré.
- **429 — Too Many Requests.** Pedí demasiado. Cada plan tiene un límite; en CoinCap son 500 créditos por mes. Si lo paso, me corta hasta que se renueve. Importa cuando el programa llama a la API dentro de un loop.

La conclusión práctica: que el pedido no reviente no significa que haya salido bien. Puede volver un 401 y yo igual intentar leer `data`, y el error me va a aparecer más adelante, en un lugar que no tiene nada que ver.

## 4. ¿Qué es una API key y por qué nunca va escrita dentro del código?
Es un texto único que el servidor me da para saber que soy yo. Sirve para dos cosas: darme permiso, y contar cuánto uso (y cobrarme si me paso). O sea, es una credencial: quien la tenga puede gastar en mi nombre.

Por eso no va escrita en un `.py` que se commitea. Mi repo `ai-plan` es público, y una key en GitHub la encuentra cualquiera — hay bots que escanean repos buscando exactamente eso.

Lo que hago en cambio:
- La key vive en un archivo `.env`, que no se sube nunca.
- `.env` está listado en `.gitignore`, así que git lo ignora.
- El código la lee con `load_dotenv()` + `os.getenv("COINCAP_API_KEY")`, así el `.py` no contiene el valor.
- Antes de cualquier `git add`, `git status` tiene que NO MOSTRAR `.env`.

Si una key igual se filtra, no alcanza con borrarla del archivo: queda en el historial de commits. Hay que **rotarla** — borrar esa key en el proveedor y crear una nueva. Eso convierte el texto filtrado en basura inútil.

El caso raro de hoy: check50 corre `bitcoin.py` en el servidor de CS50, donde no existe mi `.env`, así que para entregar tuve que hardcodear la key. El procedimiento seguro fue: commitear primero la versión con `.env`, romper el archivo, entregar, `git restore` para
volver a la versión buena, y rotar la key.