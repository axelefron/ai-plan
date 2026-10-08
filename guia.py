# ==========================================================
#  GUÍA PERSONAL — Axel · MacBook Air (macOS, zsh)
#  Actualizada al CERRAR LA SEMANA 5 (8-oct-2026).
#  CS50P completo + API de Claude + evals + TOOLS + error handling.
#
#  PARTE 1 · ENTORNO     terminal, git, venv, secretos
#  PARTE 2 · PYTHON      referencia por concepto
#  PARTE 3 · PATRONES    las formas que se repiten
#  PARTE 4 · MIS ERRORES agrupados por familia + qué significa cada traceback
#  PARTE 5 · RUTINA      cómo encaro algo y cómo cierro el día
#  PARTE 6 · TOOLS       schemas, tool use cycle, multi-tool, encadenamiento
#
#  La PARTE 2 se consulta cuando no me acuerdo cómo se escribe algo.
#  La PARTE 4 se consulta cuando algo no anda. Son momentos distintos.
# ==========================================================


# ##########################################################
#  PARTE 1 · ENTORNO
# ##########################################################

# ----------------------------------------------------------
# 1.1 ¿DÓNDE ESTOY? — la pregunta que más me cuesta
# ----------------------------------------------------------
# El prompt lo dice:
#   (.venv) axelefron@MacBook-Air clasificador %
#    ^^^^^                        ^^^^^^^^^^^  carpeta actual
#      venv activo o no
#
# TODO actúa desde donde estoy parado: python3, check50, pytest,
# git add ., load_dotenv(), y cualquier open("archivo.csv").
#
# LEER LA PALABRA ANTES DEL % antes de correr cualquier cosa.
#
#   pwd            ruta completa
#   ls             qué hay acá
#   cat archivo    contenido REAL en disco (no el del editor sin guardar)
#   cd carpeta / cd .. / cd ~/ai-plan/semana-04      (~ = /Users/axelefron)
#   cd + TAB       autocompleta
#
# cd es para CARPETAS. Un .py no es un comando: lo corre el intérprete.
#   bitcoin.py 4          -> command not found
#   python3 bitcoin.py 4  -> sí
#
# Nombres de archivo: sin espacios, sin mayúsculas, guion_bajo.
# Y CON extensión .py — un archivo "pick_rows-py" corre pero no se importa
# y VS Code no lo trata como Python.

# ----------------------------------------------------------
# 1.2 % vs >>>  Y EL REPL
# ----------------------------------------------------------
# %    = terminal (zsh): ls, cd, python3, git, pytest
# >>>  = estoy DENTRO de Python. cd no existe acá. Salir: exit()
#
# EL REPL ES MI HERRAMIENTA MÁS SUBUSADA. Verifica en 30 segundos
# en vez de adivinar:
#   "1 + 1".split(" ")        ->  ['1', '+', '1']
#   "CS50"[0:2]               ->  'CS'
#   f"{1234567.89:,.4f}"      ->  '1,234,567.8900'
#   dir("")                   ->  TODOS los métodos de string
#   help(random.randint)      ->  cómo se usa, qué devuelve
#
# LAS TRES PREGUNTAS DE UNA LIBRERÍA NUEVA:
#   dir(lib)  ¿qué tiene?   help(x)  ¿cómo se usa?   probarlo  ¿qué devuelve?
#
# Adivinar nombres de métodos fue lo que más tiempo me costó el primer mes.

# ----------------------------------------------------------
# 1.3 MAC Y ATAJOS
# ----------------------------------------------------------
# python3 archivo.py   ·   pip3 install paquete   (nunca python/pip a secas)
#
# VS CODE
#   ⌘+S         guardar      <- la bolita ● tiene que volverse X
#   ⌘+Z/⌘+⇧+Z   deshacer/rehacer
#   ⌘+/         comentar selección   <- para aislar bugs
#   ⌃+`         terminal
#   ⌘+⇧+[       plegar el bloque donde estoy (para strings largos)
#
# TERMINAL
#   ↑      comando anterior        ⌃+U   borrar la línea
#   ⌃+C    cancelar/loop infinito  ⌃+D   cerrar la entrada (EOFError)
#   TAB    autocompletar

# ----------------------------------------------------------
# 1.4 GIT
# ----------------------------------------------------------
#   cd ~/ai-plan
#   git status      <- LEER antes de add. Dice qué ve Git y qué comando usar.
#   git add .       <- "." = esta carpeta HACIA ABAJO
#   git commit -m "dia N: lo que hice"
#   git push
#
# Terminado: desaparece el * de "main*" y las M del Explorer.
#
#   git add      staging. NO guarda nada todavía.
#   git commit   congela la foto. Devuelve un hash.
#   git push     sube. El único que usa internet.
#   git restore <ruta>   reemplaza el archivo por la versión del último
#                        commit. Recupera borrados y deshace cambios.
#
# git restore NO es ⌘+Z. ⌘+Z deshace tecleo y depende del editor.
# restore trae la versión commiteada pase lo que pase.
# Por eso commiteo seguido AUNQUE ESTÉ ROTO: es mi botón de deshacer real.
#
# .gitignore (en la raíz, un patrón por línea, sin espacios adelante):
#   .env
#   __pycache__/
#   .DS_Store
#   .venv/
#
# OJO 1: hay DOS .gitignore posibles. El mío está en la raíz de ai-plan.
#        El de adentro de .venv/ solo se ignora a sí mismo.
# OJO 2: axelefron/ai-plan (mío) y me50/axelefron (CS50) son DOS repos.
#        Un push no entrega nada a CS50.

# ----------------------------------------------------------
# 1.5 INDENTACIÓN = ESTRUCTURA
# ----------------------------------------------------------
# La sangría no es estética: ES la lógica.
# Un else se aparea con el if de LA MISMA sangría. Indentado de más,
# cuelga del if interno y cambia el programa sin dar error.
#
#   for _ in range(10):        <- las 10 vueltas
#       x = ...                <- ADENTRO: valor nuevo cada vuelta
#       for _ in range(3):     <- anidado
#           ...
#       if correcto == False:  <- al nivel del for de 3: corre al terminarlo
#   print(score)               <- sin indentar: al final de todo
#
# Cuando "hace cualquier cosa" pero no tira error: mirar las líneas
# verticales de VS Code antes que la lógica.
#
# Un string de triple comilla SÍ se puede indentar por dentro
# (son espacios en el texto, inofensivos). La línea del `=` no.

# ----------------------------------------------------------
# 1.6 ENTORNOS VIRTUALES (.venv)
# ----------------------------------------------------------
# Un Python APARTE con su propia lista de librerías.
#
#   source /Users/axelefron/ai-plan/.venv/bin/activate    activar
#   deactivate                                            salir
#
# Lo reconozco por el (.venv) adelante del prompt.
# CON el venv, pip3 instala ADENTRO. SIN el venv, en el sistema.
# Son dos listas distintas.
#
# ModuleNotFoundError: No module named 'X'
#   -> lo instalé en un Python y corro con el otro.
#
# Qué va dónde:
#   herramientas de TODAS las carpetas (check50, submit50)  -> global
#   librerías de ESTE proyecto (requests, dotenv, anthropic) -> venv
#
# .venv/ va al .gitignore: miles de archivos que no son míos.
#
# .env  = archivo de texto con mis secretos
# .venv = carpeta con el Python aislado      (nombres parecidos, cosas distintas)

# ----------------------------------------------------------
# 1.7 SECRETOS — API KEYS
# ----------------------------------------------------------
# Una key es una credencial: quien la tenga gasta en mi nombre.
# Mi repo es PÚBLICO y hay bots escaneando GitHub.
#
# EL PATRÓN, SIEMPRE:
#   1. pip3 install python-dotenv       (con el venv activo)
#   2. UN SOLO .env en la raíz de ai-plan (no uno por semana).
#      load_dotenv() lo encuentra subiendo por el árbol desde cualquier
#      carpeta. Una línea por key, sin comillas ni espacios:
#          ANTHROPIC_API_KEY=sk-ant-...
#   3. .env listado en .gitignore
#   4. en el código:
#          from dotenv import load_dotenv
#          import os
#          load_dotenv()
#          mi_key = os.getenv("ANTHROPIC_API_KEY")
#      (El SDK de Anthropic la lee del entorno solo: alcanza con
#       load_dotenv() antes de crear el cliente.)
#   5. ANTES de cualquier git add: git status NO debe mostrar .env
#
# Si getenv devuelve None -> el .env no se encontró (carpeta o typo).
#
# SI ALGO ME OBLIGA A HARDCODEAR (check50 corre en el server de CS50,
# sin mi .env):
#   1. commitear primero la versión segura
#   2. romper el archivo    3. check50 + submit50
#   4. git restore <archivo>        <- NO es opcional
#   5. rotar la key en el proveedor
#
# Borrarla del archivo no alcanza: queda en el historial de commits.
# Rotarla es lo que convierte el texto filtrado en basura.


# ##########################################################
#  PARTE 2 · PYTHON — REFERENCIA
# ##########################################################

# ----------------------------------------------------------
# 2.1 FUNCIÓN vs MÉTODO
# ----------------------------------------------------------
# función -> el valor va ADENTRO:   len(texto)   abs(-10)   int("5")
# método  -> va PEGADO con punto:   texto.strip()
#
# Los métodos son DE UN TIPO. La mayoría NO modifica el original:
# DEVUELVEN algo nuevo.
#   texto.strip()          calcula y tira
#   texto = texto.strip()  lo guarda
#
# LA EXCEPCIÓN: los métodos de LISTA modifican en el lugar y devuelven None.
#   x = lista.append(algo)   -> x vale None
#   lista.append(algo)       -> así, sin asignar
#
# Encadenar: cada método opera sobre el resultado del anterior.
# EL ORDEN IMPORTA: strip ANTES que replace.
# Los corchetes se encadenan igual: dic["data"]["priceUsd"]

