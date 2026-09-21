# ==========================================================
#  GUÍA PERSONAL — Axel · MacBook Air (macOS, zsh)
#  Reescrita al cerrar la SEMANA 3 (Librerías, APIs y Unit Tests).
#  CS50P: Weeks 0-5 vistas. PS0 a PS5 entregados.
#
#  CÓMO ESTÁ ORGANIZADA:
#    PARTE 1 · ENTORNO     terminal, VS Code, git, venv, secretos
#    PARTE 2 · PYTHON      referencia por concepto
#    PARTE 3 · PATRONES    las formas que se repiten en todo ejercicio
#    PARTE 4 · MIS ERRORES lo que rompo yo + qué significa cada error
#    PARTE 5 · RUTINA      cómo encaro un ejercicio y cómo cierro el día
#
#  La PARTE 2 se consulta cuando no me acuerdo cómo se escribe algo.
#  La PARTE 4 se consulta cuando algo no anda. Son momentos distintos.
# ==========================================================


# ##########################################################
# ##########################################################
#  PARTE 1 · ENTORNO
# ##########################################################
# ##########################################################

# ----------------------------------------------------------
# 1.1 ¿DÓNDE ESTOY?  (la pregunta que más me cuesta)
# ----------------------------------------------------------
# El prompt lo dice:
#   axelefron@MacBook-Air-de-Axel-2 semana-03 %
#                                   ^^^^^^^^^  carpeta actual
#
# TODOS los comandos actúan desde donde estoy parado:
#   python3 archivo.py   busca el archivo ACÁ
#   check50 / pytest     buscan el archivo ACÁ
#   git add .            agarra de ACÁ HACIA ABAJO, no todo el repo
#   load_dotenv()        busca el .env desde ACÁ
#
# LEER LA PALABRA ANTES DEL %  antes de correr cualquier cosa.
#
# pwd            ruta completa
# ls             qué hay acá
# cat archivo    contenido REAL en disco (no el del editor sin guardar)

# ----------------------------------------------------------
# 1.2 MOVERME
# ----------------------------------------------------------
# cd carpeta                  entro a una subcarpeta
# cd ..                       subo un nivel
# cd ~/ai-plan/semana-03      voy directo   (~ = /Users/axelefron)
# cd car + TAB                autocompleta
#
# cd es para CARPETAS, nunca para archivos.
#   cd ~/.../coke.py   ->  "not a directory"
# El archivo es el destino de python3, no de cd:
#   cd ~/ai-plan/semana-03
#   python3 bitcoin.py 2
#
# Un .py NO es un comando. "bitcoin.py 4" -> command not found.
# Lo corre el intérprete: python3 bitcoin.py 4
#
# Nombres: sin espacios, sin mayúsculas. Uso guion_bajo.

# ----------------------------------------------------------
# 1.3 % vs >>>
# ----------------------------------------------------------
# %    = terminal (zsh). ls, cd, python3, check50, git, pytest
# >>>  = estoy DENTRO de Python. Solo entiende Python. cd no existe acá.
#        Salir: exit()
#
# Si abre en >>> solo, es el perfil "Python" de la terminal.
# Quiero zsh: Terminal -> New Terminal (NO "With Profile").

# ----------------------------------------------------------
# 1.4 EL REPL — mi herramienta más subusada
# ----------------------------------------------------------
# python3          entro
# exit()           salgo
#
# Sirve para VERIFICAR EN 30 SEGUNDOS en vez de adivinar:
#   "1 + 1".split(" ")        ->  ['1', '+', '1']
#   "CS50"[0:2]               ->  'CS'
#   5 in [5, 10, 25]          ->  True
#   f"{1234567.89:,.4f}"      ->  '1,234,567.8900'
#   dir("")                   ->  TODOS los métodos de string
#   help(random.randint)      ->  cómo se usa, qué devuelve
#
# LAS TRES PREGUNTAS DE UNA LIBRERÍA NUEVA:
#   dir(libreria)     ¿qué tiene adentro?
#   help(algo)        ¿cómo se usa?
#   probarlo          ¿qué devuelve con datos reales?
#   pypi.org          el modelo mental, para qué existe
#
# Adivinar nombres de métodos (.isnum, .isfloat, .add, figlet.random)
# es lo que más tiempo me costó en todo el mes. El REPL lo mata al toque.

# ----------------------------------------------------------
# 1.5 MAC: python3 Y pip3
# ----------------------------------------------------------
# python3 archivo.py      correr
# pip3 install paquete    instalar
# python / pip a secas    NO (apuntan al viejo del sistema)

# ----------------------------------------------------------
# 1.6 ATAJOS
# ----------------------------------------------------------
# VS CODE
#   ⌘+S              guardar        <- la bolita ● tiene que volverse X
#   ⌘+Z / ⌘+⇧+Z      deshacer / rehacer
#   ⌘+/              comentar selección   <- para aislar bugs
#   ⌃+`              abrir terminal
#   ⇧+Enter          correr solo la selección
#
# TERMINAL
#   ↑          comando anterior
#   ⌃+U        borrar la línea actual
#   ⌃+C        cancelar lo que corre o está colgado (loop infinito)
#   ⌃+D        cerrar la entrada (EOFError) — NO es lo mismo que ⌃+C
#   TAB        autocompletar

# ----------------------------------------------------------
# 1.7 GIT — cerrar el día
# ----------------------------------------------------------
# SIEMPRE desde la raíz del repo:
#
#   cd ~/ai-plan
#   git status                <- LEER antes de add. Dice qué ve Git
#                                y entre paréntesis qué comando usar.
#   git add .                 <- "." = esta carpeta HACIA ABAJO
#   git commit -m "dia N"
#   git push
#
# Señal de terminado: desaparece el * de "main*" abajo a la izquierda,
# y las M del Explorer. git status dice "working tree clean".
#
# QUÉ ES CADA COSA
#   git add      pone en el staging area. NO guarda nada todavía.
#   git commit   congela la foto. Devuelve un hash (ej: 2d3c367).
#   git push     sube. El único que usa internet.
#   git restore <ruta>   REEMPLAZA el archivo por la versión del
#                        último commit. Recupera borrados y deshace cambios.
#
# git restore NO es ⌘+Z. ⌘+Z deshace tecleo y depende del editor abierto.
# git restore trae la versión commiteada, sin importar qué pasó después.
# Por eso commiteo seguido AUNQUE ESTÉ ROTO: es mi botón de deshacer real.
#
# .gitignore (en la raíz, un patrón por línea, SIN espacios adelante):
#   .env
#   __pycache__/
#   .DS_Store
#   .venv/
#
# OJO: hay DOS .gitignore posibles. El mío está en la raíz de ai-plan.
# El que Python crea adentro de .venv/ tiene un "*" y solo se ignora
# a sí mismo. Mirar la barra de arriba del editor para saber cuál abrí.
#
# OJO 2: axelefron/ai-plan (mío, git push) y me50/axelefron (CS50, submit50)
# son DOS REPOS DISTINTOS. Un push no entrega nada a CS50.

