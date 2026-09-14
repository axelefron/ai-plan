# ==========================================================
#  GUÍA PERSONAL — Axel · MacBook Air (macOS, zsh)
#  Reescrita al cerrar la Semana 2. Actualizada con Semana 3 (Exceptions).
#  PS0, PS1, PS2 y PS3 completos.
#
#  CÓMO ESTÁ ORGANIZADA:
#    PARTE 1 · ENTORNO     terminal, VS Code, git
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
#   axelefron@MacBook-Air-de-Axel-2 problem_set_2 %
#                                   ^^^^^^^^^^^^^  carpeta actual
#
# TODOS los comandos actúan desde donde estoy parado:
#   python3 archivo.py   busca el archivo ACÁ
#   check50              busca el archivo ACÁ
#   git add .            agarra de ACÁ HACIA ABAJO, no todo el repo
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
# cd ~/ai-plan/semana-02      voy directo   (~ = /Users/axelefron)
# cd car + TAB                autocompleta
#
# cd es para CARPETAS, nunca para archivos.
#   cd ~/.../coke.py   ->  "not a directory"
# El archivo es el destino de python3, no de cd:
#   cd ~/ai-plan/semana-02/problem_set_2
#   python3 coke.py
#
# Nombres: sin espacios, sin mayúsculas. Uso guion_bajo.
# Con espacios hay que poner comillas en cada comando. Molesta siempre.

# ----------------------------------------------------------
# 1.3 % vs >>>
# ----------------------------------------------------------
# %    = terminal (zsh). ls, cd, python3, check50, git
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
#   a, b = "hola chau".split(" ")
#   "CS50"[0:2]               ->  'CS'
#   "A".isupper()             ->  True
#   5 in [5, 10, 25]          ->  True
#   abs(-10)                  ->  10
#   dir("")                   ->  TODOS los métodos de string
#
# Adivinar nombres de métodos (.isnum, .add, .pop sobre un str) es
# lo que más tiempo me costó en la semana 2. El REPL lo mata al toque.

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
# y las M del Explorer.
#
# QUÉ ES CADA COSA
#   git add      pone en el staging area. NO guarda nada todavía.
#   git commit   congela la foto. Devuelve un hash (ej: 64a6069).
#   git push     sube. El único que usa internet.
#   git restore <ruta>   RECUPERA archivos borrados, con la versión
#                        del último commit. Solo si ya estaban commiteados.
#
# Por eso commiteo seguido AUNQUE ESTÉ ROTO: es mi botón de deshacer real.
# Un commit es una foto congelada, no una vista en vivo.
#
# .gitignore (en la raíz, un patrón por línea, SIN espacios adelante):
#   .env
#   __pycache__/
#   .DS_Store
# El repo es PÚBLICO. Si subo una API key, la doy por perdida.
#
# OJO: axelefron/ai-plan (mío, git push) y me50/axelefron (CS50, submit50)
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
#   for c in s:
#       if c.isdigit():
#           if <otra cosa>:
#               return False          <- nivel 4
#           marca = True              <- nivel 3: adentro del isdigit,
#       else:                            afuera del if interno
#           ...                       <- este else es del isdigit()
#
# Cuando el programa "hace cualquier cosa" pero no tira error:
# mirar las líneas verticales de VS Code antes que la lógica.


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
# NINGUNO modifica el original: todos DEVUELVEN algo nuevo.
#   texto.strip()          calcula y tira el resultado
#   texto = texto.strip()  lo guarda
#
# Encadenar: cada método opera sobre el resultado del anterior.
#   texto.strip().lower().replace(" ", "-")
# EL ORDEN IMPORTA: strip ANTES que replace, o los espacios de los
# extremos ya se convirtieron en guiones.

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
# CONVERTIR UNO POR UNO, no la colección entera:
#   float("7:21")              explota
#   float(["1","+","1"])       explota (es una lista)
# Primero parto, después convierto cada pedazo que necesito.
# Y convierto SOLO lo que es número: el operador o el meridiano
# quedan como texto porque los voy a comparar.