# ----------------------------------------------------------
# 2.2 TIPOS Y CONVERSIÓN
# ----------------------------------------------------------
# input() SIEMPRE devuelve str. "42" y 42 nunca son iguales.
#
#   int(x) float(x) str(x) type(x) abs(x) len(x) round(x, n)
#
# LO QUE LLEGA DE AFUERA CASI SIEMPRE ES TEXTO:
#   input()  ·  sys.argv[1]  ·  un valor de un JSON (puede ser "323186.4")
#   "123" * 2 -> "123123"   (repite, no multiplica)
#
# CONVERTIR UNO POR UNO, no la colección entera:
#   float(sys.argv)     explota (es la lista)
#   float(sys.argv[1])  sí

# ----------------------------------------------------------
# 2.3 STRINGS — MÉTODOS
# ----------------------------------------------------------
# NORMALIZAR (antes de comparar)
#   .strip()  extremos (NO el medio)   .lower()  .upper()
#   .casefold()  como lower pero más agresivo
#   .title()  Cada Palabra     .capitalize()  Solo la primera
#   OJO: .title() CAMBIA el original. Si hay que conservar el caso, rompe.
#
# PREGUNTAR (devuelven True/False — van DIRECTO en el if, sin "== True")
#   .isalpha() .isdigit() .isalnum() .isupper() .islower()
#   .startswith("h")  .endswith(".py")
#
#   NO EXISTE .isfloat(). "¿esto se puede convertir?" NO se pregunta
#   con un if: se INTENTA adentro de un try.
#
# TRANSFORMAR
#   .replace(viejo, nuevo)   .count("a")
#   .split(sep)     parte y devuelve una LISTA
#   " ".join(lista) une — es método del SEPARADOR, no de la lista
#
#   .split() recibe UN separador. El segundo argumento es un NÚMERO
#   (cuántos cortes). Para partir por dos cosas: dos pasos.
#   Y si el separador deja espacios pegados, incluirlos en el separador:
#   "Bell, Katie".split(", ")  mejor que .split(",") + .strip()

# ----------------------------------------------------------
# 2.4 POSICIONES Y RANGOS — LA DERECHA SE EXCLUYE
# ----------------------------------------------------------
#   s[0]   primero (empieza en CERO)   s[-1]  último
#   s[0:2] desde 0 HASTA 2 SIN INCLUIRLO -> los dos primeros
#
# LA MISMA REGLA EN TODOS LADOS:
#   range(3)                -> 0,1,2        (tres vueltas)
#   range(1, 3)             -> 1,2          (DOS vueltas)
#   random.randrange(1, 11) -> 1 a 10
#   random.randint(1, 10)   -> 1 a 10       (este SÍ incluye los dos)
#   lista[0:3]              -> los 3 primeros
#
# Para incluir el tope: randint, o randrange(1, tope + 1).

# ----------------------------------------------------------
# 2.5 F-STRINGS
# ----------------------------------------------------------
#   f"Total: {percent:,.4f}%"
#    │       │       │     └─ afuera de {} = texto literal
#    │       │       └─────── ADENTRO: dos puntos + formato
#    │       └─────────────── la expresión (puede ser una llamada)
#    └─────────────────────── la f que activa las llaves
#
# REGLA: adentro de {} se calcula, afuera se imprime tal cual.
#
# FORMATOS (todos después de ":")
#   .1f .2f      decimales          .6f   para números muy chicos
#   ,            miles              ,.4f  las dos: 323,186.4000
#   .0%          0.47 -> "47%"      :10   rellena a 10 chars (alinea columnas)
#
# \n = salto de línea. Sirve cuando el cursor quedó pegado al prompt de
# un input() que nunca recibió Enter (Ctrl-D): f"\nAdieu, adieu, a..."
#
# LAS LLAVES SOLO SIGNIFICAN "INSERTÁ ACÁ" ADENTRO DE UNA f-STRING:
#   print(f"{x}")   -> el valor de x
#   print({x})      -> un SET con x adentro -> imprime {20}
#
# Adentro de una f-string con comillas dobles, las claves de un dict
# van con comillas SIMPLES:  f"{m['field']}"
#
# LOS FLOATS MIENTEN: 0.07 * 100 -> 7.000000000000001
# Y solo con algunos números -> probar con un caso no alcanza.
# REGLA: todo número calculado que se MUESTRA, va formateado.

# ----------------------------------------------------------
# 2.6 print()
# ----------------------------------------------------------
#   print(a, b)          separa con espacio
#   print(a, b, sep="_") el sep va ENTRE los argumentos
#   print("x", end="")   no salta de línea
#   print()              línea vacía
#
# print() NO DEVUELVE NADA.
#   print(x).lower()  ->  AttributeError: 'NoneType'
#
# print(input(...)) imprime y tira. Si quiero la respuesta, la GUARDO.
#
# UNA EXPRESIÓN SOLA NO IMPRIME NADA en un .py.
#   message.content[0].text        <- calcula y tira
#   print(message.content[0].text) <- sí
# En un notebook o en el REPL la última línea se muestra sola. Eso es
# una comodidad de esa herramienta, no de Python.

# ----------------------------------------------------------
# 2.7 FUNCIONES
# ----------------------------------------------------------
# def NO EJECUTA NADA. Define. Nada corre hasta que alguien llama.
#
# El parámetro recibe su valor EN LA LLAMADA. Adentro trabajo con el
# PARÁMETRO, nunca con el nombre de la función ni con variables de otra.
#
# SI LA FUNCIÓN RECIBE UN DATO, NO LE PIDO input() ADENTRO.
# Pisa el parámetro y cuelga los tests (el test no tipea nada).
#
# LLAMAR ES UNA CALCULADORA:
#   resultado = convert(dato)
#      ↑          ↑       ↑
#   guardo     la llamo  le doy el dato
# Sin el "resultado =" el valor se pierde.
#
# EL "=" SE LEE DE DERECHA A IZQUIERDA. El nombre NUEVO va a la izquierda.
#   convert(dato) = nombre   -> SyntaxError: cannot assign to function call
#
# return TERMINA LA FUNCIÓN EN EL ACTO. Nunca adentro de un loop que
# quiero que dé todas las vueltas. No lleva paréntesis.
#
# Para salir de un while de validación DENTRO de una función: return,
# no break. return sale del loop Y de la función, entregando el valor.
#
# return -> devuelve el valor a quien llamó (para el programa)
# print  -> muestra en pantalla (para el usuario)
# Una función que imprime es una caja negra: NO SE PUEDE TESTEAR.
#
# PARÁMETROS OPCIONALES — el patrón params + if:
#   Cuando la API no acepta None, no alcanza con poner el parámetro
#   en la firma: hay que decidir si la clave ENTRA al diccionario.
#
#     def chat(messages, system=None, stop_sequences=None):
#         params = {                    <- SOLO lo obligatorio
#             "model": model,
#             "max_tokens": 8000,
#             "messages": messages,
#         }
#         if system:
#             params["system"] = system
#         if stop_sequences:
#             params["stop_sequences"] = stop_sequences
#         return client.messages.create(**params)
#
#   ** desarma el diccionario en argumentos con nombre:
#   {"model": x, "max_tokens": y}  ->  model=x, max_tokens=y
#
#   CLAVE: las opcionales NO van en el dict inicial. Si están ahí,
#   el if no agrega nada y se manda None igual.
#
# VALOR POR DEFECTO MUTABLE — no usar:
#   def f(lista=[]):     <- el default se crea UNA vez, se comparte
#   def f(lista=None):   <- así, y se decide adentro
#
# SCOPE: cada función solo conoce sus parámetros y lo que crea.
# Un contador creado en main() no se suma desde otra función.

# ----------------------------------------------------------
# 2.8 LA FUNCIÓN TESTEABLE — main() + auxiliares
# ----------------------------------------------------------
#   funcion_logica  recibe, transforma, RETURN. No pide, no imprime.
#   main()          pide input, la llama, IMPRIME.
#
# Para poder MEDIR algo, ese algo tiene que DEVOLVER un valor.
#
# LA PRESENTACIÓN VA EN main(), NO EN LA FUNCIÓN:
#   shorten devuelve "Twttr", NO "Output: Twttr"
#   value devuelve 0, NO "$0"
#   Si la función devuelve texto decorado, el test nunca matchea.
#
# LA NORMALIZACIÓN (.strip().casefold()) VA ADENTRO DE LA FUNCIÓN.
#   Si está en main(), la función solo anda cuando la llaman "bien
#   preparada". El test le manda el dato crudo y falla.
#   Una función testeable se hace cargo de su propio input.
#
# Este patrón es el mismo que necesité para medir el clasificador:
# la parte que decide devuelve un dato, otra capa lo muestra.

# ----------------------------------------------------------
# 2.9 if __name__ == "__main__":
# ----------------------------------------------------------
#   if __name__ == "__main__":
#       <los tests, o main()>
#
# Separa lo que un archivo OFRECE (funciones) de lo que HACE al ejecutarlo.
#   python3 classifier.py            -> corre lo del if
#   from classifier import classify  -> define todo, NO corre el if
#
# Python le pone a cada archivo una variable __name__: vale "__main__"
# al ejecutarlo directo, y el nombre del módulo al importarlo.
#
# IMPORTAR UN ARCHIVO LO EJECUTA ENTERO, de arriba a abajo. Sin esta
# guarda, cada import dispara las llamadas a la API que el archivo tenga
# sueltas. Se paga en tokens.

