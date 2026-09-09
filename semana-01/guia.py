# ==========================================================
#  GUÍA PERSONAL — Axel · MacBook Air (macOS, zsh)
#  Cheat sheet de terminal, Python y mis errores recurrentes.
#  Se actualiza cada vez que aprendo o rompo algo nuevo.
# ==========================================================


# ##########################################################
#  0. MIS ERRORES MÁS FRECUENTES
# ##########################################################
#
# 1. CORRER SIN GUARDAR.
#    La BOLITA ● en la pestaña = sin guardar. Tiene que ser X.
#    El archivo en disco queda vacío o viejo.
#    -> ⌘+S ANTES de correr. Siempre. Aunque esté seguro.
#
# 2. ESTAR EN LA CARPETA EQUIVOCADA.
#    La palabra antes del % es la carpeta actual. LEERLA.
#
# 3. VARIAS TERMINALES en carpetas distintas y saltar entre ellas.
#    -> UNA sola terminal. Si sobran, tacho 🗑.
#
# 4. DOS ARCHIVOS CON EL MISMO NOMBRE en lugares distintos.
#    El breadcrumb arriba del editor dice cuál estoy editando.
#
# 5. ESCRIBIR EL INPUT DEL PROGRAMA en la terminal cuando el
#    programa ya terminó. Si volvió el %, terminó. No espera nada.
#
# 6. INVENTAR MÉTODOS (.add() no existe). Buscar, no adivinar.
#
# 7. NORMALIZAR UN SOLO LADO de la comparación.
#
# 8. PONER EL FORMATO AFUERA de las llaves del f-string.


# ##########################################################
#  1. ENTORNO Y TERMINAL
# ##########################################################

# ----------------------------------------------------------
# ¿DÓNDE ESTOY?
# ----------------------------------------------------------
# El prompt lo dice:
#   axelefron@MacBook-Air-de-Axel-2 indoor %
#                                   ^^^^^^  <- carpeta actual
#
# pwd            ruta completa donde estoy
# ls             lista archivos y carpetas de acá
# cat archivo    muestra el contenido REAL en disco (no el del editor)

# ----------------------------------------------------------
# MOVERME
# ----------------------------------------------------------
# cd carpeta                         entro a una subcarpeta
# cd ..                              subo un nivel
# cd ~/ai-plan/semana-01/indoor      voy directo (~ = mi carpeta personal)
# cd ind + TAB                       autocompleta el nombre

# ----------------------------------------------------------
# % vs >>>   (los dos mundos)
# ----------------------------------------------------------
# %    = terminal (zsh). Comandos del sistema: ls, cd, python3, check50
# >>>  = estoy DENTRO de Python. Solo entiende Python.
#        Salir: exit()  o  ⌃+D
#
# Si la terminal abre en >>> sin que yo haga nada, es el perfil Python.
# Quiero zsh: Terminal -> New Terminal (NO "With Profile").

# ----------------------------------------------------------
# EN MAC ES python3 Y pip3
# ----------------------------------------------------------
# python3 archivo.py     correr un programa
# pip3 install paquete   instalar una librería
# python / pip a secas   -> NO usar (apuntan al viejo del sistema)

# ----------------------------------------------------------
# CORRER UN ARCHIVO
# ----------------------------------------------------------
# python3 indoor.py      SÍ (el intérprete corre, el archivo es el input)
# indoor.py              NO -> "command not found", no es un ejecutable
#
# Botón ▶ Run: usa la ruta completa del archivo abierto.
# Terminal:    usa la carpeta donde estoy parado.
# Cuando uno anda y el otro no, es porque no coinciden.

# ----------------------------------------------------------
# ARCHIVOS Y CARPETAS
# ----------------------------------------------------------
# mkdir nombre       nueva carpeta
# touch archivo.py   nuevo archivo (o ícono "hoja +" en el Explorer)
# rm archivo.py      borrar (NO va a la papelera: desaparece)
#
# NUNCA espacios en los nombres. Usar guion_bajo o guion-medio.
# Todo en minúscula: en un servidor Linux, Indoor != indoor.