# ----------------------------------------------------------
# 1.8 INDENTACIÓN = ESTRUCTURA
# ----------------------------------------------------------
# En Python la sangría no es estética: ES la lógica.
#
# Un else se aparea con el if que tiene LA MISMA sangría.
# Si lo indento de más, cuelga del if interno y cambia todo el programa
# sin dar ningún error.
#
# Lo mismo con loops anidados:
#   for _ in range(10):        <- las 10 cuentas
#       x = ...                <- ADENTRO: valor nuevo cada vuelta
#       correcto = False
#       for _ in range(3):     <- los 3 intentos, anidado
#           ...
#       if correcto == False:  <- al nivel del for de 3: corre al terminarlo
#           ...
#   print(score)               <- sin indentar: al final de todo
#
# Cuando el programa "hace cualquier cosa" pero no tira error:
# mirar las líneas verticales de VS Code antes que la lógica.

# ----------------------------------------------------------
# 1.9 ENTORNOS VIRTUALES (.venv)   [nuevo · semana 3]
# ----------------------------------------------------------
# Un venv es un Python APARTE, con su propia lista de librerías,
# separado del Python del sistema. Sirve para que cada proyecto tenga
# lo suyo sin ensuciar la máquina.
#
#   source /Users/axelefron/ai-plan/.venv/bin/activate    activar
#   deactivate                                            salir
#
# Lo reconozco por el (.venv) adelante del prompt:
#   (.venv) axelefron@MacBook-Air-de-Axel-2 ai-plan %
#
# CON EL VENV ACTIVO, pip3 instala ADENTRO del venv.
# SIN el venv, instala en el sistema. Son dos listas distintas.
#
# ModuleNotFoundError: No module named 'dotenv'
#   -> lo instalé en un Python y estoy corriendo con el otro.
#      Instalar con el venv activo, correr con el venv activo.
#
# Qué va dónde:
#   herramientas que uso en TODAS las carpetas (check50, submit50) -> global
#   librerías de ESTE proyecto (requests, dotenv, pytest)          -> venv
#
# .venv/ va al .gitignore. Son miles de archivos que no son míos
# y se regeneran solos.
#
# .env  y  .venv  son cosas DISTINTAS con nombre parecido:
#   .env  = archivo de texto con mis secretos
#   .venv = carpeta con el Python aislado

# ----------------------------------------------------------
# 1.10 SECRETOS — API KEYS      [nuevo · semana 3]
# ----------------------------------------------------------
# Una API key es una credencial: quien la tenga puede gastar en mi nombre.
# Mi repo es PÚBLICO y hay bots que escanean GitHub buscando keys.
#
# EL PATRÓN, SIEMPRE:
#   1. pip3 install python-dotenv       (con el venv activo)
#   2. archivo .env, una línea, sin comillas ni espacios:
#          COINCAP_API_KEY=abc123...
#   3. .env listado en .gitignore
#   4. en el código:
#          from dotenv import load_dotenv
#          import os
#          load_dotenv()
#          mi_key = os.getenv("COINCAP_API_KEY")
#   5. ANTES de cualquier git add: git status NO debe mostrar .env
#
# Si getenv devuelve None -> el .env no se encontró (otra carpeta, o typo).
#
# SI ALGO ME OBLIGA A HARDCODEAR (check50 de bitcoin corre en el server
# de CS50, donde no existe mi .env ni la librería dotenv):
#   1. commitear primero la versión segura
#   2. romper el archivo (pegar la key)
#   3. check50 + submit50
#   4. git restore <archivo>       <- este paso NO es opcional
#   5. rotar la key en el proveedor (borrar la vieja, crear una nueva)
#
# Borrar una key filtrada del archivo NO alcanza: queda en el historial
# de commits. Rotarla es lo que convierte el texto filtrado en basura.


# ##########################################################
# ##########################################################
#  PARTE 2 · PYTHON — REFERENCIA
# ##########################################################
# ##########################################################

# ----------------------------------------------------------
# 2.1 FUNCIÓN vs MÉTODO
# ----------------------------------------------------------
# función -> el valor va ADENTRO:   len(texto)   abs(-10)   int("5")
# método  -> va PEGADO con punto:   texto.strip()
#
# Los métodos son DE UN TIPO: los de texto solo andan en texto.
# La mayoría NO modifica el original: DEVUELVEN algo nuevo.
#   texto.strip()          calcula y tira el resultado
#   texto = texto.strip()  lo guarda
#
# LA EXCEPCIÓN QUE ME MORDIÓ: los métodos de LISTA modifican en el lugar
# y devuelven None.
#   x = lista.append(algo)   -> x vale None, no la lista
#   lista.append(algo)       -> así, sin asignar
#
# Encadenar: cada método opera sobre el resultado del anterior.
#   texto.strip().lower().replace(" ", "-")
# EL ORDEN IMPORTA: strip ANTES que replace.
#
# Los corchetes se encadenan igual:
#   dic["data"]["priceUsd"]   -> primero abro "data", a ESO le pido "priceUsd"

# ----------------------------------------------------------
# 2.2 TIPOS Y CONVERSIÓN
# ----------------------------------------------------------
# input() SIEMPRE devuelve str, aunque escriban un número.
# "42" y 42 son cosas distintas. Nunca son iguales.
#
# int(x)    a entero    int("42") -> 42       (int("2.5") explota)
# float(x)  a decimal   float("2.5") -> 2.5
# str(x)    a texto     str(42) -> "42"
# type(x)   qué tipo es. Para debuggear.
# abs(x)    valor absoluto. abs(-10) -> 10   (función suelta, no método)
# len(x)    cuántos caracteres/elementos
# round(x, n)  redondea para CALCULAR (para mostrar uso f-string)
#
# LO QUE LLEGA DE AFUERA CASI SIEMPRE ES TEXTO, aunque parezca número:
#   input()                    -> str
#   sys.argv[1]                -> str
#   un valor de un JSON        -> puede ser str ("323186.4")
#   "123" * 2 -> "123123"      (repite, no multiplica)
#
# CONVERTIR UNO POR UNO, no la colección entera:
#   float("7:21")              explota
#   float(["1","+","1"])       explota (es una lista)
#   float(sys.argv)            explota (es la lista entera)
#   float(sys.argv[1])         sí