# ----------------------------------------------------------
# 2.10 DECIDIR Y COMPARAR
# ----------------------------------------------------------
# ==  !=  <  >  <=  >=   ·   and  or  not
#
# LOS TRES QUE SE CONFUNDEN:
#   is / is not    ¿son EL MISMO OBJETO?  casi nunca es lo que quiero
#   == / !=        ¿valen LO MISMO?
#   in / not in    ¿está CONTENIDO en?
#
#   letra not in "aeiou"   sí      letra is not "aeiou"   SIEMPRE True
#
# in funciona sobre string, lista y dict (en el dict busca CLAVES).
#   if level in [1, 2, 3]:    mejor que dos comparaciones
#
# CADA LADO DEL or/and TIENE QUE SER UNA COMPARACIÓN COMPLETA:
#   if x == 5 or x == 10:    sí
#   if x == 5 or 10:         MAL — siempre True, no avisa
#   if x in [5, 10, 25]:     mejor
#
# NO COMPARAR CONTRA UN TIPO NI CONTRA UNA CLASE DE ERROR:
#   shorten("w") != int       siempre True, no prueba nada
#   elif FileNotFoundError:   siempre True
#   El nombre de un error va después de except, o en pytest.raises.
#   No se PREGUNTA si algo va a fallar: se intenta.
#
# ENCADENADA: 7 <= t <= 8   ("entre 7 y 8", los dos signos igual)
#
# if/elif/else SE DETIENE en la primera verdadera.
#   -> ordenar de lo MÁS ESPECÍFICO a lo general.
#      startswith("hello") ANTES que startswith("h").
#   Con ifs sueltos Python evalúa todos. Si son excluyentes, elif.

# ----------------------------------------------------------
# 2.11 LOOPS
# ----------------------------------------------------------
# for    recorrer algo que YA TENGO, o repetir N veces conocidas
# while  repetir MIENTRAS una condición sea verdadera
#
#   for c in s:                     cada carácter
#   for _ in range(3):              3 vueltas, no me importa el número
#   for i, x in enumerate(l, start=1):   índice Y elemento juntos
#
# EL NOMBRE DESPUÉS DEL for ES DEL LOOP. Si uso una variable que ya
# tenía, la pierdo:  for result in range(3):  <- pisa mi variable
#
# WHILE — LA REGLA DE ORO
#   1. La variable de la condición nace ANTES del loop.
#   2. Adentro, algo LA MODIFICA.
#   3. Si no, es infinito. Se corta con ⌃+C.
#   Corolario: si lo que se repite es PREGUNTAR, el input() va ADENTRO.
#
# DOS FASES = DOS LOOPS, uno abajo del otro. Meterlos en el mismo hace
# que vuelva a preguntar lo primero cada vuelta.
#
# LAS TRES PALABRAS QUE SE CONFUNDEN:
#   pass      "acá no hago nada"       -> SIGUE con la línea de abajo
#   continue  "abandono esta vuelta"   -> salta al principio del loop
#   break     "abandono el loop"
#
#   Un pass donde va un continue deja que el código siga bajando y
#   ejecute lo que yo quería saltear. Bug silencioso.
#   En un while True, volver arriba es NO hacer nada: no hay que escribirlo.
#
# += 1  es  = x + 1   (con strings pega, con listas extiende)

# ----------------------------------------------------------
# 2.12 LISTAS
# ----------------------------------------------------------
#   lista[0]  ·  lista[0:3]  ·  len(lista)  ·  x in lista
#
#   lista.append(x)   agrega EL OBJETO. Modifica, devuelve None.
#   lista.extend(l2)  recorre l2 y agrega CADA COSA de adentro.
#
#   batch = ["a","b","c"]
#     .append(batch) -> [["a","b","c"]]   1 elemento
#     .extend(batch) -> ["a","b","c"]     3 elementos
#   Acumulando 10 llamadas de 20 items: append da len 10, extend da 200.
#
#   " ".join(lista)   une — método del SEPARADOR, no de la lista
#   sorted(l)         copia ordenada (no modifica). sorted(l, reverse=True)
#
# LIST COMPREHENSION — un for compacto:
#   todos = [row["text"] for row in reader]
#   equivale a crear la lista vacía y hacer append en un for.
#   Las dos están bien; el for normal es más fácil de depurar.
#
# print(lista) imprime con corchetes y comillas. for x in lista: uno por línea.

# ----------------------------------------------------------
# 2.13 DICCIONARIOS
# ----------------------------------------------------------
# Pares CLAVE : VALOR. Se buscan por clave, no por posición.
#
#   fruits["Apple"]     -> 130      CORCHETES, no paréntesis
#   fruits("Apple")     -> TypeError: not callable
#   fruits["Mango"]     -> KeyError (explota)
#   "Apple" in fruits   -> True     (pregunta por CLAVES)
#   fruits.get("Mango") -> None     (no explota)
#   dic["clave"] = x    -> agrega o pisa. Así agrego una clave nueva
#                          a un dict que ya existe.
#
# ANIDADOS (lo que devuelve una API):
#   respuesta["data"]["priceUsd"]
#   Cada corchete se cierra antes de abrir el siguiente. Si me quedo
#   un nivel corto, obtengo el dict de adentro.
#   -> print() del diccionario ENTERO antes de escribir la navegación.
#
# LISTA DE DICCIONARIOS — cada item con varios atributos:
#   for amigo in amigos: print(amigo["name"])
#   Es un dataframe. El dict plano es un VLOOKUP.
#
# DICCIONARIO COMO ÍNDICE — para cruzar dos colecciones:
#   Mal: por cada fila de A, recorrer todo B buscando la que coincide.
#        20x20 = 400 comparaciones. 200x200 = 40.000.
#   Bien: recorrer B UNA vez y armar clave -> fila.
#
#     indice = {}
#     for row in reader:
#         indice[row["text"]] = row
#     ...
#     fila_b = indice[texto]        <- búsqueda directa
#
#   Es el índice de un libro. Reconocer la situación: "voy a buscar
#   muchas veces por una clave" -> armá un dict.
#
#   Y SIEMPRE con guarda, porque la clave puede no estar:
#     if clave not in indice:
#         print(f"NOT FOUND: {clave[:60]}")
#         continue
#
# Una TUPLA (a, b) puede ser clave de un diccionario porque es inmutable.
# Una lista no.
#
# None = "no hay valor". No es 0 ni "" ni False.

# ----------------------------------------------------------
# 2.14 TRY / EXCEPT
# ----------------------------------------------------------
#   try:     <lo que puede romperse>
#   except <TipoDeError>:    <qué hacer con ESE error>
#   else:    <corre SOLO si no hubo excepción>
#
# EL try PROTEGE SOLO LAS LÍNEAS INDENTADAS ADENTRO. Si la línea que
# puede romper quedó afuera, el programa revienta igual.
# Y envolver de más hace que atrape cosas que quería manejar distinto.
#
# VARIOS ERRORES EN UN except: un solo paréntesis, coma en el medio.
#   except (ValueError, IndexError):     sí
#   except (ValueError) (IndexError):    SyntaxError
#
# VARIOS except, UNO POR ERROR, cada uno con SU reacción:
#   except KeyError:   pass     <- item inválido: ignorar
#   except EOFError:   break    <- Ctrl-D: salir
#
# Python usa el PRIMER except que coincida. Meter todo en uno solo les
# da a todos la misma reacción.
#
# UN except QUE HACE pass SOBRE UN ERROR REAL ESCONDE LA CAUSA: después
# explota en otro lado y el traceback apunta a la línea equivocada.
# Para lo que no puedo manejar: sys.exit("mensaje").
#
# except Exception as e:  atrapa cualquier cosa y e dice cuál fue.
#   Ancho de más para producción, pero correcto en un loop largo donde
#   lo que importa es NO FRENAR:
#     except Exception as e:
#         print(f"Row {i} failed: {e}")
#         continue

# ----------------------------------------------------------
# 2.15 try/except vs if
# ----------------------------------------------------------
# try/except  atrapa lo que ROMPE.
#     "cat" -> ValueError   ·   sys.argv[1] faltante -> IndexError
# if          maneja lo que ANDA PERO NO SIRVE.
#     "4/3" es un número válido pero el enunciado lo rechaza
#     "-5" es perfecto pero un guess negativo no vale
#     len(sys.argv) < 2 se cuenta ANTES de leer el índice
#
# AL VALIDAR UN RANGO, MIRAR LOS DOS EXTREMOS.

# ----------------------------------------------------------
# 2.16 ERRORES COMO SEÑAL
# ----------------------------------------------------------
# EOFError = Ctrl-D = "no hay más entrada". No es falla del usuario:
# es cómo se avisa que terminó. Se atrapa y se sale con break.
# Ctrl-C = KeyboardInterrupt = cancelar el programa.
#
# Al cortar con Ctrl-D el prompt del input() ya se imprimió y nunca
# recibió Enter: mi salida sale pegada. Por eso el "\n" del print final.

# ----------------------------------------------------------
# 2.17 LIBRERÍAS, MÓDULOS Y PAQUETES
# ----------------------------------------------------------
# módulo = un .py con funciones reutilizables
# paquete = módulos en una carpeta
# librería estándar = viene con Python (random, sys, json, os, csv, collections)
# terceros = hay que instalarlos (requests, pytest, anthropic, dotenv)
#
# pip3 instala desde PyPI (pypi.org). npm es el equivalente de JS.
#
#   import random              -> random.choice(...)
#   from random import choice  -> choice(...)
# La segunda es la que uso para mis propios archivos:
#   from classifier import classify
#
# YA USADAS:
#   random.choice / randint(a,b) incluye ambos / randrange(a,b) excluye b
#   random.sample(lista, n)   n elementos SIN repetir
#   random.shuffle(lista)     mezcla EN EL LUGAR
#   random.seed(42)           fija la secuencia pseudo-aleatoria
#   statistics.mean(lista)
#   json.dumps(obj, indent=2) imprime un JSON legible
#   collections.Counter(secuencia)  cuenta apariciones -> .most_common()
#
# random.seed(): Python genera PSEUDO-azar, una fórmula con un valor
# inicial. Misma semilla -> misma secuencia, siempre. Sin seed usa la
# hora del sistema. El 42 es arbitrario; lo que importa es que esté FIJO,
# para que regenerar un archivo no me haga perder el trabajo hecho encima
# y para que el experimento sea reproducible.
#
# KEYWORD ARGUMENTS: argumentos con nombre, no dependen del orden.
#   print(a, b, sep="_")   ·   enumerate(lista, start=1)