# ----------------------------------------------------------
# 2.3 STRINGS — MÉTODOS
# ----------------------------------------------------------
# NORMALIZAR (antes de comparar)
#   .strip()        saca espacios de los EXTREMOS (no los del medio)
#   .lower()        todo minúscula
#   .upper()        todo MAYÚSCULA
#   .casefold()     como lower pero más agresivo
#   .title()        Primera Letra De Cada Palabra   <- para "Sweet Cherries"
#   .capitalize()   Solo la primera letra de todo   <- rompe con 2 palabras
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
# TRANSFORMAR
#   .replace(viejo, nuevo)   cambia TODAS las apariciones
#   .count("a")              cuántas veces aparece
#   .split(sep)              parte el texto y devuelve una LISTA
#   " ".join(lista)          une una lista en un texto
#
# .split() RECIBE UN SOLO SEPARADOR.
#   El segundo argumento es un NÚMERO (cuántos cortes), no otro separador.
#   NO existe forma de partir por dos separadores en una llamada.
#   Para eso: dos pasos.  "7:30 a.m." -> split(" ") -> luego split(":")

# ----------------------------------------------------------
# 2.4 STRINGS — POSICIONES Y PEDAZOS
# ----------------------------------------------------------
#   s[0]      primer carácter        (empieza en CERO)
#   s[1]      segundo
#   s[-1]     último
#   s[0:2]    desde 0 HASTA 2 SIN INCLUIR el 2  -> los dos primeros
#
# EL NÚMERO DE LA DERECHA SE EXCLUYE. Siempre.
#   "CS50"[0:1]  ->  "C"     (una sola letra)
#   "CS50"[0:2]  ->  "CS"    (dos letras)

# ----------------------------------------------------------
# 2.5 F-STRINGS (mostrar)
# ----------------------------------------------------------
#   f"Total: {percent:.1f}%"
#    │       │       │    │
#    │       │       │    └─ afuera de {} = texto literal
#    │       │       └────── ADENTRO: dos puntos + formato
#    │       └────────────── adentro: la expresión a mostrar
#    └────────────────────── la f que activa las llaves
#
# REGLA: adentro de {} se calcula, afuera se imprime tal cual.
# El formato SIEMPRE adentro, después de ":".
#   .1f = 1 decimal    .2f = 2 decimales (plata)    :, = separador de miles
#
# El formato va donde el valor TODAVÍA ES NÚMERO.
# Si ya se convirtió a texto, no hay nada que formatear.
#
# LOS FLOATS MIENTEN:
#   0.07 * 100  ->  7.000000000000001
#   0.6  * 100  ->  60.0      (este sale bien de casualidad)
# El error aparece SOLO CON ALGUNOS NÚMEROS -> probar con un caso no alcanza.
# REGLA: todo número calculado que se MUESTRA, va formateado.

# ----------------------------------------------------------
# 2.6 print()
# ----------------------------------------------------------
# print(a, b)             separa con un espacio
# print(a, b, sep="_")    el sep va ENTRE los argumentos
#                         -> NO sirve para armar texto, eso lo armo con +
# print("x", end="")      no salta de línea al final
# print()                 imprime una línea vacía
#
# print() NO DEVUELVE NADA (devuelve None).
#   print(x.lower())   sí
#   print(x).lower()   no  -> AttributeError: 'NoneType'

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
# Un input() adentro pisa lo que le mandaron. (Me pasó en tip, interpreter, meal.)
#
# LLAMAR ES UNA CALCULADORA — necesita las tres partes:
#   resultado  =  convert( lo_que_le_paso )
#      ↑            ↑            ↑
#   guardo       la llamo    le doy el dato
# Sin el "resultado =" el valor se pierde.
#
# EL "=" SE LEE DE DERECHA A IZQUIERDA:
#   "calculá lo de la derecha, guardalo con el nombre de la izquierda"
#   El nombre NUEVO va SIEMPRE a la izquierda.
#   nombre = convert(dato)      sí
#   convert(dato) = nombre      SyntaxError: cannot assign to function call
#
# return TERMINA LA FUNCIÓN EN EL ACTO.
#   Las líneas que siguen no corren.
#   NUNCA adentro de un loop que quiero que dé todas las vueltas.
#   Va al final, o en una salida temprana deliberada.
#
# return vs print
#   return -> devuelve el valor a quien llamó (para el programa)
#   print  -> muestra en pantalla (para el usuario)
#   Asignar a una variable local NO es devolver: esa variable muere.
#
# SCOPE: cada función solo conoce sus propios parámetros y lo que crea.
#   Si main tiene "plate" y is_valid tiene "s", adentro de is_valid
#   uso "s". Usar "plate" -> NameError.
#
# Vocabulario: parámetro = el nombre en el def
#              argumento = el valor real que paso al llamar