# ----------------------------------------------------------
# ATAJOS — VS CODE
# ----------------------------------------------------------
# ⌘+S              guardar
# ⌘+Z / ⌘+⇧+Z      deshacer / rehacer
# ⌘+/              comentar-descomentar selección  <- para aislar bugs
# ⌘+⇧+P            paleta de comandos
# ⌃+`              abrir terminal (o Terminal -> New Terminal)
# ⌃+ -             volver a donde estaba el cursor antes
# ⇧+Enter          correr solo la selección

# ----------------------------------------------------------
# ATAJOS — TERMINAL
# ----------------------------------------------------------
# ↑          comando anterior (no reescribir python3 archivo.py)
# ⌃+U        borrar la línea que estoy escribiendo
# ⌃+C        cancelar lo que esté corriendo o colgado
# TAB        autocompletar nombres


# ##########################################################
#  2. PYTHON — FUNDAMENTOS
# ##########################################################

# ----------------------------------------------------------
# FUNCIÓN vs MÉTODO
# ----------------------------------------------------------
# función -> el valor va ADENTRO:   len(texto)
# método  -> va PEGADO con punto:   texto.strip()
#
# Los métodos son de un TIPO: los de texto solo andan en texto.
# NINGUNO modifica el original: todos DEVUELVEN algo nuevo.
#   texto.strip()          -> calcula y tira el resultado
#   texto = texto.strip()  -> lo guarda

# ----------------------------------------------------------
# TIPOS Y CONVERSIÓN
# ----------------------------------------------------------
# input() SIEMPRE devuelve str, aunque el usuario escriba un número.
# "42" (texto) y 42 (número) son cosas distintas. Nunca son iguales.
#
# int(x)      a entero      int("42") -> 42     (int("2.5") explota)
# float(x)    a decimal     float("2.5") -> 2.5
# str(x)      a texto       str(42) -> "42"
#             str() con UN argumento convierte.
#             str() con DOS hace otra cosa (decodificar bytes). NO concatena.
# type(x)     qué tipo es. Útil para debuggear.

# ----------------------------------------------------------
# OTRAS BUILT-IN
# ----------------------------------------------------------
# print(x)        muestra en pantalla. NO devuelve nada (None).
# input("msg")    pide texto al usuario.
# len(x)          cuántos caracteres/elementos tiene
# round(x, n)     redondea a n decimales (para CALCULAR, no para mostrar)

# ----------------------------------------------------------
# MÉTODOS DE TEXTO (str)
# ----------------------------------------------------------
# LIMPIAR / NORMALIZAR (antes de comparar)
#   .strip()        saca espacios de los EXTREMOS
#                   OJO: NO saca los espacios del medio.
#   .lower()        todo a minúscula
#   .casefold()     como lower pero más agresivo (otros idiomas)
#   .upper()        todo a MAYÚSCULA
#   .title()        Primera Letra De Cada Palabra
#                   (se rompe con "McDonald" -> "Mcdonald")
#   .capitalize()   Solo la primera letra de todo el texto
#
# PREGUNTAR (devuelven True o False)
#   .startswith("h")      ¿empieza con eso?
#   .endswith(".py")      ¿termina con eso?
#   "x" in texto          ¿está contenido? (operador, no método)
#
# TRANSFORMAR
#   .replace(viejo, nuevo)   cambia TODAS las apariciones
#   .count("a")              cuántas veces aparece
#   .split(",")              parte el texto en una lista
#   " ".join(lista)          une una lista en un texto
#
# ENCADENAR: cada método opera sobre el resultado del anterior.
#   texto.strip().lower().replace(" ", "-")
#
#   EL ORDEN IMPORTA: strip ANTES que replace, o los espacios de los
#   extremos ya se convirtieron en guiones y no se pueden sacar.
#
# Para ver todos los métodos de texto: dir("") en el intérprete.