# ----------------------------------------------------------
# 2.18 sys.argv
# ----------------------------------------------------------
#   python3 bitcoin.py 2.5
#   sys.argv[0] -> "bitcoin.py"    sys.argv[1] -> "2.5"    (strings)
#
# len(sys.argv) CUENTA el nombre del archivo: 1 argumento -> len == 2
#
# ORDEN DE LAS VALIDACIONES:
#   1. ¿existe?  if len(sys.argv) < 2    <- ANTES de leer [1]
#   2. ¿sirve?   try: float(sys.argv[1])
# Al revés, el IndexError revienta antes del chequeo.
#
# sys.exit("mensaje")  imprime y termina.

# ----------------------------------------------------------
# 2.19 APIs, requests Y JSON
# ----------------------------------------------------------
# API = puerta que un servidor deja abierta para que otros PROGRAMAS
# le pidan datos. Lo que vuelve no está pensado para que lo lea yo.
#
#   respuesta = requests.get("https://...")
#
# LA URL ES UN STRING, con https:// adelante (sin esquema -> MissingSchema).
#
# Lo que devuelve get() es un OBJETO Response, NO un diccionario:
#   respuesta["clave"]       -> TypeError: not subscriptable
#   datos = respuesta.json() -> ESTO sí es un diccionario
#
# JSON = formato de TEXTO para intercambiar datos entre máquinas que no
# comparten lenguaje. Se PARECE a un dict pero es texto: por eso existe
# .json(), y por eso un número puede llegar como "323186.4" con comillas.
#
# CÓDIGOS: 200 OK · 401 key mal/ausente · 429 pasé el límite
# Que el pedido no reviente NO significa que salió bien.
#
# EL FLUJO:
#   1. validar el argumento
#   2. try: requests.get(url) / except RequestException: sys.exit(...)
#   3. datos = respuesta.json()
#   4. print(datos) para VER la estructura antes de navegarla
#   5. corchetes encadenados  6. convertir  7. formatear
#
# Para explorar un JSON sin código: pegar la URL en el navegador.

# ----------------------------------------------------------
# 2.20 UNIT TESTS Y pytest
# ----------------------------------------------------------
# Un test es "dado ESTE input, espero ESTE output".
#
#   assert shorten("Twitter") == "Twttr"
#   Si es True no pasa nada. Si es False -> AssertionError.
#
# pytest corre todas las funciones que empiezan con test_ y da un reporte.
#   pytest test_archivo.py
#
#   from twttr import shorten
#
#   def test_minusculas():
#       assert shorten("twitter") == "twttr"
#   def test_mayusculas():
#       assert shorten("TWITTER") == "TWTTR"
#
# UN CASO POR FUNCIÓN. Todos los asserts juntos: el primer fallo corta.
#
# UN TEST TIENE QUE PODER FALLAR.
#   assert shorten("word").isalpha()   pasa aunque la función no haga nada
#   assert shorten("word") != int      SIEMPRE True
#   Si no hay un == contra un valor que escribí YO, no estoy midiendo.
#
#   with pytest.raises(TypeError):     para verificar que algo LANZA error
#       shorten(5)
#
# CUANDO UN TEST FALLA PUEDE SER EL CÓDIGO **O MI EXPECTATIVA**.
#   Escribí "MRclg", lo correcto era "MRclG". El rojo era mío.
#
# check50 de un test corre MIS TESTS contra versiones rotas a propósito
# y verifica que las detecten. Un test flojo sale en rojo ahí.

# ----------------------------------------------------------
# 2.21 ARCHIVOS — open, with Y CSV
# ----------------------------------------------------------
# Una lista vive en la MEMORIA y se borra al terminar. Un archivo queda
# en disco. Eso es persistencia.
#
#   with open(ruta, modo) as f:
#       <trabajo con f>
#   <acá YA ESTÁ CERRADO>
#
# El with cierra solo al salir, incluso si algo explota. Siempre with.
#
# MODOS:  "r" leer (default, falta -> FileNotFoundError)
#         "w" escribir DESDE CERO — si existe, LO VACÍA
#         "a" append al final
# Elegir mal el modo es destructivo.
#
# LEER TEXTO:
#   for line in f:        línea por línea — lo normal
#   f.readlines()         todo a una lista de una (memoria de más)
#   acumular en lista     cuando necesito todo junto para ordenar/contar
#
#   Cada línea trae el "\n" pegado -> .rstrip()
#   f.write(texto)  escribe. El "\n" lo pongo YO.
#
# BINARIOS (imágenes, audio, video): bytes crudos. Se abren con librerías
# que saben interpretarlos (pillow para imágenes). open pelado no sirve.
#
# CSV — dos familias:
#   csv.reader / csv.writer          trabajan con LISTAS (por posición)
#   csv.DictReader / csv.DictWriter  trabajan con DICTS (por nombre)
#   La versión Dict es más legible: row["house"] en vez de row[1].
#
#   reader = csv.DictReader(f)
#       Usa la PRIMERA FILA como nombres de columna.
#       Pasarle fieldnames= es decirle "este archivo NO tiene encabezado".
#       El reader SE CONSUME: para recorrerlo varias veces, list(reader)
#       ADENTRO del with.
#
#   writer = csv.writer(f)
#       writer.writerow(["text"])      <- el encabezado, A MANO, una vez
#       writer.writerow([valor])       <- UNA LISTA de celdas
#       Si le paso el string pelado, lo trata como secuencia de caracteres
#       y escribe una letra por columna.
#       fieldnames NO es parámetro de csv.writer.
#
#   writer = csv.DictWriter(f, fieldnames=[...])
#       fieldnames van acá, UNA vez. Definen el ORDEN de las columnas
#       (manda esto, no el orden de las claves del dict).
#       writer.writeheader()     la fila de títulos. SIN "=".
#       writer.writerow({...})   un diccionario. SIN "=".
#
#   writeheader() y writerow() no devuelven nada útil. Asignarlas
#   (writer = writer.writeheader()) destruye el writer. Igual que .append().
#
#   Al escribir: open(ruta, "w", newline="")
#
# EL PATRÓN "TRANSFORMAR UN ARCHIVO" (scourgify):
#   DOS archivos, DOS bloques secuenciales, no uno anidado.
#   1. abrir ENTRADA (sys.argv[1]), recorrer, armar una lista limpia
#   2. abrir SALIDA (sys.argv[2]) en "w", escribir encabezado + lista
#   1 = entrada, 2 = salida. SIEMPRE.


# ##########################################################
#  PARTE 3 · PATRONES QUE SE REPITEN
# ##########################################################

# ----------------------------------------------------------
# 3.1 EL ACUMULADOR
# ----------------------------------------------------------
#   resultado = ""              <- AFUERA del loop. Nace vacío.
#   for letra in palabra:
#       resultado += algo       <- ADENTRO. Crece cada vuelta.
#   print(resultado)            <- AFUERA. UN solo print.
#
# Si nace ADENTRO, se reinicia cada vuelta.
# El VALOR INICIAL define el tipo: "" acumula texto, 0 cuenta, [] junta.
#
# EL ERROR QUE MÁS ME COSTÓ: print() adentro del loop.
# El if NO decide qué imprimir -> decide QUÉ AGREGAR a la variable.

# ----------------------------------------------------------
# 3.2 LA BANDERA
# ----------------------------------------------------------
# Una booleana que RECUERDA algo del loop para usarlo DESPUÉS.
#
#   correcto = False            <- afuera
#   for _ in range(3):
#       if acertó:
#           correcto = True
#           break
#   if correcto == False:       <- al salir, sé POR QUÉ salí
#
# Un loop no me dice si terminó por éxito o por agotarse.
# Una bandera que se prende pero nunca se consulta no sirve.

# ----------------------------------------------------------
# 3.3 "BUSCÁ EL FALLO"
# ----------------------------------------------------------
# Cuando TODAS las condiciones deben cumplirse:
#   if <regla 1 falla>: return False
#   if <regla 2 falla>: return False
#   return True            <- solo se alcanza si sobrevivió todo
#
# Cada if describe el CASO MALO y sale temprano. UN SOLO return True.
# Al revés, alcanza con cumplir UNA sola regla.
#
# Y una regla NO es un valor con el que comparar: es una PREGUNTA.
# s.isalnum() YA ES la respuesta.

# ----------------------------------------------------------
# 3.4 NORMALIZAR PARA COMPARAR, NO PARA GUARDAR
# ----------------------------------------------------------
#   if letter.lower() not in "aeiou":
#       resultado += letter     <- la letra ORIGINAL
#
# Y NORMALIZAR LOS DOS LADOS del ==.
# La normalización va donde el dato ENTRA a la función que lo usa.

# ----------------------------------------------------------
# 3.5 EL DATO DEL USUARIO NO ES UNA INSTRUCCIÓN
# ----------------------------------------------------------
# Si escribe "+", eso es el TEXTO "+" en una variable. Python no lo
# ejecuta. Yo tengo que MIRARLO con un if y decidir.
#
# Lo mismo con el texto que le paso a un LLM: encerrarlo en etiquetas
# <message>...</message> le marca al modelo dónde empieza y termina el
# DATO, para que algo que parezca una orden adentro no se tome como
# instrucción mía. Es seguridad, no estética.

# ----------------------------------------------------------
# 3.6 EL PROGRAMA EN FASES
# ----------------------------------------------------------
#   FASE 1   while True: pedir y validar el setup -> break/return
#   UNA VEZ  lo que se decide una sola vez (el número secreto)
#   FASE 2   while/for: el ciclo principal
#
# Lo que se sortea o calcula UNA VEZ va AFUERA del loop principal.
# Adentro se re-hace cada vuelta y el objetivo cambia solo.

# ----------------------------------------------------------
# 3.7 CRUZAR DOS ARCHIVOS POR UNA COLUMNA
# ----------------------------------------------------------
#   1. leer el archivo A como lista de dicts
#   2. leer B como DICCIONARIO indexado por la columna común (ver 2.13)
#   3. recorrer A, buscar en el índice, comparar
#
# REGLA: el texto de la columna que une los dos archivos tiene que venir
# de la MISMA FUENTE. Copiarlo a mano desde una terminal, una captura o
# una versión vieja garantiza que algo no coincida — y falla en silencio
# o con un KeyError que no explica la causa.