# ----------------------------------------------------------
# 2.8 EL PATRÓN main() + auxiliares
# ----------------------------------------------------------
#   funcion_logica  recibe, transforma, RETURN. No habla con nadie.
#   main()          pide input, la llama, IMPRIME.
#
# Cada función UN trabajo. Si están cruzadas, no funciona.
#   convert   ENTRA "7:21" (string)  ->  SALE 7.35 (número)
#   main      no recibe nada         ->  no devuelve nada, imprime
#
# Se separan para poder TESTEAR la lógica sin teclado.

# ----------------------------------------------------------
# 2.9 if __name__ == "__main__":
# ----------------------------------------------------------
#   if __name__ == "__main__":
#       main()
#
# Un .py se puede EJECUTAR (python3 archivo.py) o IMPORTAR
# (otro archivo quiere usar mis funciones).
# Al importar, Python corre todo lo del nivel de afuera — incluido
# un main() suelto. Eso ROMPE LOS TESTS de check50, que importa el
# archivo para probar las funciones por separado.
#
# La guarda hace que main() corra SOLO al ejecutar directo.
# Desde meal.py en adelante, todos los ejercicios de CS50P la llevan.

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
#
# CADA LADO DEL or / and TIENE QUE SER UNA COMPARACIÓN COMPLETA:
#   if x == 5 or x == 10 or x == 25:     sí
#   if x == 5 or 10 or 25:               MAL — siempre True, no avisa
#   if " " or "." not in plate:          MAL — mismo bug
#   if x in [5, 10, 25]:                 mejor que todo lo anterior
#
# COMPARACIÓN ENCADENADA — leerla como dos unidas por "y":
#   7 <= t <= 8   ->  (7 <= t) y (t <= 8)     "entre 7 y 8"
#   7 <= t >= 8   ->  (7 <= t) y (t >= 8)     "mayor que 8". MAL.
#   Los dos signos tienen que apuntar para el mismo lado.
#
# if / elif / else
#   Se DETIENE en la primera condición verdadera.
#   -> ordenar de lo MÁS ESPECÍFICO a lo más general.
#   Con ifs sueltos, Python evalúa todos. Si los casos son excluyentes, elif.
#   Un if SIN else significa "en el otro caso, no hago nada". Es válido.
#
# match / case
#   case "a" | "b":   el | es un OR
#   case _:           el resto

# ----------------------------------------------------------
# 2.11 LOOPS
# ----------------------------------------------------------
# for    recorrer algo que YA TENGO y sé cuánto mide
#        (un string, una lista, un range, un diccionario)
# while  repetir MIENTRAS una condición sea verdadera
#        (no sé de antemano cuántas vueltas van a ser)
#
# Un for sobre un STRING da UN CARÁCTER por vuelta.
# Un for sobre una LISTA da un elemento por vuelta.
#
#   for c in s:              cada carácter
#   for _ in range(3):       3 vueltas, no me importa el número
#                            (_ = variable que no voy a usar)
#   for i in range(len(lista)):   cuando necesito el índice
#
# range(n) va de 0 a n-1, o sea n vueltas.
#   range(10) -> 0,1,2...9   son DIEZ vueltas
#   (Lo tenía mal anotado: para 10 items va range(10), no range(9).)
#
# WHILE — LA REGLA DE ORO
#   1. La variable de la condición nace ANTES del loop.
#   2. Adentro del loop, algo LA MODIFICA.
#   3. Si no, es infinito. Se corta con ⌃+C.
#
#   Un while bien escrito NO necesita break: la condición corta sola.
#
# EL ORDEN ADENTRO DEL WHILE DECIDE QUÉ SE IMPRIME:
#   while falta > 0:
#       print(falta)        <- mostrar PRIMERO
#       pedir dato
#       restar
#   print(cambio)           <- afuera: solo cuando ya terminó
#   Así nunca imprime el "falta: 0", porque chequea antes de entrar.
#
# break      salir del loop ya
# continue   saltear el resto de ESTA vuelta y seguir con la próxima
#
# += y -=   incrementar / decrementar (más pythonico que x = x + 1)
#           Con números suma. Con strings PEGA texto.