# ----------------------------------------------------------
# 2.3 STRINGS — MÉTODOS
# ----------------------------------------------------------
# NORMALIZAR (antes de comparar)
#   .strip()        saca espacios de los EXTREMOS (no los del medio)
#   .lower()        todo minúscula
#   .upper()        todo MAYÚSCULA
#   .casefold()     como lower pero más agresivo
#   .title()        Primera Letra De Cada Palabra
#   .capitalize()   Solo la primera letra de todo
#
# OJO con .title(): CAMBIA las mayúsculas del original.
# Si el enunciado pide conservar el caso tal cual, .title() lo rompe.
#
# PREGUNTAR (devuelven True / False — se usan DIRECTO en el if,
#            no hace falta "== True")
#   .isalpha()          ¿son todas letras?
#   .isdigit()          ¿son todos dígitos?
#   .isalnum()          ¿letras o números, sin símbolos ni espacios?
#   .isupper()          ¿está todo en mayúscula?
#   .islower()          ¿está todo en minúscula?
#   .startswith("h")    ¿empieza con eso?
#   .endswith(".py")    ¿termina con eso?
#
# NO EXISTE .isfloat(). Me lo inventé dos veces.
# "¿esto se puede convertir a número?" NO se pregunta con un if:
# se INTENTA la conversión adentro de un try y se ve si explota.
#
# TRANSFORMAR
#   .replace(viejo, nuevo)   cambia TODAS las apariciones
#   .count("a")              cuántas veces aparece
#   .split(sep)              parte el texto y devuelve una LISTA
#   " ".join(lista)          une una lista en un texto
#
# .split() RECIBE UN SOLO SEPARADOR.
#   El segundo argumento es un NÚMERO (cuántos cortes), no otro separador.
#   Para partir por dos cosas: dos pasos.

# ----------------------------------------------------------
# 2.4 STRINGS — POSICIONES Y PEDAZOS
# ----------------------------------------------------------
#   s[0]      primer carácter        (empieza en CERO)
#   s[-1]     último
#   s[0:2]    desde 0 HASTA 2 SIN INCLUIR el 2  -> los dos primeros
#
# EL NÚMERO DE LA DERECHA SE EXCLUYE. Siempre.
#   "CS50"[0:1]  ->  "C"     (una sola letra)
#   "CS50"[0:2]  ->  "CS"    (dos letras)
#
# La misma regla en OTROS LADOS:
#   range(3)                  -> 0, 1, 2      (tres vueltas)
#   range(1, 3)               -> 1, 2         (DOS vueltas, no tres)
#   random.randrange(1, 11)   -> 1 a 10       (el 11 nunca sale)
#   random.randint(1, 10)     -> 1 a 10       (este SÍ incluye los dos)
#   lista[0:3]                -> los 3 primeros
#
# Cuando quiero incluir el tope: randint, o randrange(1, tope + 1).

# ----------------------------------------------------------
# 2.5 F-STRINGS (mostrar)
# ----------------------------------------------------------
#   f"Total: {percent:,.4f}%"
#    │       │       │     │
#    │       │       │     └─ afuera de {} = texto literal
#    │       │       └─────── ADENTRO: dos puntos + formato
#    │       └─────────────── adentro: la expresión a mostrar
#    └─────────────────────── la f que activa las llaves
#
# REGLA: adentro de {} se calcula, afuera se imprime tal cual.
# Adentro puede ir cualquier expresión, incluso una llamada a función:
#   f"Output: {shorten(word)}"      f"${value(greeting)}"
#
# FORMATOS, todos después de ":" y adentro de las llaves:
#   .1f    1 decimal
#   .2f    2 decimales (plata)
#   ,      separador de miles
#   ,.4f   las dos cosas: miles Y 4 decimales   -> 323,186.4000
#
# \n dentro de un string = salto de línea.
#   Sirve cuando el cursor quedó pegado al prompt de un input()
#   que nunca recibió Enter (caso Ctrl-D): f"\nAdieu, adieu, a..."
#
# El formato va donde el valor TODAVÍA ES NÚMERO.
#
# LOS FLOATS MIENTEN:
#   0.07 * 100  ->  7.000000000000001
# El error aparece SOLO CON ALGUNOS NÚMEROS -> probar con un caso no alcanza.
# REGLA: todo número calculado que se MUESTRA, va formateado.

# ----------------------------------------------------------
# 2.6 print()
# ----------------------------------------------------------
# print(a, b)             separa con un espacio
# print(a, b, sep="_")    el sep va ENTRE los argumentos
# print("x", end="")      no salta de línea al final
# print()                 imprime una línea vacía
#
# print() NO DEVUELVE NADA (devuelve None).
#   print(x.lower())   sí
#   print(x).lower()   no  -> AttributeError: 'NoneType'
#
# print(input(...)) imprime lo que el usuario escribió y lo tira.
# Si quiero usar la respuesta, la GUARDO en una variable.
#
# f-string innecesario: print(f"{value(x)}") == print(value(x))

# ----------------------------------------------------------
# 2.7 FUNCIONES
# ----------------------------------------------------------
# def NO EJECUTA NADA. Define. Nada corre hasta que alguien llama.
#
#   def convert(time):
#       ^       ^
#       nombre  parámetro = etiqueta del casillero vacío
#
# El parámetro recibe su valor EN LA LLAMADA.
# Adentro trabajo con el PARÁMETRO, nunca con el nombre de la función
# ni con variables de otra función.
#
# SI LA FUNCIÓN RECIBE UN DATO, NO LE PIDA INPUT ADENTRO.
# Un input() adentro PISA lo que le mandaron, y además cuelga los tests
# (el test no tipea nada: la función se queda esperando para siempre).
# Me pasó en tip, interpreter, meal, generate_integer, shorten.
#
# LLAMAR ES UNA CALCULADORA — necesita las tres partes:
#   resultado  =  convert( lo_que_le_paso )
#      ↑            ↑            ↑
#   guardo       la llamo    le doy el dato
# Sin el "resultado =" el valor se pierde.
#
# Y NO LLAMAR DOS VECES A LA MISMA FUNCIÓN por descuido:
#   shorten(word)                    <- calcula y tira
#   print(f"Output: {shorten(word)}")<- vuelve a calcular
# La primera línea sobra.
#
# EL "=" SE LEE DE DERECHA A IZQUIERDA:
#   El nombre NUEVO va SIEMPRE a la izquierda.
#   nombre = convert(dato)      sí
#   convert(dato) = nombre      SyntaxError: cannot assign to function call
#
# return TERMINA LA FUNCIÓN EN EL ACTO.
#   Las líneas que siguen no corren.
#   NUNCA adentro de un loop que quiero que dé todas las vueltas.
#   return no es una función: return x, sin paréntesis.
#
# DENTRO DE UNA FUNCIÓN, PARA SALIR DE UN WHILE DE VALIDACIÓN, VA return,
# NO break. return sale del loop Y de la función, entregando el valor.
#
# return vs print
#   return -> devuelve el valor a quien llamó (para el programa)
#   print  -> muestra en pantalla (para el usuario)
#   Una función que imprime es una caja negra: NO SE PUEDE TESTEAR.
#
# SCOPE: cada función solo conoce sus propios parámetros y lo que crea.
#   Un contador creado en main() no se puede sumar desde otra función.
#   El contador vive donde vive el loop que lo hace crecer.