# ----------------------------------------------------------
# 3.8 MEDIR ANTES DE MEJORAR (evals)
# ----------------------------------------------------------
# Que "corra sin errores" NO significa que "funcione". Un try/except que
# no salta y un CSV bien escrito no dicen nada sobre si el contenido
# es correcto.
#
# Para saberlo: un conjunto de casos donde YO sé la respuesta correcta.
# Misma idea que un unit test, pero el resultado esperado no se calcula:
# lo decido yo.
#
# EL ORDEN, Y NO SE SALTEA NINGUNO:
#   1. Escribir las reglas de decisión ANTES de etiquetar.
#      Si no, la fila 3 y la 17 —que son el mismo caso— salen distinto,
#      y después no sé si el error es del modelo o mío.
#   2. Etiquetar SIN mirar lo que dijo el modelo (sesgo de anclaje).
#   3. Elegir casos difíciles a propósito, no solo al azar.
#   4. MEDIR EL RUIDO: re-correr sin cambiar nada.
#   5. UN experimento por vez, anotando qué cambié y qué pasó.
#   6. Leer los desacuerdos, no solo el porcentaje. El número dice
#      CUÁNTO; la lista dice QUÉ arreglar.
#   7. Reportar el número CON su margen.
#
# QUÉ SE PUEDE EVALUAR CON == :
#   valor de lista cerrada  -> sí. Binario, contable.
#   texto libre             -> NO.
#     "Customer lost card, needs replacement"
#     "Customer needs a replacement card after losing theirs"
#     significan lo mismo y == dice False -> 0/20 sin que nada esté mal.
#   Para texto libre: model-based grading (un modelo como juez).
#   Mientras tanto: medir lo medible y ser EXPLÍCITO sobre lo que quedó
#   sin medir.

# ----------------------------------------------------------
# 3.9 RUIDO vs SEÑAL
# ----------------------------------------------------------
# Un LLM no es determinístico: mismo input puede dar distinto output.
#
# Corrí la misma eval dos veces SIN CAMBIAR NADA:
#   corrida 1: category 15/20 · sentiment 14/20 · priority 15/20
#   corrida 2: category 15/20 · sentiment 14/20 · priority 17/20
#
# priority se movió +2 solo. Entonces cualquier cambio que la mueva
# menos de 2 puntos NO PRUEBA NADA.
#
# Sin medir el ruido primero, confundo azar con mejora, anoto "funcionó",
# y construyo encima de una conclusión falsa.
#
# COROLARIO: el campo más ruidoso era el peor definido.
# Criterio vago -> el modelo duda -> el azar decide.
# Si un número varía mucho, antes de buscar un modelo mejor, revisar
# si mi definición es ambigua.

# ----------------------------------------------------------
# 3.10 EL MODELO NO FALLA, LE FALTA MI INFORMACIÓN
# ----------------------------------------------------------
# 3 de mis 5 errores de categoría eran una regla que YO tenía escrita
# en el README y nunca puse en el system prompt. La copié -> los 3
# errores desaparecieron. +3 puntos.
#
# Reflejo natural: "este modelo es malo, probemos uno más grande".
# Pregunta más barata: "¿le dije lo que yo sé?"
# La brecha entre lo que yo sé y lo que el prompt dice es el primer
# lugar donde mirar, y es gratis de arreglar.
#
# Y AL REVÉS: MI GROUND TRUTH TAMBIÉN SE EQUIVOCA.
# El modelo devolvió "positive" sobre un mensaje que termina en
# "Thank you." Mi propia definición decía positive = thanks. Tenía razón
# él. Las evals no son un examen donde el modelo rinde y yo corrijo:
# son dos criterios comparándose. Por eso los sets se REVISAN.
#
# UN EJEMPLO EN UN PROMPT ES UNA INVITACIÓN A COPIARLO.
#   Puse "like the card ending in 4412" -> el modelo generó mensajes
#   con 4412. Puse "refer to it as 'the card ending in XXXX'" -> unos
#   copiaron los dígitos reales y otros escribieron XXXX literal.
#   Para prohibir algo: decir qué NO hacer, sin dar una frase rellenable.

# ----------------------------------------------------------
# 3.11 MEDIR EL COSTO
# ----------------------------------------------------------
# El objeto de client.messages.create() trae .usage con input_tokens
# y output_tokens.
#
# OJO: una función que hace "return message.content[0].text" DESCARTA
# el usage. Para medirlo hay que guardar el objeto entero.
#
#   costo = (usage.input_tokens  / 1_000_000) * precio_input
#         + (usage.output_tokens / 1_000_000) * precio_output
#
# Los precios son por MILLÓN y son DOS distintos. El de salida suele
# ser varias veces el de entrada.
#
# NO hardcodear los números de tokens: usar usage.input_tokens, si no
# quedo midiendo una versión vieja del prompt.
#
# MI CASO (Haiku 4.5, oct-2026): 464 entrada + 53 salida por mensaje
#   $0,00073 por mensaje · $0,15 los 200 · $73 los 100.000
#
# LO QUE REVELA LA CUENTA:
#   - ~86% de los tokens de entrada son el system prompt, reenviado
#     en CADA llamada.
#   - La salida es el 10% de los tokens pero el 37% del costo (vale 5x).
#
# PALANCAS (identificadas, no implementadas):
#   prompt caching  Haiku 4.5 pide un mínimo de 4.096 tokens cacheables.
#                   Mi prompt tiene ~400: no califica. Serviría si crece.
#   Batch API       encaja: nadie espera un clasificador que corre sobre
#                   un CSV.
#   sacar el summary  bajaría ~1/3 del costo, gratis, si no se necesita.
#
# A $73 por 100.000 no vale la pena optimizar todavía. Pero saber que
# las palancas existen y cuánto mueven vale cuando un cliente pregunta.


# ##########################################################
#  PARTE 4 · MIS ERRORES
# ##########################################################

# ----------------------------------------------------------
# 4.1 LAS FAMILIAS (buscar por tipo, no por número)
# ----------------------------------------------------------
#
# ===== A · NO LO CORRÍ / NO LO GUARDÉ =====================
# A1. Inventar sintaxis y no probarla.
#     .isnum, .isfloat, .add, len(6), figlet.random, lista.join()
#     Escribo 15 líneas sobre algo que nunca corrió. -> REPL, 30 segundos.
# A2. Correr sin guardar. La bolita ● tiene que ser X. ⌘+S.
# A3. Carpeta equivocada, o venv desactivado.
#     Leer la palabra antes del %, y si está el (.venv).
#
# ===== B · LITERAL vs VARIABLE (mi familia dominante) =====
# B1. == cuando quiero =, o los lados del = invertidos.
# B2. Comillas donde iba la variable.
#       writerow(["message"])  -> escribe la palabra 200 veces
#       writerow([message])    -> escribe el contenido
# B3. Valor fijo donde iba el parámetro.
#       stop_sequences=["```"] adentro de create() en vez del parámetro
#       que recibí. La función lo acepta, lo ignora, y NO SE QUEJA.
# B4. Nombre de archivo sin comillas.
#       open(messages.csv)   -> busca el atributo .csv de una variable
# B5. El nombre de un error usado como condición.
#       elif FileNotFoundError:  -> siempre True
# B6. Un comentario explicativo convertido en código.
#       row["name"] is "last, name" era una descripción, no una orden.
# B7. Llaves fuera de una f-string: print({x}) imprime un set.
#
# ===== C · EL VALOR SE PIERDE ============================
# C1. Líneas que calculan y tiran el resultado.
#     z != 0 / s.isalnum() / shorten(word) / message.content[0].text
#     sueltas. Para que una condición HAGA algo va en un if. Para que
#     un valor sobreviva va con =.
# C2. Variable suelta en una línea queriendo decir "volvé a preguntar".
# C3. Asignar el resultado de un método que devuelve None.
#     x = lista.append()  ·  writer = writer.writeheader()
#
# ===== D · ADENTRO / AFUERA DEL LOOP =====================
# D1. El acumulador o la bandera nacen adentro -> se reinician.
# D2. Lo que se decide UNA vez queda adentro -> se re-hace cada vuelta
#     (el random nuevo en cada intento, en game).
# D3. print() adentro del loop cuando iba uno solo al final.
# D4. El for me pisa una variable: for result in range(3).
# D5. Escribir el archivo adentro del loop -> queda solo la última vuelta.
#
# ===== E · pass / continue / break =======================
# E1. pass donde va continue: sigue bajando y ejecuta lo que quería
#     saltear. Bug silencioso.
# E2. break donde va return, dentro de una función.
#
# ===== F · try MAL PUESTO ================================
# F1. La línea riesgosa afuera del try -> el except no sirve.
# F2. Un solo except para errores que necesitan reacciones distintas.
# F3. Un except con pass sobre un error real -> esconde la causa y
#     después explota en otro lado con un traceback engañoso.
#
# ===== G · LA FUNCIÓN NO ES TESTEABLE ====================
# G1. input() adentro de una función que ya recibió el dato.
#     Pisa el parámetro y cuelga los tests.
# G2. Devuelve texto decorado ("Output: X", "$0") en vez del valor.
# G3. Normaliza en main() y no adentro de la función.
# G4. Mezclar escalas (0.75 vs 75) o tipos (0 vs "$0").
#
# ===== H · TESTS QUE NO MIDEN ============================
# H1. Expectativa mal calculada a mano. El rojo puede ser mío.
# H2. Tests que no pueden fallar (comparar contra un tipo, o pedir
#     algo que se cumple siempre).
#
# ===== I · VARIABLE O MÉTODO EQUIVOCADO ==================
# I1. Acumular la variable que no es.
#     all_messages.extend(messages) en vez de batch. El print de
#     progreso mostraba números que parecían correctos: el peor bug.
# I2. append donde iba extend -> 10 elementos en vez de 200.
# I3. Parámetro de otra clase: csv.writer(f, fieldnames=...)
# I4. Intercambiar sys.argv[1] y [2]. 1 = entrada, 2 = salida.
# I5. Dos operaciones en un solo "=" con desbalance de nombres.
# I6. .strip() para un espacio que está en el medio.
# I7. Olvidarme el https:// en una URL.
#
# ===== J · DESTRUCTIVO / CARO ============================
# J1. Escribir el nombre de archivo equivocado en un open(..., "w").
#     Casi piso 200 clasificaciones con pick_rows.py.
#     ANTES de correr algo que escribe: leer el nombre de salida.
#     Si pasa: git restore <archivo>
# J2. Re-correr un script que gasta API para probar un cambio cosmético.
#     Con Haiku son centavos. Con un modelo caro y 100k filas, no.
# J3. Guardar un archivo sin la extensión .py. Corre, pero no se importa
#     y VS Code no lo trata como Python.
# J4. Medir con un modelo y cotizar con otro.