# ----------------------------------------------------------
# 2.12 LISTAS
# ----------------------------------------------------------
# lista = ["Luru", "Kike", "Botto"]
#
#   lista[0]        primer elemento
#   lista[0:3]      un pedazo (la derecha se excluye)
#   len(lista)      cuántos
#   x in lista      ¿está?
#
# print(lista)        imprime la lista entera con corchetes
# for x in lista:     imprime uno por línea
#
# Para tener el número de orden junto al valor:
#   for i in range(len(friends)):
#       print(i + 1, friends[i])      (+1 porque los índices arrancan en 0)

# ----------------------------------------------------------
# 2.13 DICCIONARIOS
# ----------------------------------------------------------
# Guardan pares CLAVE : VALOR. Se buscan por clave, no por posición.
#
#   fruits = {
#       "Apple": 130,
#       "Banana": 110,
#   }
#
#   fruits["Apple"]        -> 130      CORCHETES, no paréntesis
#   fruits("Apple")        -> TypeError: 'dict' object is not callable
#   fruits["Mango"]        -> KeyError (la clave no existe: explota)
#   "Apple" in fruits      -> True     (pregunta por CLAVES)
#   fruits.get("Mango")    -> None     (no explota)
#
# LAS CLAVES NO SE REPITEN. Si repito una, el valor nuevo pisa al viejo.
#   {"fruit": "Apple", "calories": 130,
#    "fruit": "Banana", "calories": 110}   -> queda UN diccionario de 2 items
#   La clave es el dato POR EL QUE BUSCO, el valor es lo que QUIERO OBTENER.
#   Como un VLOOKUP de dos columnas.
#
# Recorrerlo da las CLAVES:
#   for nombre in fruits:
#       print(nombre, fruits[nombre])
#
# LISTA DE DICCIONARIOS — cuando cada item tiene VARIOS atributos:
#   amigos = [
#       {"name": "Luru", "casa": "Lapis", "hobbie": "Bici"},
#       {"name": "Kike", "casa": "Lapis", "hobbie": None},
#   ]
#   for amigo in amigos:
#       print(amigo["name"], amigo["casa"])
#
#   Es un dataframe (filas con columnas). Hay que RECORRERLO para buscar.
#   El dict plano es un VLOOKUP: acceso directo, sin loop.
#   Con un solo dato por clave -> dict plano. Con varios -> lista de dicts.
#   (En la semana 4, lo que devuelve un LLM estructurado es esto.)
#
# None = "no hay valor". No es 0 ni "" ni False. No da error.

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
# El try envuelve SOLO lo que puede fallar.
# Envolver de más hace que el except atrape cosas que yo quería
# manejar de otra forma, y el bug no avisa.
#
# VARIOS except, UNO POR ERROR, cada uno con SU reacción:
#   except KeyError:
#       pass        <- item inválido: ignorar y volver a preguntar
#   except EOFError:
#       break       <- Ctrl-D: salir del loop
#
# Python usa el PRIMER except que coincida.
# Meter todos los errores en un solo except les da a todos la misma
# reacción. Ese fue mi bug en taqueria: "burger" cerraba el programa.
#
# pass  = no hago nada, sigo
# break = salgo del loop
#
# NO listar errores que no pueden pasar. Engaña al que lee el código:
# parece que maneja casos que en realidad no existen.

# ----------------------------------------------------------
# 2.15 try/except  vs  if       (la distinción que importa)
# ----------------------------------------------------------
# try/except  atrapa lo que ROMPE.
#     "cat/dog"  -> ValueError al convertir
#     "3/0"      -> ZeroDivisionError al dividir
#
# if          maneja lo que ANDA PERO NO SIRVE.
#     "4/3"  -> 1.33 es un número perfectamente válido,
#               pero el enunciado lo rechaza.
#     "-1/4" -> -0.25 tampoco rompe nada. También se rechaza.
#
# El if de validación va en el else del try, antes del return,
# o con un continue adentro del try.
#
# AL VALIDAR UN RANGO, MIRAR LOS DOS EXTREMOS.
# "result > 1" solo cubre el techo. El negativo pasa igual.
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
# Son distintos. Ctrl-C corta un loop infinito; Ctrl-D cierra la entrada.