# ----------------------------------------------------------
# 2.8 EL PATRÓN main() + auxiliares
# ----------------------------------------------------------
#   funcion_logica  recibe, transforma, RETURN. No pide, no imprime.
#   main()          pide input, la llama, IMPRIME.
#
# Cada función UN trabajo. Si están cruzadas, no funciona.
#   convert   ENTRA "7:21" (string)  ->  SALE 7.35 (número)
#   main      no recibe nada         ->  no devuelve nada, imprime
#
# LA PRESENTACIÓN VA EN main(), NO EN LA FUNCIÓN:
#   shorten devuelve "Twttr", NO "Output: Twttr"
#   value devuelve 0, NO "$0"
#   El "Output: " y el "$" los pone el print.
#   Si la función devuelve texto decorado, el test nunca va a matchear.
#
# ¿DÓNDE VA LA NORMALIZACIÓN (.strip().casefold())?
#   ADENTRO de la función, no en main().
#   Si está en main(), la función solo anda cuando la llaman "bien
#   preparada". El test le manda "Hello customer" crudo y falla.
#   Una función que se va a testear se hace cargo de su propio input.

# ----------------------------------------------------------
# 2.9 if __name__ == "__main__":
# ----------------------------------------------------------
#   if __name__ == "__main__":
#       main()
#
# Un .py se puede EJECUTAR (python3 archivo.py) o IMPORTAR
# (otro archivo quiere usar mis funciones).
# Al importar, Python corre todo lo del nivel de afuera — incluido
# un main() suelto. Eso ROMPE los tests: al hacer "from twttr import
# shorten", el programa entero arrancaría y pediría input.
#
# La guarda hace que main() corra SOLO al ejecutar directo.
# Desde meal.py en adelante, todos los ejercicios la llevan.

# ----------------------------------------------------------
# 2.10 DECIDIR Y COMPARAR
# ----------------------------------------------------------
# ==  igual     !=  distinto     <  >  <=  >=
# and   or   not
#
# LOS TRES QUE SE CONFUNDEN:
#   is / is not    ¿son EL MISMO OBJETO?   casi nunca es lo que quiero
#   == / !=        ¿valen LO MISMO?
#   in / not in    ¿está CONTENIDO en?     membresía
#
#   letra not in "aeiou"     sí, es membresía
#   letra is not "aeiou"     SIEMPRE True. No compara lo que creo.
#
# in funciona sobre string, lista y diccionario (en el dict busca CLAVES).
#   if level in [1, 2, 3]:    mejor que dos comparaciones con > y <=
#
# CADA LADO DEL or / and TIENE QUE SER UNA COMPARACIÓN COMPLETA:
#   if x == 5 or x == 10 or x == 25:     sí
#   if x == 5 or 10 or 25:               MAL — siempre True, no avisa
#   if x in [5, 10, 25]:                 mejor que todo lo anterior
#
# NO COMPARAR CONTRA UN TIPO NI CONTRA UNA CLASE DE ERROR:
#   shorten("word") != int        siempre True. No prueba nada.
#   value(x) == TypeError         no es así como se verifica un error.
#   Para verificar que algo LANZA un error: with pytest.raises(TypeError):
#
# COMPARACIÓN ENCADENADA:
#   7 <= t <= 8   ->  (7 <= t) y (t <= 8)     "entre 7 y 8"
#   Los dos signos tienen que apuntar para el mismo lado.
#
# if / elif / else
#   Se DETIENE en la primera condición verdadera.
#   -> ordenar de lo MÁS ESPECÍFICO a lo más general.
#      startswith("hello") ANTES que startswith("h"), o "hello" nunca
#      llega a su rama.
#   Con ifs sueltos, Python evalúa todos. Si son excluyentes, elif.

# ----------------------------------------------------------
# 2.11 LOOPS
# ----------------------------------------------------------
# for    recorrer algo que YA TENGO, o repetir un número CONOCIDO de veces
# while  repetir MIENTRAS una condición sea verdadera
#        (no sé de antemano cuántas vueltas van a ser)
#
#   for c in s:              cada carácter
#   for _ in range(3):       3 vueltas, no me importa el número
#   for i in range(len(lista)):   cuando necesito el índice
#
# EL NOMBRE DESPUÉS DEL for ES DEL LOOP. Python le mete el valor de cada
# vuelta encima. Si uso ahí una variable que ya tenía, la pierdo:
#   for result in range(3):   <- pisa mi variable result
#   for _ in range(3):        <- así
#
# WHILE — LA REGLA DE ORO
#   1. La variable de la condición nace ANTES del loop.
#   2. Adentro del loop, algo LA MODIFICA.
#   3. Si no, es infinito. Se corta con ⌃+C.
#
#   Corolario: si lo que se repite es PREGUNTAR, el input() va ADENTRO.
#   Un input arriba del while = loop infinito garantizado.
#
# DOS FASES = DOS LOOPS, no uno.
#   Si un programa pide una cosa y después otra en ciclo (level, y después
#   guesses), son dos while separados uno abajo del otro. Meterlos en el
#   mismo loop hace que vuelva a preguntar lo primero cada vuelta.
#
# LAS TRES PALABRAS QUE SE CONFUNDEN:
#   pass      "acá no hago nada"  -> y SIGUE con la línea de abajo
#   continue  "abandono esta vuelta" -> salta al principio del loop
#   break     "abandono el loop entero"
#
#   Un pass donde va un continue deja que el código siga bajando
#   y ejecute lo que yo quería saltear. Es un bug silencioso.
#
#   En un while True, si no hay return ni break, el loop vuelve arriba
#   SOLO. No hace falta escribir nada para "volver a preguntar".
#
# += y -=   incrementar / decrementar. Con números suma, con strings pega.

# ----------------------------------------------------------
# 2.12 LISTAS
# ----------------------------------------------------------
# lista = ["Luru", "Kike", "Botto"]
#
#   lista[0]        primer elemento
#   lista[0:3]      un pedazo (la derecha se excluye)
#   len(lista)      cuántos
#   x in lista      ¿está?
#   lista.append(x) agrega al final — MODIFICA la lista, devuelve None
#
# " ".join(lista)   une los elementos con ese separador.
#   join es método del SEPARADOR, no de la lista.
#   lista.join(...)  ->  AttributeError: 'list' object has no attribute 'join'
#
# print(lista)        imprime la lista entera con corchetes y comillas
# for x in lista:     imprime uno por línea

