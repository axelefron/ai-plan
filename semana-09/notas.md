## Día 26 — Hook que protege .env

- Con CLAUDE.md activo, Claude se negó a leer .env por la regla escrita. No usó ninguna herramienta: obedeció un pedido.
- Sin CLAUDE.md, Claude sí intentó leer .env.test (con Read y con cat en Bash) y el hook protect_env.py lo bloqueó con exit 2 y mi mensaje. Eso es código que se ejecuta, no un pedido.
- Conviene tener las dos capas: CLAUDE.md le explica a Claude qué evitar y por qué, y el hook garantiza el bloqueo aunque Claude no obedezca o no tenga el archivo cargado.
- Cómo se podría saltear: el matcher no incluye Glob, y algo como cat .e""nv no matchea la regex. También bloquea de más: frena cualquier comando que contenga .env, incluso un mensaje de commit.

## Mini proyecto (Día 27): analizador de gastos desde CSV

- Qué hace: lee un CSV de gastos, los clasifica por categoría y calcula el total por categoría y por mes.
- Qué recibe: la ruta de un archivo CSV con columnas fecha, descripción y monto (uno de prueba con datos inventados, no el del banco).
- Qué produce: un resumen mensual en pantalla y guardado en semana-09/resumen.md.
- Qué NO hace: no modifica ni borra el CSV original, no usa internet ni APIs, no guarda datos personales reales en el repo.

## Plan de Claude Code (modo plan)
- Paso que corregí: la verificación con git diff sobre el CSV de ejemplo no servía porque el archivo es nuevo y sin commitear, así que daba vacío siempre. La reemplazamos por comparar shasum antes y después de correr el script.
- Paso que pedí que me explique: por qué una fila inválida detenía todo el programa. Quedó en validar todas las filas, informar todos los errores juntos con su línea y no generar resumen.md si hay alguno. [agregar la razón que dio Claude]