# ##########################################################
# ##########################################################
#  PARTE 3 · PATRONES QUE SE REPITEN
# ##########################################################
# ##########################################################

# ----------------------------------------------------------
# 3.1 EL ACUMULADOR      (camel.py, twttr.py)
# ----------------------------------------------------------
#   resultado = ""              <- AFUERA del loop. Nace vacío.
#   for letra in palabra:
#       resultado += algo       <- ADENTRO. Crece cada vuelta.
#   print(resultado)            <- AFUERA, después. UN solo print.
#
# Si la variable nace ADENTRO del loop, se reinicia cada vuelta
# y pierdo todo lo acumulado.
#
# El VALOR INICIAL define qué tipo de acumulador es:
#   texto = ""   acumula texto   ("a" + "x" = "ax")
#   conteo = 0   cuenta          (1 + 1 = 2)
#
# EL ERROR QUE MÁS ME COSTÓ:
#   poner print() adentro del loop.
#   El if NO decide qué imprimir -> decide QUÉ AGREGAR a la variable.
#   Adentro del for no va ningún print (salvo para debuggear).

# ----------------------------------------------------------
# 3.2 LA BANDERA         (plates.py)
# ----------------------------------------------------------
# Una variable que RECUERDA algo entre vueltas del loop.
# Mismo mecanismo que el acumulador, pero guarda un sí/no.
#
#   vi_un_numero = False        <- afuera, arranca en "no"
#   for c in s:
#       if c.isdigit():
#           if vi_un_numero == False and c == "0":
#               return False    <- solo para el PRIMER dígito
#           vi_un_numero = True <- para TODO dígito
#       else:
#           if vi_un_numero == True:
#               return False    <- una letra que llegó tarde
#
# Sirve cuando la pregunta "¿esto está mal?" depende de lo que pasó antes.
# Una bandera que se prende pero NUNCA SE CONSULTA en un if no sirve de nada.

# ----------------------------------------------------------
# 3.3 "BUSCÁ EL FALLO"   (plates.py)
# ----------------------------------------------------------
# Cuando TODAS las condiciones deben cumplirse:
#
#   if <regla 1 falla>: return False
#   if <regla 2 falla>: return False
#   if <regla 3 falla>: return False
#   return True                      <- solo se alcanza si sobrevivió todo
#
# Cada if describe el CASO MALO y sale temprano.
# UN SOLO return True, al final, afuera de todos los ifs.
#
# Al revés (cada regla devuelve True) alcanza con cumplir UNA sola
# para declararlo válido. Es el error que tuve toda la tarde.
#
# Y una regla NO es un valor con el que comparar: es una PREGUNTA
# que le hago al dato, y la respuesta es True o False.
#   s.isalnum()  YA ES la respuesta. No se compara con nada más.

# ----------------------------------------------------------
# 3.4 NORMALIZAR PARA COMPARAR, NO PARA GUARDAR
# ----------------------------------------------------------
# El .lower() va del lado de la PREGUNTA, no del dato que voy a usar.
#
#   if letter.lower() not in "aeiou":
#       resultado += letter          <- la letra ORIGINAL, con su mayúscula
#
# .lower() no modifica letter: produce una copia temporal para comparar.
#
# Y HAY QUE NORMALIZAR LOS DOS LADOS del ==:
#   answer == "Forty two"
#     ↑            ↑
#  minúscula   mayúscula   -> NUNCA matchea
# Python no toca lo que yo escribo en el código.
#
# La normalización va en UN SOLO LUGAR: donde el dato entra.
# No cubre: espacios en el MEDIO, ni sinónimos.

# ----------------------------------------------------------
# 3.5 EL DATO DEL USUARIO NO ES UNA INSTRUCCIÓN
# ----------------------------------------------------------
# Si el usuario escribe "+", eso es el TEXTO "+" guardado en una variable.
# Python no lo ejecuta. Yo tengo que MIRAR ese dato con un if y decidir.
# Igual con "a.m.", con el operador, con la moneda.
# Lo leo, no lo deduzco.