# ----------------------------------------------------------
# 2.13 DICCIONARIOS
# ----------------------------------------------------------
# Guardan pares CLAVE : VALOR. Se buscan por clave, no por posición.
#
#   fruits = {"Apple": 130, "Banana": 110}
#
#   fruits["Apple"]        -> 130      CORCHETES, no paréntesis
#   fruits("Apple")        -> TypeError: 'dict' object is not callable
#   fruits["Mango"]        -> KeyError (la clave no existe: explota)
#   "Apple" in fruits      -> True     (pregunta por CLAVES)
#   fruits.get("Mango")    -> None     (no explota)
#
# LAS CLAVES NO SE REPITEN. El valor nuevo pisa al viejo.
#
# DICCIONARIOS ANIDADOS (lo que devuelve una API):
#   respuesta = {"data": {"id": "bitcoin", "priceUsd": "323186.4"}}
#   respuesta["data"]["priceUsd"]   -> "323186.4"
#
#   Cada corchete se cierra antes de abrir el siguiente.
#   Si me quedo un nivel corto, obtengo el dict de adentro, no el valor.
#   -> print() del diccionario entero ANTES de escribir la navegación.
#
# Recorrerlo da las CLAVES:
#   for nombre in fruits:
#       print(nombre, fruits[nombre])
#
# Si quiero UN valor de UN diccionario, NO va ningún for. El for es para
# recorrer varios.
#
# LISTA DE DICCIONARIOS — cuando cada item tiene VARIOS atributos:
#   amigos = [{"name": "Luru", "casa": "Lapis"}, ...]
#   for amigo in amigos:
#       print(amigo["name"])
#   Es un dataframe. El dict plano es un VLOOKUP.
#
# None = "no hay valor". No es 0 ni "" ni False.

# ----------------------------------------------------------
# 2.14 TRY / EXCEPT
# ----------------------------------------------------------
#   try:
#       <lo que puede romperse>
#   except <TipoDeError>:
#       <qué hacer con ESE error>
#   else:
#       <corre SOLO si no hubo ninguna excepción>
#
# EL try PROTEGE SOLO LAS LÍNEAS INDENTADAS ADENTRO.
# Si la línea que puede romper quedó afuera, el except no se entera
# y el programa revienta igual. Me pasó dos veces (game, get_level).
#
# El try envuelve SOLO lo que puede fallar. Envolver de más hace que
# el except atrape cosas que yo quería manejar de otra forma.
#
# VARIOS ERRORES EN UN MISMO except: un solo paréntesis, coma en el medio.
#   except (ValueError, IndexError):        sí
#   except (ValueError) (IndexError):       SyntaxError
#
# VARIOS except, UNO POR ERROR, cada uno con SU reacción:
#   except KeyError:
#       pass        <- item inválido: ignorar y volver a preguntar
#   except EOFError:
#       break       <- Ctrl-D: salir del loop
#
# Python usa el PRIMER except que coincida.
# Meter todos los errores en un solo except les da a todos la misma
# reacción. Ese fue mi bug en taqueria.
#
# UN except QUE HACE pass SOBRE UN ERROR REAL ME ESCONDE LA CAUSA.
#   Si el requests.get falla y hago pass, después explota en otro lado
#   con NameError y el traceback apunta a la línea equivocada.
#   Para errores que no puedo manejar: sys.exit("mensaje").
#
# NO listar errores que no pueden pasar. Un except requests.RequestException
# alrededor de código que no toca la red no se activa nunca.

# ----------------------------------------------------------
# 2.15 try/except  vs  if       (la distinción que importa)
# ----------------------------------------------------------
# try/except  atrapa lo que ROMPE.
#     "cat"      -> ValueError al convertir
#     sys.argv[1] sin argumento -> IndexError
#     "3/0"      -> ZeroDivisionError
#
# if          maneja lo que ANDA PERO NO SIRVE.
#     "4/3"  -> 1.33 es un número válido, pero el enunciado lo rechaza.
#     "-5"   -> es un número perfecto, pero un guess negativo no vale.
#     len(sys.argv) < 2  -> se cuenta ANTES de intentar leer el índice.
#
# AL VALIDAR UN RANGO, MIRAR LOS DOS EXTREMOS.
# El caso raro que no se me ocurre probar es el que rompe el check50.

# ----------------------------------------------------------
# 2.16 ERRORES COMO SEÑAL, NO COMO FALLA
# ----------------------------------------------------------
# EOFError = Ctrl-D = "no hay más entrada".
# No es un error del usuario: es cómo se avisa que terminó.
# Se atrapa con except y se sale con break.
#
# Ctrl-D  -> termina la entrada (EOFError)
# Ctrl-C  -> cancela el programa (KeyboardInterrupt)
#
# Detalle: cuando el usuario corta con Ctrl-D, el prompt del input()
# ya se imprimió y nunca recibió Enter. Mi salida sale pegada a él.
# Por eso el "\n" al principio del print final.

# ----------------------------------------------------------
# 2.17 LIBRERÍAS, MÓDULOS Y PAQUETES     [nuevo · semana 3]
# ----------------------------------------------------------
# módulo   = un archivo .py con funciones reutilizables
# paquete  = módulos organizados en una carpeta (lleva un __init__.py)
# librería estándar = viene con Python (random, statistics, sys, json, os)
# paquete de terceros = hay que instalarlo (requests, pytest, cowsay)
#
# pip3 = el gestor que instala paquetes desde PyPI (pypi.org).
#
# DOS FORMAS DE IMPORTAR:
#   import random              -> uso random.choice(...)
#   from random import choice  -> uso choice(...)
# La segunda trae solo lo que nombro. Es la que uso para mis propios
# archivos en los tests: from twttr import shorten
#
# LA STANDARD LIBRARY QUE YA USÉ:
#   random.choice(lista)        un elemento al azar
#   random.randint(a, b)        entero entre a y b, LOS DOS INCLUIDOS
#   random.randrange(a, b)      entero entre a y b-1
#   random.shuffle(lista)       mezcla EN EL LUGAR (no devuelve nada)
#   statistics.mean(lista)      promedio
#   json.dumps(obj, indent=2)   imprime un JSON legible
#
# KEYWORD ARGUMENTS: argumentos con nombre, para no depender del orden.
#   print(a, b, sep="_")
#   emoji.emojize(texto, language="alias")
#   figlet.setFont(font=elegida)

# ----------------------------------------------------------
# 2.18 sys.argv — ARGUMENTOS DE LÍNEA DE COMANDOS   [nuevo]
# ----------------------------------------------------------
# Lo que escribo después del nombre del archivo al correrlo:
#   python3 bitcoin.py 2.5
#
# sys.argv es una LISTA de strings:
#   sys.argv[0]  -> "bitcoin.py"     el nombre del archivo
#   sys.argv[1]  -> "2.5"            el primer argumento REAL
#   sys.argv[1:] -> todos los argumentos, sin el nombre del archivo
#
# len(sys.argv) CUENTA INCLUYENDO el nombre del archivo.
#   una llamada correcta con 1 argumento -> len == 2
#   error cuando len < 2
#
# ORDEN DE LAS VALIDACIONES:
#   1. ¿existe el argumento?   if len(sys.argv) < 2   <- ANTES de leer [1]
#   2. ¿sirve el argumento?    try: float(sys.argv[1])
#   Al revés, el IndexError revienta antes de llegar al chequeo.
#
# sys.exit("mensaje")  imprime el mensaje y termina el programa.

