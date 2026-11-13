## Día 26 — Hook que protege .env

- Con CLAUDE.md activo, Claude se negó a leer .env por la regla escrita. No usó ninguna herramienta: obedeció un pedido.
- Sin CLAUDE.md, Claude sí intentó leer .env.test (con Read y con cat en Bash) y el hook protect_env.py lo bloqueó con exit 2 y mi mensaje. Eso es código que se ejecuta, no un pedido.
- Conviene tener las dos capas: CLAUDE.md le explica a Claude qué evitar y por qué, y el hook garantiza el bloqueo aunque Claude no obedezca o no tenga el archivo cargado.
- Cómo se podría saltear: el matcher no incluye Glob, y algo como cat .e""nv no matchea la regex. También bloquea de más: frena cualquier comando que contenga .env, incluso un mensaje de commit.

## Mini proyecto (Día 27): analizador de gastos desde CSV

- Qué hace: lee un CSV de gastos, los clasifica por categoría y calcula el total por categoría y por mes.
- Qué recibe: la ruta de un archivo CSV con columnas fecha, descripción y monto (uno de prueba con datos inventados, no el del banco).
- Qué produce: un resumen mensual en pantalla y guardado en semana-09/summary.md.
- Qué NO hace: no modifica ni borra el CSV original, no usa internet ni APIs, no guarda datos personales reales en el repo.

## Plan de Claude Code (modo plan)
- Paso que corregí: la verificación con git diff sobre el CSV de ejemplo no servía porque el archivo es nuevo y sin commitear, así que daba vacío siempre. La reemplazamos por comparar shasum antes y después de correr el script.
- Paso que pedí que me explique: por qué una fila inválida detenía todo el programa. Quedó en validar todas las filas, informar todos los errores juntos con su línea y no generar summary.md si hay alguno.


## Dia 27

# Bloque A

Inicio: 4:05 PM

- Tiempo: empecé 4:05 PM; código y tests funcionando 4:51 PM.
- El code-reviewer encontró: BOM de Excel, samefile en macOS, tests que no probaban los arreglos.
- A mano me hubiera llevado minimo 5 hs.
- Próxima vez haría distinto: crear yo los CSVs.

### Preguntas del code-reviewer

1. En expenses.py (línea 143), ¿por qué hace falta os.path.samefile y no alcanza con comparar input_path == output_path, aun después de resolve()? ¿Qué pasaría en macOS sin él con EXPENSES.csv?

   Respuesta: comparar con == compara el texto de las rutas, y resolve() en macOS no corrige las mayúsculas. macOS por defecto no distingue mayúsculas en el disco, así que expenses.csv y EXPENSES.csv son el mismo archivo aunque el texto sea distinto. Sin samefile, el programa creería que son archivos distintos, escribiría el resumen encima del CSV de entrada y lo destruiría. samefile compara el archivo real en el disco, no el texto, así que lo detecta. También detecta symlinks y hard links. Por eso antes se comprueba que ambas rutas existan, porque samefile da error si una no existe.

2. En test_main_output_in_missing_folder_returns_error, ¿qué línea de main hace que el resumen igual aparezca en pantalla antes del error de guardado? ¿Es un problema?

   Respuesta: main imprime el resumen con print antes de llamar a save_summary, así que cuando el guardado falla el resumen ya se mostró. No es un problema: el usuario igual ve el resultado, después ve un mensaje de error claro y el programa devuelve 1. Lo importante es que no se rompe con un traceback y que el CSV de entrada no se toca.

3. Si ejecutara la suite en Linux (disco sensible a mayúsculas), ¿qué mostraría pytest -rs para el test de capitalización y por qué no sería un fallo?

   Respuesta: mostraría ese test como skipped, con el motivo que escribió el skipif (el disco distingue mayúsculas). No sería un fallo porque en Linux expenses.csv y EXPENSES.csv son archivos distintos, así que el caso que prueba el test no puede ocurrir ahí. Saltearlo significa que no aplica en ese entorno, no que el código esté mal.