# ##########################################################
# ##########################################################
#  PARTE 4 · MIS ERRORES
# ##########################################################
# ##########################################################

# ----------------------------------------------------------
# 4.1 LOS QUE REPITO (por orden de tiempo perdido)
# ----------------------------------------------------------
# 1. INVENTAR SINTAXIS Y NO CORRERLA.
#    .isnum, .add, len(6), int(a, b), .split(":", ",")
#    Escribo 15 líneas sobre algo que nunca corrió.
#    -> REPL primero. Una línea. 30 segundos.
#
# 2. CORRER SIN GUARDAR. La bolita ● tiene que ser X. ⌘+S.
#
# 3. ESTAR EN LA CARPETA EQUIVOCADA. Leer la palabra antes del %.
#
# 4. == cuando quiero =, o los lados del = invertidos.
#    ==  pregunta si son iguales, devuelve True/False
#    =   guarda lo de la derecha en el nombre de la izquierda
#    El nombre nuevo va SIEMPRE a la izquierda.
#
# 5. USAR LA VARIABLE EQUIVOCADA adentro del loop.
#    Imprimir `word` en vez de `letter`, preguntar por `s` en vez de `c`,
#    mirar `s[0]` cuando quiero el carácter de esta vuelta.
#    Adentro del for, el dato de esta vuelta es la variable del for.
#
# 6. LÍNEAS QUE CALCULAN Y TIRAN EL RESULTADO.
#    z != 0     /     s.isalnum()     /     convert(dato)   sueltas.
#    Para que una condición HAGA algo tiene que estar en un if.
#    Para que un valor sobreviva tiene que guardarse con =.
#
# 7. return ADENTRO DE UN LOOP que tiene que dar todas las vueltas.
#
# 8. NORMALIZAR UN SOLO LADO de la comparación.
#
# 9. PONER EL FORMATO AFUERA de las llaves del f-string.
#
# 10. VALORES ESCRITOS A MANO que deberían ser variables.
#     print("Change Owed: 0") cuando el cambio puede ser 10.
#
# 11. MEZCLAR ESCALAS. Comparar la fracción (0.75) contra umbrales
#     pensados para el porcentaje (99). Cada variable tiene su unidad:
#     fraction = 0.75   /   percent = 75. No son intercambiables.
#
# 12. UN SOLO except PARA ERRORES QUE NECESITAN REACCIONES DISTINTAS.