# ----------------------------------------------------------
# 2.19 APIs, requests Y JSON       [nuevo · semana 3]
# ----------------------------------------------------------
# API = una puerta que un servidor deja abierta para que otros PROGRAMAS
# le pidan datos, en vez de para personas con un navegador.
# Mi código hace lo mismo que Chrome; lo que vuelve no está pensado
# para que lo lea yo, sino para que lo use el programa.
#
#   import requests
#   respuesta = requests.get("https://...")
#
# LA URL ES UN STRING. Va entre comillas, y con https:// adelante.
# Sin el esquema -> MissingSchema (que es un RequestException).
#
# Lo que devuelve get() es un OBJETO Response, NO un diccionario:
#   respuesta["clave"]       -> TypeError: 'Response' object is not subscriptable
#   datos = respuesta.json() -> ESTO sí es un diccionario
#
# JSON = JavaScript Object Notation. Es un formato de TEXTO para
# intercambiar datos entre computadoras que no comparten lenguaje.
# Se PARECE a un diccionario pero es texto: por eso existe .json(),
# que traduce. Y por eso un número puede llegar como "323186.4",
# con comillas, y hay que pasarlo por float().
#
# CÓDIGOS DE ESTADO:
#   200  OK, los datos vienen adjuntos
#   401  Unauthorized: falta la key, está mal, o la borré
#   429  Too Many Requests: me pasé del límite del plan
#
# Que el pedido no reviente NO significa que salió bien.
#
# EL FLUJO COMPLETO:
#   1. validar el argumento
#   2. try: requests.get(url)  /  except requests.RequestException: sys.exit(...)
#   3. datos = respuesta.json()
#   4. print(datos) para VER la estructura antes de navegarla
#   5. sacar el valor con corchetes encadenados
#   6. convertir a número
#   7. formatear para mostrar
#
# Para explorar el JSON sin escribir código: pegar la URL en el navegador.

# ----------------------------------------------------------
# 2.20 UNIT TESTS Y pytest      [nuevo · semana 3]
# ----------------------------------------------------------
# Un test es "dado ESTE input, espero ESTE output". Es la base literal
# de las evals del mes 2.
#
# assert  afirma que algo es True.
#   Si es True, no pasa nada. Si es False -> AssertionError.
#
#   assert shorten("Twitter") == "Twttr"
#
# pytest = programa que corre automáticamente todas las funciones que
# empiezan con test_ y me da un reporte, en vez de frenar en el primero.
#   pip3 install pytest        (con el venv activo)
#   pytest test_archivo.py
#
# ESTRUCTURA DE UN ARCHIVO DE TEST:
#   from twttr import shorten          <- importo la función a probar
#
#   def test_minusculas():
#       assert shorten("twitter") == "twttr"
#
#   def test_mayusculas():
#       assert shorten("TWITTER") == "TWTTR"
#
# UN CASO POR FUNCIÓN. Si meto todos los asserts en una sola función,
# el primer fallo corta y no veo los demás.
#
# UN TEST TIENE QUE PODER FALLAR.
#   assert shorten("word").isalpha()     pasa aunque la función no haga nada
#   assert shorten("word") != int        SIEMPRE True. No prueba nada.
#   assert shorten("Twitter") == "Twttr" ESTO es un test.
# Si no hay un == contra un valor que escribí YO a mano, no estoy midiendo.
#
# with pytest.raises(TypeError):   para verificar que algo LANZA un error
#     shorten(5)
#
# CUANDO UN TEST FALLA, PUEDE SER EL CÓDIGO **O MI EXPECTATIVA**.
#   "MuRcIElaGO" -> yo escribí "MRclg", lo correcto era "MRclG".
#   El rojo era mío. Calcular el resultado esperado a mano, con cuidado.
#
# TIPOS: 0 y "$0" NO son iguales. Si cambio lo que devuelve la función,
# tengo que cambiar los dos lados: el código Y los tests.
#
# Para que un archivo sea testeable: la lógica en una función que RECIBE
# y DEVUELVE, sin input() ni print() adentro. Ver 2.8.
#
# check50 de un test (test_twttr, test_bank) NO prueba mi función:
# corre MIS TESTS contra versiones rotas a propósito, y verifica que
# los detecten. Un test flojo sale en rojo ahí.


# ##########################################################
# ##########################################################
#  PARTE 3 · PATRONES QUE SE REPITEN
# ##########################################################
# ##########################################################

# ----------------------------------------------------------
# 3.1 EL ACUMULADOR      (camel, twttr, professor)
# ----------------------------------------------------------
#   resultado = ""              <- AFUERA del loop. Nace vacío.
#   for letra in palabra:
#       resultado += algo       <- ADENTRO. Crece cada vuelta.
#   print(resultado)            <- AFUERA, después. UN solo print.
#
# Si la variable nace ADENTRO del loop, se reinicia cada vuelta.
#
# El VALOR INICIAL define qué tipo de acumulador es:
#   texto = ""   acumula texto        conteo = 0   cuenta
#
# EL ERROR QUE MÁS ME COSTÓ:
#   poner print() adentro del loop.
#   El if NO decide qué imprimir -> decide QUÉ AGREGAR a la variable.

# ----------------------------------------------------------
# 3.2 LA BANDERA         (plates, professor)
# ----------------------------------------------------------
# Una variable booleana que RECUERDA algo del loop para usarlo DESPUÉS.
#
#   correcto = False            <- afuera del loop interno
#   for _ in range(3):
#       ...
#       if acertó:
#           correcto = True     <- la prendo
#           score += 1
#           break
#   if correcto == False:       <- al salir, sé POR QUÉ salí
#       print(la respuesta)
#
# Un loop por sí solo no me dice si terminó por éxito o por agotarse.
# La bandera es lo que distingue los dos finales.
#
# Una bandera que se prende pero NUNCA SE CONSULTA no sirve de nada.

# ----------------------------------------------------------
# 3.3 "BUSCÁ EL FALLO"   (plates)
# ----------------------------------------------------------
# Cuando TODAS las condiciones deben cumplirse:
#
#   if <regla 1 falla>: return False
#   if <regla 2 falla>: return False
#   return True                      <- solo se alcanza si sobrevivió todo
#
# Cada if describe el CASO MALO y sale temprano.
# UN SOLO return True, al final.
#
# Al revés (cada regla devuelve True) alcanza con cumplir UNA sola.
#
# Y una regla NO es un valor con el que comparar: es una PREGUNTA.
#   s.isalnum()  YA ES la respuesta. No se compara con nada más.