# ----------------------------------------------------------
# 4.2 QUÉ SIGNIFICA CADA TRACEBACK
# ----------------------------------------------------------
# LEER DE ABAJO HACIA ARRIBA. La última línea dice QUÉ, las de arriba
# DÓNDE, y el ^^^^ marca la posición exacta.
#
# NameError: name 'X' is not defined
#   O es una palabra suelta sin comillas, o es de OTRA función, o la
#   línea que la creaba está adentro de un except que hizo pass.
#
# UnboundLocalError: cannot access local variable 'x'
#   La variable se crea SOLO adentro de un if que no se cumplió.
#   O: escribí  message = message.messages.create(...)  — Python ve que
#   'message' se asigna en esa línea, la trata como local, y al evaluar
#   el lado derecho todavía no tiene valor. Si el nombre fuera otro,
#   sería NameError (más claro). Que coincida con el destino lo disfraza.
#
# ModuleNotFoundError: No module named 'X'
#   No está instalada EN EL PYTHON QUE ESTOY USANDO (venv vs sistema).
#
# AttributeError: 'str' object has no attribute 'isnum'
#   Ese método no existe para ese tipo, o me lo inventé.
# AttributeError: 'NoneType' object has no attribute 'X'
#   Le apliqué un método al resultado de algo que devuelve None
#   (print, .append, .writeheader).
# AttributeError: 'list' object has no attribute 'join'
#   join es del separador: " ".join(lista)
#
# TypeError: 'dict' object is not callable
#   Paréntesis donde van corchetes. fruits("Apple") -> fruits["Apple"]
# TypeError: 'Response' object is not subscriptable
#   Corchetes al objeto de requests. Primero .json()
# TypeError: 'type' object is not iterable
#   Le pasé un TIPO donde iba un valor. shorten(int) -> shorten("5")
# TypeError: float() argument must be ... not 'dict'
#   Me quedé un nivel corto navegando el JSON. Falta otro corchete.
# TypeError: object of type 'int' has no len()
# TypeError: unsupported operand for *: 'dict' and 'float'
#   Opero con el contenedor, no con el valor de adentro.
# TypeError: '<=' not supported between 'int' and 'str'
#   Comparo número con string. Falta convertir.
# TypeError: writer() takes no keyword arguments
#   fieldnames es de DictWriter, no de csv.writer.
# TypeError: create() got an unexpected keyword argument 'X'
#   Typo en el nombre de un parámetro (stop_sequencies).
#
# ValueError: invalid literal for int() with base 10: 'cat'
#   Quise convertir algo que no es número. except ValueError.
# ValueError: not enough values to unpack
#   Los nombres a la izquierda del = no coinciden con lo que dio split.
#
# IndexError: list index out of range
#   Pedí una posición que no existe. Clásico: sys.argv[1] sin argumento.
#   -> chequear len() ANTES de leer el índice.
#
# KeyError: 'X'
#   Esa clave no está en el diccionario. Si es un cruce de archivos:
#   ese texto está en uno y no en el otro, casi siempre porque se copió
#   a mano o desde una versión vieja. -> if clave not in dic: continue
#
# FileNotFoundError
#   El archivo no existe, o estoy parado en otra carpeta. No se previene
#   con un if: se atrapa alrededor del open.
#
# AssertionError: assert 'MRclG' == 'MRclg'
#   Un test falló. Pytest muestra el diff. Revisar si el error está en
#   el código O en mi expectativa.
#
# json.JSONDecodeError
#   Lo que volvió no era JSON válido. Casi siempre: el modelo agregó
#   texto alrededor, o max_tokens cortó la respuesta a la mitad.
#
# requests.exceptions.MissingSchema     falta https://
# EOFError / KeyboardInterrupt          Ctrl-D / Ctrl-C
# ZeroDivisionError                     división por cero
#
# SyntaxError: cannot assign to function call here
#   Puse la llamada a la izquierda del =.
# SyntaxError: invalid syntax
#   Falta paréntesis, coma, comillas o los dos puntos.
#   También: except (A) (B): en vez de except (A, B):
# IndentationError: unexpected indent
#   Indenté una sentencia de nivel superior.
#
# command not found: X
#   bitcoin.py no es un comando -> python3 bitcoin.py
# can't open file '...': No such file or directory
#   Estoy en otra carpeta. Leer el prompt y hacer cd.


# ##########################################################
#  PARTE 5 · RUTINA
# ##########################################################

# ----------------------------------------------------------
# 5.1 UN EJERCICIO DE CS50P
# ----------------------------------------------------------
# 1. Leer la página ENTERA. La consigna está en "Implementation Details".
# 2. Escribir las reglas en una lista, cada una como PREGUNTA.
# 3. Mirar el Demo carácter por carácter. check50 compara LITERAL.
# 4. cd a la carpeta. Nombre EXACTO. Venv si hace falta.
# 5. UNA regla por vez. Correr. Verificar. Recién ahí la siguiente.
# 6. Probar YO los casos feos ANTES de check50: el que se pasa, el vacío,
#    el negativo, el cero.
# 7. check50 · 8. si sale rojo, correr ese input a mano · 9. submit50

# ----------------------------------------------------------
# 5.2 SI EL EJERCICIO PIDE TESTS
# ----------------------------------------------------------
# 1. El archivo y el test, EN LA MISMA CARPETA.
# 2. Reestructurar primero: lógica en una función que recibe y devuelve,
#    con la normalización adentro.
# 3. Un test por caso, cada uno en su propia def test_algo().
# 4. Calcular a mano el esperado. Con cuidado.
# 5. pytest · 6. preguntarme si cada test PODRÍA fallar.

# ----------------------------------------------------------
# 5.3 UN EXPERIMENTO DE PROMPT
# ----------------------------------------------------------
# 1. Anotar el baseline ANTES de tocar nada.
# 2. Correr dos veces sin cambios -> ese es el ruido, mi umbral.
# 3. UN cambio por vez.
# 4. Re-correr sobre el set chico (20), no sobre los 200.
# 5. Anotar: qué cambié, qué pasó, si está arriba o abajo del ruido.
# 6. Leer los desacuerdos nuevos. ¿Cambiaron de dirección o solo de cantidad?

# ----------------------------------------------------------
# 5.4 CHECKLIST ANTES DE PEDIR AYUDA
# ----------------------------------------------------------
# [ ] ¿Guardé? (⌘+S — bolita ● -> X)
# [ ] ¿Corrí el código, o solo lo escribí?
# [ ] ¿Verifiqué en el REPL los métodos que usé?
# [ ] ¿Estoy en la carpeta correcta? ¿Está el (.venv)?
# [ ] ¿Imprimí la variable antes de usarla? ¿Sé qué hay adentro?
# [ ] ¿Hay alguna línea que calcula algo y no lo guarda?
# [ ] ¿El acumulador/bandera nace AFUERA del loop?
# [ ] ¿Lo que se decide una vez está afuera del loop?
# [ ] ¿La línea que puede romper está ADENTRO del try?
# [ ] ¿La indentación empareja los if/else y los loops como quiero?
# [ ] ¿Cada función DEVUELVE, o solo imprime?
# [ ] ¿La función normaliza su propio input?
# [ ] ¿Normalicé los dos lados de la comparación?
# [ ] ¿Misma escala y mismo TIPO?
# [ ] ¿Validé los DOS extremos del rango?
# [ ] ¿El nombre del archivo de salida es el que quiero pisar?

# ----------------------------------------------------------
# 5.5 SI ME TRABO (en este orden)
# ----------------------------------------------------------
# 0-5 min    Leer el error ENTERO, de abajo hacia arriba.
# 5-15 min   print() de las variables justo antes de la línea que falla.
# 15-20 min  Buscar el mensaje de error textual en Google.
# 20+ min    Preguntar: "no me des el código, explicame por qué pasa
#            y decime en qué línea mirar".
# NUNCA      Copiar y pegar algo que no entiendo.
#
# SI SE ENREDA FEO — el método que funcionó siempre:
#   Borrar todo y volver a DOS líneas. Correr. Verificar.
#   Agregar UNA línea. Correr. Verificar.
#
# Y si el bloqueo es "no sé qué escribir", casi siempre el problema real
# es "no sé qué tengo". Imprimir las variables destraba más que pensar.
#
# SI ESTOY QUEMADO: cerrar el día. Commitear aunque esté a medias.

# ----------------------------------------------------------
# 5.6 CERRAR EL DÍA
# ----------------------------------------------------------
#   cd ~/ai-plan
#   git status            <- que NO aparezcan .env ni .venv
#   git add .
#   git commit -m "dia N: lo que hice"
#   git push
#
# Aunque esté roto o incompleto. Regla del plan.
# La guía se actualiza UNA VEZ POR SEMANA, los viernes.