# ----------------------------------------------------------
# F-STRINGS (mostrar)
# ----------------------------------------------------------
# ANATOMÍA:
#
#   f"Total: {percent_margin:.1f}%"
#    │       │              │    │
#    │       │              │    └─ afuera de {} = texto literal
#    │       │              └────── ADENTRO: dos puntos + formato
#    │       └───────────────────── adentro: la expresión a mostrar
#    └───────────────────────────── la f que activa las llaves
#
# REGLA: adentro de {} se calcula. Afuera se imprime tal cual.
# El formato SIEMPRE va adentro, después de ":".
#
# Formatos:  .1f = 1 decimal   .2f = 2 decimales (plata)   :, = miles
#
# El formato va donde el valor TODAVÍA ES NÚMERO.
# Si ya se convirtió a texto, no hay nada que formatear.

# ----------------------------------------------------------
# LOS FLOATS MIENTEN
# ----------------------------------------------------------
# 0.07 * 100  ->  7.000000000000001
# 0.6  * 100  ->  60.0        (este sale bien de casualidad)
#
# Los decimales se guardan en binario y algunos no tienen
# representación exacta (como 1/3 en decimal).
# El error aparece SOLO CON ALGUNOS NÚMEROS
#   -> probar con un caso no alcanza. Nunca probar solo con 0 o 1.
#
# REGLA: todo número calculado que se MUESTRA, va formateado.


# ##########################################################
#  3. MIS FUNCIONES
# ##########################################################
#
# def NO EJECUTA NADA. Define. Nada corre hasta que alguien llama.
# Por eso main() al final del archivo es obligatorio.
#
#   def slugify(text):
#       ^        ^
#       nombre   parámetro = etiqueta del casillero vacío
#
# El parámetro recibe su valor EN LA LLAMADA, lo pone quien llama.
# Adentro trabajo con el PARÁMETRO (text), nunca con el nombre
# de la función.
#
# SCOPE: el parámetro solo existe adentro de la función.
#        Afuera -> NameError. Por eso dos funciones pueden usar
#        el mismo nombre de parámetro sin pisarse.
#
# return -> devuelve el resultado a quien llamó (para el programa)
# print  -> muestra en pantalla (para el usuario)
# Asignar a una variable local NO es devolver. Esa variable muere.
#
# Vocabulario: parámetro = el nombre en el def
#              argumento = el valor real que paso al llamar

# ----------------------------------------------------------
# EL PATRÓN main() + funciones auxiliares
# ----------------------------------------------------------
#   funcion_logica  -> recibe, transforma, RETURN. No habla con nadie.
#   main()          -> pide input, la llama, IMPRIME.
#   main()          -> al final del archivo, para que algo se ejecute
#
# Se separan para poder TESTEAR la lógica sin teclado.
# No se puede testear algo que pide input e imprime.
# Sí se puede testear una función que recibe X y devuelve Y.


# ##########################################################
#  4. DECIDIR Y COMPARAR
# ##########################################################
#
# ==  igual     !=  distinto     <  >  <=  >=
# and   or   not
# x in ("a", "b", "c")  -> más limpio que x=="a" or x=="b" or x=="c"

# ----------------------------------------------------------
# if / elif / else
# ----------------------------------------------------------
# Se DETIENE en la primera condición verdadera.
# -> ordenar de lo MÁS ESPECÍFICO a lo más general.
#    Si "hello" va después de "h", nunca se alcanza.

# ----------------------------------------------------------
# match / case
# ----------------------------------------------------------
# Para comparar UN valor contra varias opciones fijas.
#   case "a" | "b":   el | es un OR: varios valores, misma respuesta
#   case _:           el resto (como un else)

# ----------------------------------------------------------
# NORMALIZAR ANTES DE COMPARAR
# ----------------------------------------------------------
# input(...).strip().casefold()  -> el usuario puede escribir como quiera
#
# PERO: hay que normalizar LOS DOS LADOS del ==.
#   answer == "Forty two"
#      ↑           ↑
#   minúscula   mayúscula  ->  NUNCA matchea
#
# Si normalizo a minúscula, los valores de comparación van en minúscula.
# Python no toca lo que yo escribo en el código.
#
# La normalización va en UN SOLO LUGAR: donde el dato entra.
# No repartida en cada comparación.
#
# Qué NO cubre: espacios en el MEDIO, y sinónimos
# ("cuarenta y dos" no es otra forma de escribir "forty two").