# ----------------------------------------------------------
# 3.4 NORMALIZAR PARA COMPARAR, NO PARA GUARDAR
# ----------------------------------------------------------
# El .lower() va del lado de la PREGUNTA, no del dato que voy a usar.
#
#   if letter.lower() not in "aeiou":
#       resultado += letter          <- la letra ORIGINAL, con su mayúscula
#
# Y HAY QUE NORMALIZAR LOS DOS LADOS del ==.
#
# La normalización va donde el dato ENTRA a la función que lo usa.

# ----------------------------------------------------------
# 3.5 EL DATO DEL USUARIO NO ES UNA INSTRUCCIÓN
# ----------------------------------------------------------
# Si el usuario escribe "+", eso es el TEXTO "+" guardado en una variable.
# Python no lo ejecuta. Yo tengo que MIRAR ese dato con un if y decidir.

# ----------------------------------------------------------
# 3.6 EL PROGRAMA EN FASES      (game, professor)
# ----------------------------------------------------------
# Cuando un programa tiene momentos distintos, son BLOQUES SEPARADOS,
# no un loop que hace todo:
#
#   FASE 1   while True: pedir y validar el setup -> break/return
#   UNA VEZ  lo que se decide una sola vez (el número secreto)
#   FASE 2   while/for: el ciclo principal
#
# Lo que se sortea o calcula UNA VEZ va AFUERA del loop principal.
# Adentro se re-hace cada vuelta y el objetivo cambia solo.
# (Mi bug en game: un random nuevo en cada intento.)

# ----------------------------------------------------------
# 3.7 LA FUNCIÓN TESTEABLE       [nuevo · semana 3]
# ----------------------------------------------------------
# Para poder MEDIR algo, ese algo tiene que DEVOLVER un valor.
#
#   def transformar(dato):      <- recibe, normaliza, calcula, RETURN
#   def main():                 <- input, llama, print
#
# Una función que imprime no se puede testear: no hay valor que comparar.
# Una función que pide input cuelga el test.
# Una función que devuelve texto decorado ("Output: X") nunca matchea.
#
# Este patrón es el mismo que voy a necesitar en la semana 4 para medir
# el clasificador: la parte que decide devuelve un dato, y otra capa
# lo muestra.


# ##########################################################
# ##########################################################
#  PARTE 4 · MIS ERRORES
# ##########################################################
# ##########################################################

# ----------------------------------------------------------
# 4.1 LOS QUE REPITO (por orden de tiempo perdido)
# ----------------------------------------------------------
# 1. INVENTAR SINTAXIS Y NO CORRERLA.
#    .isnum, .isfloat, .add, len(6), .split(":", ","), figlet.random,
#    random.randint sin paréntesis, lista.join()
#    Escribo 15 líneas sobre algo que nunca corrió.
#    -> REPL primero. Una línea. 30 segundos.
#
# 2. CORRER SIN GUARDAR. La bolita ● tiene que ser X. ⌘+S.
#
# 3. ESTAR EN LA CARPETA EQUIVOCADA, o con el venv desactivado.
#    Leer la palabra antes del %, y si está el (.venv).
#
# 4. == cuando quiero =, o los lados del = invertidos.
#
# 5. USAR LA VARIABLE EQUIVOCADA adentro del loop, o dejar que el for
#    me pise una variable (for result in range(3)).
#
# 6. LÍNEAS QUE CALCULAN Y TIRAN EL RESULTADO.
#    z != 0  /  s.isalnum()  /  shorten(word)  /  (input(...))  sueltas.
#    Para que una condición HAGA algo tiene que estar en un if.
#    Para que un valor sobreviva tiene que guardarse con =.
#
# 7. VARIABLES SUELTAS EN UNA LÍNEA queriendo decir "volvé a preguntar".
#    Escribir `n` solo no hace nada. En un while True, volver arriba
#    es NO hacer nada; para saltear el resto de la vuelta va continue.
#
# 8. pass DONDE VA continue. pass sigue bajando y ejecuta lo que
#    quería saltear. Bug silencioso.
#
# 9. LA LÍNEA RIESGOSA AFUERA DEL try. El except entonces no sirve.
#
# 10. LA FUNCIÓN QUE PIDE input() ADENTRO cuando ya recibió el dato.
#     Pisa el parámetro y cuelga los tests.
#
# 11. LA FUNCIÓN QUE DEVUELVE TEXTO DECORADO ("Output: X", "$0")
#     en vez del valor pelado.
#
# 12. NORMALIZAR EN main() Y NO EN LA FUNCIÓN. El test le manda el dato
#     crudo y falla.
#
# 13. EXPECTATIVA MAL CALCULADA EN UN TEST. El rojo puede ser mío.
#
# 14. TESTS QUE NO PUEDEN FALLAR (comparar contra un tipo, o pedir
#     algo que se cumple siempre).
#
# 15. NORMALIZAR UN SOLO LADO de la comparación.
#
# 16. PONER EL FORMATO AFUERA de las llaves del f-string.
#
# 17. VALORES ESCRITOS A MANO que deberían ser variables.
#     randrange(1, 11) cuando el usuario eligió el nivel.
#
# 18. MEZCLAR ESCALAS (0.75 vs 75) o TIPOS (0 vs "$0").
#
# 19. UN SOLO except PARA ERRORES QUE NECESITAN REACCIONES DISTINTAS,
#     o un except con pass que esconde la causa real.
#
# 20. OLVIDARME EL https:// en una URL.