# ----------------------------------------------------------
# 5.7 CIERRE DEL MES 1 (2-oct-2026)
# ----------------------------------------------------------
# Pregunta del mes: ¿puedo automatizar una tarea real con un LLM
# y PROBAR que funciona?  -> Sí, y tengo el número.
#
# Lo construido en 4 semanas desde cero:
#   - CS50P completo (PS0 a PS6)
#   - Generador de 200 mensajes sintéticos con variedad controlada
#   - Clasificador con salida estructurada (prefill + stop sequences)
#   - Pipeline de 200 con try/except por fila -> CSV
#   - Sistema de evaluación propio con ground truth de 20 filas
#   - Tres experimentos de prompt medidos contra el ruido
#   - Costo unitario medido: $0,00073 por mensaje
#
# Resultado: ~18/20 category y sentiment, ~16-17/20 priority, ±1-2.
#
# LOS CUATRO CONCEPTOS QUE ME LLEVO:
#   1. Medir el ruido antes de medir la mejora
#   2. El modelo no falla, le falta mi información
#   3. Un campo sin definir es un campo ruidoso
#   4. Mi ground truth también se equivoca
#
# LO QUE MÁS VA A SEGUIR APARECIENDO:
#   2.7 y 2.8   funciones con parámetros opcionales y testeables
#   2.13        diccionarios anidados y como índice
#   2.19        APIs, requests y JSON
#   2.14/2.15   try/except vs if
#   3.8 a 3.11  evals, ruido, costo
#   1.7         secretos

# ----------------------------------------------------------
# 5.8 SEMANA 5 (8-oct-2026) — TOOLS, ENCADENAMIENTO, ERROR HANDLING
# ----------------------------------------------------------
# Pregunta de la semana: ¿cómo hace Claude para usar herramientas y
# encadenarlas sin que yo haga cada paso?
#
# Lo construido en 3 días (Días 13-15):
#   - Agente mínimo con 1 tool (addition)
#   - Agente multi-tool con historial persistente (3 APIs reales)
#   - Agente con encadenamiento automático (search → calculate → save)
#   - Error handling transparente (fallas → Claude decide qué hacer)
#   - Logging detallado por turno y por tool call
#   - Video de demostración (2 min, 3 escenarios)
#   - README.md + commits + posts en redes
#
# Resultado: 3 tools ejecutadas correctamente, 0 crashes, Claude razona
# qué necesita y ejecuta sin intervención humana.
#
# CONCEPTOS CLAVE APRENDIDOS:
#   1. El schema JSON NO es estético: es un guardrail. El enum define
#      qué Claude PUEDE hacer.
#   2. El historial (messages = [] persistente) es lo que permite
#      planning entre turnos.
#   3. Error handling VA DENTRO del for tool_uses (no en __main__).
#      Claude recibe el error como tool_result, no como crash.
#   4. El logging = observabilidad. Sin logs, no sé qué ejecutó ni por qué.
#
# ESTADÍSTICAS:
#   - Líneas de código: ~350
#   - Tokens totales: ~5,100
#   - Costo estimado: ~$0.008
#   - Files pusheados: 1 video + código + README
#
# LO QUE SIGUE:
#   Semana 6 abre el segundo mes: "¿Cómo le doy al agente acceso a más datos?"
#   - RAG (Retrieval Augmented Generation): buscar en documentos
#   - Memory: estado persistente entre sesiones
#   - MCP (Model Context Protocol): servidores que ofrecen tools


# ##########################################################
#  PARTE 6 · TOOLS — SCHEMAS, CICLOS, ENCADENAMIENTO
# ##########################################################

# ----------------------------------------------------------
# 6.1 EL SCHEMA JSON (GUARDRAIL, NO ESTÉTICA)
# ----------------------------------------------------------
# Una tool es una función que Claude puede DECIDIR ejecutar si la necesita.
# El schema es la ESPECIFICACIÓN: qué parámetros acepta, de qué tipo,
# cuáles son obligatorios.
#
# tools = [
#   {
#     "name": "search_in_csv",
#     "description": "Search products by category or price",
#     "input_schema": {
#       "type": "object",
#       "properties": {
#         "criteria": {
#           "type": "string",
#           "enum": ["electronics", "peripherals", "furniture", "price_high", "price_low"]
#         },
#         "quantity": {
#           "type": "integer",
#           "description": "Number of items to return"
#         }
#       },
#       "required": ["criteria", "quantity"]
#     }
#   }
# ]
#
# EL SCHEMA OBLIGA A CLAUDE A CUMPLIR:
#   - criteria tiene que ser UNO de los valores del enum
#   - quantity tiene que ser un número entero, no un string
#   - Los dos parámetros son obligatorios, no puede faltar ninguno
#
# SI NO ESPECIFICO:
#   - Claude prueba criterios que no existen (tipo "books")
#   - Manda parámetros como strings cuando son números
#   - La función explota en tiempo de ejecución
#
# El enum es la herramienta más efectiva: NO necesito un if/elif adentro
# de la función para validar. Claude ve que tiene 5 opciones, elige una.

# ----------------------------------------------------------
# 6.2 EL CICLO TOOL USE (5 FASES)
# ----------------------------------------------------------
# Fase 1: USER INPUT + TOOLS
#   user_input = "Find 2 electronics and apply 10% discount"
#   messages.append({"role": "user", "content": user_input})
#   response = client.messages.create(
#       model="claude-3-5-sonnet-20241022",
#       max_tokens=1024,
#       tools=tools,      <- ← le digo cuáles tools tiene disponibles
#       messages=messages
#   )
#
# Fase 2: CLAUDE DECIDE USAR UNA TOOL
#   response.stop_reason == "tool_use"
#   Claude devolvió un bloque de content con type == "tool_use"
#   Contiene: .name (qué tool), .id (qué llamada), .input (qué parámetros)
#
# Fase 3: YO EJECUTO LA TOOL
#   tool_uses = [block for block in response.content if block.type == "tool_use"]
#   for tool_use in tool_uses:
#       resultado = execute_tool(tool_use.name, tool_use.input)
#       tool_results.append({
#           "type": "tool_result",
#           "tool_use_id": tool_use.id,  <- ← le vuelvo a mandar el ID
#           "content": resultado
#       })
#
# Fase 4: VUELVO A MANDAR EL CONTEXTO COMPLETO
#   messages.append({"role": "assistant", "content": response.content})
#   messages.append({"role": "user", "content": tool_results})
#   <- ahora messages tiene: mi pregunta + lo que Claude quiso hacer + el resultado
#
# Fase 5: CLAUDE DECIDÉ QUÉ HACER CON EL RESULTADO
#   response = client.messages.create(model=..., messages=messages, tools=tools)
#   Si necesita OTRA tool: vuelvo a Fase 3.
#   Si termina: response.stop_reason == "end_turn" → devuelve la respuesta final
#
# PUNTO CRÍTICO: El historial (messages) crece y se re-envía CADA VEZ.
# Claude ve TODO lo que pasó antes, por eso puede planificar multi-paso.

# ----------------------------------------------------------
# 6.3 MULTI-TOOL CON HISTORIAL PERSISTENTE
# ----------------------------------------------------------
# EL PATRÓN: messages = [] AFUERA del loop, se mantiene entre turnos
#
#   from anthropic import Anthropic
#   client = Anthropic()
#   messages = []
#
#   while True:
#       user_input = input("You: ").strip()
#       if user_input.lower() == "exit": break
#
#       messages.append({"role": "user", "content": user_input})
#
#       while True:  # <- inner loop: mientras haya tool calls
#           response = client.messages.create(
#               model="claude-3-5-sonnet-20241022",
#               max_tokens=1024,
#               tools=tools,
#               messages=messages
#           )
#
#           if response.stop_reason == "tool_use":
#               tool_uses = [block for block in response.content
#                            if block.type == "tool_use"]
#               tool_results = []
#
#               messages.append({"role": "assistant", "content": response.content})
#
#               for tool_use in tool_uses:
#                   result = execute_tool(tool_use.name, tool_use.input)
#                   tool_results.append({
#                       "type": "tool_result",
#                       "tool_use_id": tool_use.id,
#                       "content": result
#                   })
#
#               messages.append({"role": "user", "content": tool_results})
#
#           else:  # stop_reason == "end_turn"
#               final_response = next(
#                   (block.text for block in response.content
#                    if hasattr(block, "text")),
#                   None
#               )
#               print(f"Claude: {final_response}\n")
#               messages.append({"role": "assistant", "content": response.content})
#               break  # <- salir del inner loop, volver a pedir input
#
# RESULTADO: La conversación PERSISTE. Turno 1 pregunto "plan Miami weekend".
# Claude usa 3 tools. Turno 2 pregunto "add concerts", Claude RECUERDA el plan
# anterior y agrega sin repetir lo que ya vio.

# ----------------------------------------------------------
# 6.4 ENCADENAMIENTO — UNA TOOL COMO INPUT DE LA SIGUIENTE
# ----------------------------------------------------------
# ESCENARIO: "Find electronics, apply 20% discount, save report"
#
# tools = [
#   { "name": "search_in_csv", ... },
#   { "name": "calculate_discount", ... },
#   { "name": "save_report", ... }
# ]
#
# def execute_tool(tool_name, tool_input):
#     if tool_name == "search_in_csv":
#         criteria = tool_input.get("criteria")
#         quantity = tool_input.get("quantity")
#         # -> devuelve string con "ID | Product | Price | Stock"
#         return "ID: 1 | Laptop | $1200 | 5\nID: 2 | Monitor | $350 | 8"
#
#     elif tool_name == "calculate_discount":
#         prices = tool_input.get("prices")  # <- estos números vinieron
#         discount_percent = tool_input.get("discount_percent")
#         # del resultado de search_in_csv que Claude parsó
#         total = sum(prices)
#         discount = total * (discount_percent / 100)
#         final = total - discount
#         return f"Original: ${total} | Discount: ${discount} | Final: ${final}"
#
#     elif tool_name == "save_report":
#         filename = tool_input.get("filename")
#         content = tool_input.get("content")
#         with open(filename, "w") as f:
#             f.write(content)
#         return f"✓ Report saved to {filename}"
#
# FLUJO AUTOMÁTICO:
#   Turno 1: Claude ve los 3 tools, piensa "necesito buscar primero"
#   -> ejecuta search_in_csv -> obtiene [1200, 350]
#
#   Turno 2: Claude ve el resultado de search, decide calcular descuento
#   -> ejecuta calculate_discount([1200, 350], 20) -> obtiene totales
#
#   Turno 3: Claude ve los dos resultados, formatea un reporte
#   -> ejecuta save_report(filename, formatted_text) -> archivo creado
#
#   Turno 4: Claude ve que todas las tools se ejecutaron exitosamente
#   -> devuelve respuesta final en lenguaje natural
#
# YO NO ESCRIBO LOS PASOS. Claude decide el orden y qué parametrizar.
# PERO: system prompt importa. "Always save the final report without asking"
# fuerza que no se quede a mitad de camino.