# ##########################################################
#  5. ERRORES: QUÉ SIGNIFICAN
# ##########################################################
#
# command not found: X
#   zsh no conoce X. No está instalado, o no es un comando
#   (hello.py no es un comando: se corre con python3).
#
# NameError: name 'X' is not defined
#   Python leyó X como VARIABLE y no existe.
#   Una palabra suelta sin comillas nunca es texto.
#
# AttributeError: 'float' object has no attribute 'add'
#   Ese método no existe PARA ESE TIPO. O me lo inventé.
#   Los números no tienen métodos de texto.
#
# AttributeError: 'NoneType' object has no attribute 'strip'
#   Le apliqué un método al resultado de print().
#   print() NO devuelve nada.
#     print(variable.lower())   <- sí
#     print(variable).lower()   <- no
#
# TypeError: can't multiply sequence by non-int of type 'str'
#   Estoy operando con textos creyendo que son números.
#   Probablemente una función devolvió el parámetro sin convertir.
#
# SyntaxError: invalid syntax
#   Falta un paréntesis, una coma, comillas o los dos puntos.
#   Mirar el ^^^^ que marca la posición exacta.
#
# can't open file '...': No such file or directory
#   Estoy parado en otra carpeta. Leer el prompt y hacer cd.


# ##########################################################
#  6. RUTINA DE CADA EJERCICIO DE CS50P
# ##########################################################
#
# 1. Leer la página ENTERA antes de escribir.
#    La consigna está en "Implementation Details", arriba del Demo.
# 2. Mirar el Demo carácter por carácter: espacios, mensajes, mayúsculas.
# 3. cd ~/ai-plan/semana-01/<carpeta>   (mkdir si no existe)
# 4. Archivo con el nombre EXACTO que pide el enunciado.
# 5. Escribir -> ⌘+S -> python3 archivo.py
# 6. Probar YO los casos del enunciado ANTES de check50.
# 7. check50 cs50/problems/2022/python/<ejercicio>
# 8. Si sale rojo: abrir la URL que da check50. Siempre.
# 9. submit50 cs50/problems/2022/python/<ejercicio>

# ----------------------------------------------------------
# CHECKLIST ANTES DE PEDIR AYUDA
# ----------------------------------------------------------
# [ ] ¿Guardé? (⌘+S — la bolita tiene que ser X)
# [ ] ¿Estoy en la carpeta correcta? (leer el prompt)
# [ ] ¿Cada función DEVUELVE o solo asigna a una variable local?
# [ ] ¿Uso el PARÁMETRO adentro, no el nombre de la función?
# [ ] ¿El método que uso existe para ESE tipo?
# [ ] ¿El formato está adentro de las llaves y en la función correcta?
# [ ] ¿Normalicé los dos lados de la comparación?
# [ ] ¿Probé con más de un caso, incluyendo uno "feo"?

# ----------------------------------------------------------
# SI ME TRABO (en este orden)
# ----------------------------------------------------------
# 0-5 min    Leer el error ENTERO, de abajo hacia arriba.
#            La última línea dice QUÉ pasó, las de arriba DÓNDE.
# 5-15 min   print() de las variables justo antes de la línea que falla.
# 15-20 min  Buscar el mensaje de error textual en Google.
# 20+ min    Preguntar: "no me des el código, explicame por qué pasa
#            y decime en qué línea mirar".
# NUNCA      Copiar y pegar algo que no entiendo.


# ##########################################################
#  7. CERRAR EL DÍA
# ##########################################################
#
# cd ~/ai-plan
# git add .
# git commit -m "dia N: lo que hice"
# git push
#
# Aunque esté roto o incompleto: el commit es mi botón de deshacer real.
# Un commit es una FOTO congelada, no una vista en vivo.
# El link de un commit viejo muestra siempre esa foto vieja.

# ==========================================================
# 8 · CERRAR EL DÍA CON GIT
# ==========================================================