# ----------------------------------------------------------
# 4.2 QUÉ SIGNIFICA CADA ERROR
# ----------------------------------------------------------
# LEER DE ABAJO HACIA ARRIBA. La última línea dice QUÉ,
# las de arriba DÓNDE, y el ^^^^ marca la posición exacta.
#
# NameError: name 'X' is not defined
#   Python leyó X como variable y no existe.
#   O es una palabra suelta sin comillas, o es una variable de OTRA función.
#
# AttributeError: 'str' object has no attribute 'isnum'
#   Ese método no existe PARA ESE TIPO, o me lo inventé.
#
# AttributeError: 'NoneType' object has no attribute 'strip'
#   Le apliqué un método al resultado de print(). print() no devuelve nada.
#
# UnboundLocalError: cannot access local variable 'x'
#   La variable se crea SOLO adentro de un if que no se cumplió.
#   -> crearla antes, afuera.
#
# TypeError: 'dict' object is not callable
#   Usé paréntesis donde van corchetes. fruits("Apple") -> fruits["Apple"]
#
# TypeError: object of type 'int' has no len()
#   len() mide cosas con longitud. Un número no tiene.
#
# TypeError: 'str' object cannot be interpreted as an integer
#   Le pasé texto donde iba un número.
#   Clásico: .split(" ", ",") — el 2do argumento de split es un número.
#
# TypeError: '<=' not supported between 'int' and 'str'
#   Comparo un número con un string. Falta convertir, o estoy comparando
#   la variable equivocada (el string original en vez del número).
#
# TypeError: can't multiply sequence by non-int
#   Opero con textos creyendo que son números. Alguna función devolvió
#   el parámetro sin convertir.
#
# ValueError: invalid literal for int() with base 10: '1 + 1'
#   Quise convertir a número algo que no lo es entero.
#   Casi siempre: convertí ANTES de partir.
#
# ValueError: not enough values to unpack
#   Los nombres a la izquierda del = no coinciden con la cantidad
#   de elementos que devolvió el split.
#
# KeyError: 'Mango'
#   Esa clave no está en el diccionario.
#   Se maneja con `in` antes, o atrapándolo con except KeyError.
#
# EOFError
#   El usuario apretó Ctrl-D. No es una falla: es el fin de la entrada.
#
# KeyboardInterrupt
#   Ctrl-C. Cancelé el programa a mano.
#
# SyntaxError: cannot assign to function call here
#   Puse la llamada a la izquierda del =. El nombre nuevo va primero.
#
# SyntaxError: invalid syntax
#   Falta paréntesis, coma, comillas o los dos puntos.
#
# ZeroDivisionError
#   División por cero. Se previene con un if ANTES de dividir
#   (o con try/except, semana 3).
#
# command not found: X
#   zsh no conoce X. hello.py no es un comando: se corre con python3.
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
#    ("¿son todos letras o números?" — no "letras o números")
# 3. Mirar el Demo carácter por carácter: espacios, mayúsculas, dos puntos.
#    check50 compara LITERAL. Copio el texto del enunciado.
# 4. cd a la carpeta del ejercicio. Archivo con el nombre EXACTO.
# 5. UNA regla / UN paso por vez. Correr. Verificar. Recién ahí la siguiente.
# 6. Probar YO los casos del enunciado ANTES de check50,
#    incluyendo los "feos": el que se pasa, el vacío, el de dos palabras.
# 7. check50 cs50/problems/2022/python/<ejercicio>
# 8. Si sale rojo, leer QUÉ input falló. Correr ese input a mano.
# 9. submit50 (los dos comandos son distintos: check50 no entrega nada)

# ----------------------------------------------------------
# 5.2 CHECKLIST ANTES DE PEDIR AYUDA
# ----------------------------------------------------------
# [ ] ¿Guardé? (⌘+S — bolita ● -> X)
# [ ] ¿Corrí el código, o solo lo escribí?
# [ ] ¿Verifiqué en el REPL los métodos que usé?
# [ ] ¿Estoy en la carpeta correcta?
# [ ] ¿Uso la variable de ESTA vuelta del loop, o la de afuera?
# [ ] ¿Hay alguna línea que calcula algo y no lo guarda?
# [ ] ¿El acumulador/bandera nace AFUERA del loop?
# [ ] ¿La indentación empareja los if/else como quiero?
# [ ] ¿Cada función DEVUELVE, o solo asigna a una variable local?
# [ ] ¿Normalicé los dos lados de la comparación?
# [ ] ¿Cada except tiene la reacción que corresponde a ESE error?
# [ ] ¿Validé los DOS extremos del rango, no solo uno?
# [ ] ¿Estoy comparando valores de la misma escala/unidad?
# [ ] ¿Probé con más de un caso, incluyendo uno "feo"?
#     (el negativo, el cero, el que se pasa, el que no existe)

# ----------------------------------------------------------
# 5.3 SI ME TRABO (en este orden)
# ----------------------------------------------------------
# 0-5 min    Leer el error ENTERO, de abajo hacia arriba.
# 5-15 min   print() de las variables justo antes de la línea que falla.
#            (y borrarlo después)
# 15-20 min  Buscar el mensaje de error textual en Google.
# 20+ min    Preguntar: "no me des el código, explicame por qué pasa
#            y decime en qué línea mirar".
# NUNCA      Copiar y pegar algo que no entiendo.
#
# SI SE ENREDA FEO — el método que funcionó:
#   Borrar todo y volver a DOS líneas. Correr. Verificar.
#   Agregar UNA línea. Correr. Verificar.
#   Es más rápido que seguir moviendo piezas de algo que nunca corrió.

# ----------------------------------------------------------
# 5.4 CERRAR EL DÍA
# ----------------------------------------------------------
#   cd ~/ai-plan
#   git add .
#   git commit -m "dia N: lo que hice"
#   git push
#
# Aunque esté roto o incompleto. Regla del plan.