# ----------------------------------------------------------
# 6.5 ERROR HANDLING — TRY/EXCEPT DENTRO DEL FOR TOOL_USES
# ----------------------------------------------------------
# REGLA DE ORO: El try/except va DENTRO del for que recorre tool_uses,
# no en __main__. Esto permite que Claude VEA el error como tool_result
# y decida qué hacer, en vez de crashear.
#
#   for tool_use in tool_uses:
#       try:
#           result = execute_tool(tool_use.name, tool_use.input)
#           is_error = False
#       except Exception as e:
#           result = f"Tool failed: ❌ {str(e)}"
#           is_error = True
#
#       tool_results.append({
#           "type": "tool_result",
#           "tool_use_id": tool_use.id,
#           "content": result
#       })
#
#       log.append({
#           "tool_name": tool_use.name,
#           "tool_input": tool_use.input,
#           "tool_result": result,
#           "is_error": is_error
#       })
#
# TRES ESCENARIOS Y CÓMO LOS MANEJA CLAUDE:
#
# 1. FALLA TOTAL (ValueError en search_in_csv):
#    Claude recibe: "Tool failed: ❌ Database connection lost while searching"
#    Claude decide: "Puedo reportar el error sin inventar datos"
#    -> respuesta: "Unfortunately, the search failed. I cannot proceed."
#    ✓ CORRECTO: no inventó productos
#
# 2. RESULTADO VACÍO (search devuelve ""):
#    Claude recibe: "" (no es un error, solo sin datos)
#    Claude decide: "Si no hay productos, guardo un reporte explicando"
#    -> ejecuta save_report con contenido "No products found"
#    ✓ CORRECTO: documentó lo que pasó
#
# 3. LATENCIA (3 tools tardan 3 segundos):
#    Los tres execute_tool() se disparan, devuelven en el tiempo normal
#    Claude recibe todos los resultados, formatea el reporte final
#    ✓ CORRECTO: no hay problema de timing

# ----------------------------------------------------------
# 6.6 LOGGING — OBSERVABILIDAD POR TURNO Y POR TOOL CALL
# ----------------------------------------------------------
# Sin logs, no sé:
#   - qué tools ejecuté
#   - en qué orden
#   - cuáles fallaron
#   - cuántos tokens gasté
#
# EL PATRÓN:
#
#   log = []  # global
#
#   def run_agent(user_message, system_prompt):
#       messages = []
#       turn_num = 0
#       execution_log = {
#           "turns": [],
#           "total_input_tokens": 0,
#           "total_output_tokens": 0
#       }
#
#       messages.append({"role": "user", "content": user_message})
#
#       while True:
#           turn_num += 1
#           response = client.messages.create(
#               model="claude-3-5-sonnet-20241022",
#               max_tokens=1024,
#               system=system_prompt,
#               tools=tools,
#               messages=messages
#           )
#
#           # CONTAR TOKENS DE ESTE TURNO
#           execution_log["total_input_tokens"] += response.usage.input_tokens
#           execution_log["total_output_tokens"] += response.usage.output_tokens
#
#           if response.stop_reason == "tool_use":
#               tool_uses = [...]
#               messages.append({"role": "assistant", "content": response.content})
#
#               for tool_use in tool_uses:
#                   try:
#                       result = execute_tool(tool_use.name, tool_use.input)
#                       is_error = False
#                   except Exception as e:
#                       result = f"Tool failed: {str(e)}"
#                       is_error = True
#
#                   # LOG CADA TOOL CALL
#                   execution_log["turns"].append({
#                       "turn": turn_num,
#                       "tool_name": tool_use.name,
#                       "tool_input": tool_use.input,
#                       "tool_result": result,
#                       "is_error": is_error,
#                       "input_tokens": response.usage.input_tokens,
#                       "output_tokens": response.usage.output_tokens
#                   })
#
#                   tool_results.append({...})
#
#               messages.append({"role": "user", "content": tool_results})
#
#           else:  # "end_turn"
#               final_response = next(...).text
#
#               # LOG LA FINALIZACIÓN
#               execution_log["turns"].append({
#                   "turn": turn_num,
#                   "event": "agent_complete",
#                   "final_response": final_response,
#                   "input_tokens": response.usage.input_tokens,
#                   "output_tokens": response.usage.output_tokens
#               })
#
#               log.append(execution_log)
#               return final_response
#
# AL FINAL, IMPRIMO UN RESUMEN:
#   print("=== TOKEN USAGE ===")
#   print(f"Total: {execution_log['total_input_tokens']} in + "
#         f"{execution_log['total_output_tokens']} out")
#
# ESTO TE DICE:
#   - Cuántas vueltas tuvo que dar Claude
#   - Qué tools ejecutó
#   - Cuáles fallaron y cómo
#   - El costo exacto

# ----------------------------------------------------------
# 6.7 ERRORES COMUNES CON TOOLS
# ----------------------------------------------------------
#
# ===== K · TOOLS ===================================
# K1. El schema no es suficientemente restrictivo.
#     properties con type: "string" pero sin enum -> Claude inventa valores
#     -> Solución: enum["electronics", "peripherals", "furniture"]
#
# K2. try/except en __main__ en vez de dentro del for tool_uses.
#     El programa revienta, Claude nunca ve el error como tool_result
#     -> Solución: except DENTRO del for, devuelve mensaje "Tool failed: ..."
#
# K3. No loggear dentro del loop.
#     Al final no sé qué ejecutó, cuándo, ni por qué
#     -> Solución: append al log DENTRO del for tool_uses
#
# K4. No guardar el objeto response completo: "return message.content[0].text"
#     Pierde .usage con los tokens, no puedo medir costo
#     -> Solución: Pasar el objeto entero, extraer .text Y .usage.input_tokens
#
# K5. Cambiar messages AFUERA del while True.
#     El historial se pierde entre preguntas
#     -> Solución: messages = [] ANTES del while, se mantiene durante toda
#        la sesión de usuario
#
# K6. Parámetros opcionales sin validar.
#     API de Claude no acepta None -> TypeError
#     -> Solución: if sistema not in None: params["system"] = sistema
#        (ver 2.7 PARÁMETROS OPCIONALES)
#
# K7. Asumir que el JSON es válido sin parsear.
#     El modelo cortó la respuesta a max_tokens o agregó texto
#     -> json.JSONDecodeError -> Solución: try/except alrededor de .json()

# ----------------------------------------------------------
# 6.8 LOS PATRONES QUE SE REPITEN EN TOOLS
# ----------------------------------------------------------
#
# PATRÓN 1: VALIDACIÓN ANTES DE LA HERRAMIENTA (schema)
#   El enum es el validador. No necesito if/elif adentro de execute_tool.
#   properties con "required": ["X", "Y"] previene parametros faltantes.
#
# PATRÓN 2: HISTORIAL = PLANNING
#   messages = [] persistente permite que Claude razone multi-turno.
#   Sin historial, cada turno es independiente.
#
# PATRÓN 3: ENCADENAMIENTO AUTOMÁTICO
#   No escribo "luego hace esto". Claude ve el resultado de una tool
#   y decide si necesita otra. El system prompt guía ("Always save...").
#
# PATRÓN 4: ERROR HANDLING TRANSPARENTE
#   try/except DENTRO del loop, devuelvo "Tool failed: ..." como tool_result.
#   Claude ve el error y elige: reintentar, reportar, o actuar diferente.
#
# PATRÓN 5: LOGGING = OBSERVABILIDAD
#   Cada tool_use genera un entry con turn, tool_name, input, result, is_error.
#   Al final, puedo responder "¿qué pasó?" con datos.

# ----------------------------------------------------------
# 6.9 CÓMO ESTUDIAR TOOLS
# ----------------------------------------------------------
#
# DÍA 13: Agente MÍNIMO.
#   1 tool, 1 parámetro. Ver cómo Claude decide "necesito esta tool".
#   Código: simple_tool_agent.py
#
# DÍA 14 A: Multi-tool CON HISTORIAL.
#   3 tools reales (APIs externas). Turno 1 ejecuta 14 tool_uses,
#   turno 2 Claude recuerda y ajusta. Punto: historial.
#   Código: agent_with_tools.py
#
# DÍA 14 B: Encadenamiento.
#   search -> calculate -> save. Sin intervención. Punto: orden automático.
#   Código: agent_chained_tasks.py
#
# DÍA 15 A: Error handling.
#   3 escenarios: falla, vacío, éxito. Punto: Claude no inventa datos.
#   Código: agent_error_handling.py + logging.
#
# DÍA 15 B: Observabilidad.
#   Video, README, logging detallado. Punto: puedo ver qué hizo.
#
# EJERCICIO PROPIO (para consolidar):
#   Agente con 2-3 tools nuevas. Un scenario real (tu trabajo, un hobby).
#   El punto es que sea tool_use, no que sea complejo. Empezá pequeño.

# ----------------------------------------------------------
# 6.10 PRÓXIMA SEMANA (6): RAG, MEMORY, MCP
# ----------------------------------------------------------
# Week 6 abre el segundo mes: "¿Cómo le doy al agente acceso a más datos?"
#
# RAG = Retrieval Augmented Generation
#   El agente no memoriza: BUSCA en documentos cuando lo necesita.
#   Tool = vector search. Schema = qué buscar.
#
# Memory = Estado persistente
#   Tools que guardan datos, tools que leen. Entre sesiones.
#
# MCP = Model Context Protocol
#   Servidores que ofrecen tools. El agente elige cuál usar.
#
# El ciclo tool_use que viste en Semana 5 es la COLUMNA VERTEBRAL.
# Semana 6 solo agrega herramientas nuevas al mismo ciclo.