# ----------------------------------------------------------
# 4.2 QUÉ SIGNIFICA CADA ERROR
# ----------------------------------------------------------
# LEER DE ABAJO HACIA ARRIBA. La última línea dice QUÉ,
# las de arriba DÓNDE, y el ^^^^ marca la posición exacta.
#
# NameError: name 'X' is not defined
#   Python leyó X como variable y no existe.
#   O es una palabra suelta sin comillas, o es de OTRA función,
#   o la línea que la creaba está adentro de un except que hizo pass.
#
# ModuleNotFoundError: No module named 'dotenv'
#   La librería no está instalada EN EL PYTHON QUE ESTOY USANDO.
#   Casi siempre: la instalé afuera del venv y corro adentro (o al revés).
#
# AttributeError: 'str' object has no attribute 'isnum'
#   Ese método no existe PARA ESE TIPO, o me lo inventé.
#
# AttributeError: 'NoneType' object has no attribute 'strip'
#   Le apliqué un método al resultado de algo que devuelve None:
#   print(), o .append() de una lista.
#
# AttributeError: 'list' object has no attribute 'join'
#   join es del separador: " ".join(lista), no lista.join().
#
# UnboundLocalError: cannot access local variable 'x'
#   La variable se crea SOLO adentro de un if que no se cumplió.
#
# TypeError: 'dict' object is not callable
#   Usé paréntesis donde van corchetes. fruits("Apple") -> fruits["Apple"]
#
# TypeError: 'Response' object is not subscriptable
#   Le puse corchetes al objeto de requests. Primero .json().
#
# TypeError: 'type' object is not iterable
#   Le pasé un TIPO (int) donde iba un valor. shorten(int) -> shorten("5")
#
# TypeError: float() argument must be a string or a real number, not 'dict'
#   Me quedé un nivel corto navegando el JSON. Falta otro corchete.
#
# TypeError: object of type 'int' has no len()
#   len() mide cosas con longitud. Un número no tiene.
#
# TypeError: unsupported operand type(s) for *: 'dict' and 'float'
#   Estoy operando con el contenedor, no con el valor de adentro.
#
# TypeError: '<=' not supported between 'int' and 'str'
#   Comparo un número con un string. Falta convertir.
#
# ValueError: invalid literal for int() with base 10: 'cat'
#   Quise convertir a número algo que no lo es.
#   Se atrapa con except ValueError.
#
# ValueError: not enough values to unpack
#   Los nombres a la izquierda del = no coinciden con lo que devolvió split.
#
# IndexError: list index out of range
#   Pedí una posición que no existe. Clásico: sys.argv[1] sin argumento.
#   -> chequear len() ANTES de leer el índice.
#
# KeyError: 'Mango'
#   Esa clave no está en el diccionario.
#
# AssertionError: assert 'MRclG' == 'MRclg'
#   Un test falló. Pytest muestra el diff: - lo esperado, + lo obtenido.
#   Revisar si el error está en el código O en mi expectativa.
#
# requests.exceptions.MissingSchema
#   A la URL le falta https://
#
# EOFError                Ctrl-D. Fin de la entrada, no una falla.
# KeyboardInterrupt       Ctrl-C. Cancelé el programa a mano.
#
# SyntaxError: cannot assign to function call here
#   Puse la llamada a la izquierda del =.
#
# SyntaxError: invalid syntax
#   Falta paréntesis, coma, comillas o los dos puntos.
#   También: except (A) (B): en vez de except (A, B):
#
# ZeroDivisionError       División por cero.
#
# command not found: X
#   zsh no conoce X. bitcoin.py no es un comando: python3 bitcoin.py
#
# can't open file '...': No such file or directory
#   Estoy parado en otra carpeta. Leer el prompt y hacer cd.


# ##########################################################
# ##########################################################
#  PARTE 5 · RUTINA
# ##########################################################
# ##########################################################

# ----------------------------------------------------------
# 5.1 CADA EJERCICIO DE CS50P
# ----------------------------------------------------------
# 1. Leer la página ENTERA antes de escribir.
#    La consigna está en "Implementation Details", arriba del Demo.
# 2. Escribir las reglas en una lista, cada una como PREGUNTA.
# 3. Mirar el Demo carácter por carácter: espacios, mayúsculas, dos puntos.
#    check50 compara LITERAL. Copio el texto del enunciado.
# 4. cd a la carpeta. Archivo con el nombre EXACTO. Venv activo si hace falta.
# 5. UNA regla / UN paso por vez. Correr. Verificar. Recién ahí la siguiente.
# 6. Probar YO los casos del enunciado ANTES de check50,
#    incluyendo los "feos": el que se pasa, el vacío, el negativo, el cero.
# 7. check50 cs50/problems/2022/python/<ejercicio>
# 8. Si sale rojo, leer QUÉ input falló. Correr ese input a mano.
# 9. submit50 (check50 no entrega nada)

# ----------------------------------------------------------
# 5.2 SI EL EJERCICIO PIDE TESTS
# ----------------------------------------------------------
# 1. El archivo a probar y el test van EN LA MISMA CARPETA.
# 2. Reestructurar primero: la lógica en una función que recibe y devuelve.
#    Normalización adentro de esa función.
# 3. Un test por caso, cada uno en su propia def test_algo().
# 4. Calcular a mano el resultado esperado. Con cuidado.
# 5. pytest test_archivo.py
# 6. Antes de darlo por bueno: preguntarme si cada test PODRÍA fallar.

# ----------------------------------------------------------
# 5.3 CHECKLIST ANTES DE PEDIR AYUDA
# ----------------------------------------------------------
# [ ] ¿Guardé? (⌘+S — bolita ● -> X)
# [ ] ¿Corrí el código, o solo lo escribí?
# [ ] ¿Verifiqué en el REPL los métodos que usé?
# [ ] ¿Estoy en la carpeta correcta? ¿Está el (.venv)?
# [ ] ¿Uso la variable de ESTA vuelta del loop, o la de afuera?
# [ ] ¿Hay alguna línea que calcula algo y no lo guarda?
# [ ] ¿El acumulador/bandera nace AFUERA del loop?
# [ ] ¿Lo que se decide una vez está afuera del loop?
# [ ] ¿La línea que puede romper está ADENTRO del try?
# [ ] ¿La indentación empareja los if/else y los loops como quiero?
# [ ] ¿Cada función DEVUELVE, o solo imprime?
# [ ] ¿La función se hace cargo de normalizar su propio input?
# [ ] ¿Normalicé los dos lados de la comparación?
# [ ] ¿Estoy comparando la misma escala y el mismo TIPO?
# [ ] ¿Validé los DOS extremos del rango?
# [ ] ¿Probé con más de un caso, incluyendo uno "feo"?

# ----------------------------------------------------------
# 5.4 SI ME TRABO (en este orden)
# ----------------------------------------------------------
# 0-5 min    Leer el error ENTERO, de abajo hacia arriba.
# 5-15 min   print() de las variables justo antes de la línea que falla.
# 15-20 min  Buscar el mensaje de error textual en Google.
# 20+ min    Preguntar: "no me des el código, explicame por qué pasa
#            y decime en qué línea mirar".
# NUNCA      Copiar y pegar algo que no entiendo.
#
# SI SE ENREDA FEO — el método que funcionó:
#   Borrar todo y volver a DOS líneas. Correr. Verificar.
#   Agregar UNA línea. Correr. Verificar.
#
# Y SI ESTOY QUEMADO: cerrar el día. Commitear aunque esté a medias.
# Un loop mal escrito a las 11 de la noche sale en cinco minutos
# al día siguiente.

# ----------------------------------------------------------
# 5.5 CERRAR EL DÍA
# ----------------------------------------------------------
#   cd ~/ai-plan
#   git status            <- que NO aparezcan .env ni .venv
#   git add .
#   git commit -m "dia N: lo que hice"
#   git push
#
# Aunque esté roto o incompleto. Regla del plan.
#
# La guía se actualiza UNA VEZ POR SEMANA, los viernes.