# Los 3 comandos, siempre en ~/ai-plan (verificar con pwd):
#
#   git add .
#   git commit -m "dia 4"
#   git push
#
# Qué hace cada uno:
#
# git add .        --> el "." significa "todo lo de esta carpeta hacia abajo".
#                      NO guarda nada. Pone los archivos en el staging area,
#                      que es la mesa donde armo el próximo commit.
#
# git commit -m    --> congela la foto y le pone nombre. El -m es el mensaje.
#                      Cada commit es un estado completo al que puedo volver.
#                      Devuelve un hash (ej: 64a6069) = nombre único de esa foto.
#                      El primero dice "root-commit"; los demás, "1 parent".
#
# git push         --> sube los commits a GitHub. Es el único que usa internet.
#                      Sin push, los commits existen solo en mi Mac.
#
# Por qué "git push" solo, sin "-u origin main":
#   el -u del primer push dejó fijada la relación main <-> origin/main.
#   Desde ahí, "git push" ya sabe a dónde va.

# git status --> ANTES de add. Me muestra qué ve Git como nuevo o cambiado.
#                Es el único momento barato para darme cuenta de que estoy
#                por subir algo que no quiero.

# --- El .gitignore ---
# Archivo en la RAÍZ de ai-plan (mismo nivel que semana-01), un patrón por línea:
#
#   .env
#   __pycache__/
#   .DS_Store
#
# SIN espacios adelante: Git compara el patrón tal cual, y "  .env" no coincide
# con el archivo .env. La regla queda muerta y no avisa.
#
# Por qué importa: el repo es PÚBLICO y el día 10 la API key va en .env.
# Un commit no es un archivo que borro: es una foto que queda en el historial.
# Si subo una key, la doy por perdida — la anulo y saco otra.

# Regla del plan: el día cierra con un commit, aunque el código esté roto.

# --- interpreter.py (PS1) — lo que me costó ---

# 1. UN solo input. Si el usuario escribe "1 + 1" completo,
#    los tres datos ya están adentro de ese string.
#    No preguntar tres veces.

# texto.split(" ")  --> devuelve una LISTA: ['1', '+', '1']
# a, b, c = lista   --> reparte: un nombre por elemento.
#                       Son DOS operaciones distintas: partir y repartir.
#                       Si la cantidad de nombres no coincide, falla.

# 2. Los nombres nuevos van a la IZQUIERDA del "=".
#    El "=" se lee de derecha a izquierda:
#    "calculá lo de la derecha, guardalo con el nombre de la izquierda".
#    Lo que va entre comillas es TEXTO, nunca un nombre de variable.

# 3. Python lee de arriba hacia abajo.
#    Una línea solo puede usar cosas creadas en una línea de MÁS ARRIBA.

# 4. Después del split todo es string. float() convierte UN valor,
#    no una lista. Y el operador NO se convierte: queda string
#    porque se compara con "+", "-", "*", "/".

# 5. El operador que escribe el usuario es un DATO, no una instrucción.
#    Python no lo ejecuta. Yo miro ese dato con un if y decido la cuenta.

# 6. Cada rama GUARDA en result; el print va uno solo al final.
#    Así el formato .1f se escribe una vez y no cuatro.

# 7. Una línea suelta como "z != 0" calcula y tira el resultado.
#    Para que una condición haga algo tiene que estar en un if.

# 8. check50 busca el archivo en la carpeta donde estoy parado.
#    Leer la palabra antes del % ANTES de correrlo.

# MÉTODO CUANDO ME TRABO FEO:
#    Borrar todo y volver a 2 líneas. Correr. Verificar.
#    Agregar UNA línea. Correr. Verificar.
#    Adivinar nombres de métodos (.pop, .add) es lo que más tiempo me cuesta.

# --- if __name__ == "__main__": ---
# Un archivo .py se puede EJECUTAR (python3 archivo.py) o IMPORTAR
# (otro archivo quiere usar mis funciones).
# Al importar, Python corre todo lo que está en el nivel de afuera.
# Si llamo main() suelto, se ejecuta también al importar --> rompe los tests.
# La guarda hace que main() corra SOLO cuando ejecuto el archivo directo.
# check50 importa mi archivo para probar las funciones sueltas.
# Desde meal.py en adelante, TODOS los ejercicios de CS50P la llevan.

# --- .split() otra vez (me costó 4 veces hoy) ---
# .split(sep) recibe UN separador.
# El 2do argumento es un NÚMERO (cuántos cortes), no otro separador.
# Para partir por dos separadores distintos --> dos llamadas, en dos pasos.