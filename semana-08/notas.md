# Día 22 — Building Effective Agents (3ª lectura)

## Idea central del texto
- Workflow = el código decide el camino, con pasos predefinidos.
- Agente = el LLM decide el camino en un loop con tools.
- Regla del artículo: empezar por lo más simple. Un workflow si los pasos son predecibles; un agente solo si no se puede predecir cuántos pasos hacen falta.
- Bloque base: el "augmented LLM" (LLM + tools, retrieval o memoria).

## Los 5 workflows, en mis palabras
- Prompt chaining: pasos fijos; la salida de uno es la entrada del siguiente.
- Routing: clasificar la entrada y mandarla a un camino especializado.
- Parallelization: tareas independientes en paralelo, o la misma tarea varias veces para votar.
- Orchestrator-workers: un LLM reparte subtareas que no se conocen de antemano.
- Evaluator-optimizer: un LLM genera, otro evalúa y devuelve feedback, y se itera.

## Qué patrón usa cada cosa que construí
- Clasificador (S4): una sola llamada; es el paso de *routing* sin el camino posterior. Sumarle ese camino lo dejaría más ordenado, pero no hace falta: el resultado es predecible y se puede fijar en código.
- RAG (S6): augmented LLM; retrieval y generación en un orden fijo (cadena de 2 pasos), sin loop.
- Agente S5 (`agent_chained_tasks`): agente autónomo (loop + tools). Podría haber sido un prompt chaining, pero elegí un agente con tools predefinidas que creé yo, para poder optimizar el workflow y que el agente decida con augmentation y mejore la respuesta final. El costo: más espera y más llamadas a la API.

## Qué patrón me conviene agregar
- Candidato: evaluator-optimizer en el RAG (= reflection del Módulo 2 de Ng).
  - Por qué: un RAG que inventa no se puede vender. Un segundo paso que verifica "¿cada afirmación está respaldada por los fragmentos?" ataca justo ese riesgo.
  - Cómo lo mido: re-correr mis 15 preguntas de eval antes y después. Hipótesis: el score mejora, porque un segundo LLM hace de revisor y devuelve su feedback al primero para que rehaga la respuesta.
  - Hay que fijar un máximo de turnos: si el loop corre indefinidamente buscando mejorar, el gasto de API y la latencia suben sin aportar valor.
- Para más adelante: orchestrator-workers (= planning del Módulo 5) en el proyecto vertical, si el proceso tiene subtareas que no se conocen de antemano.
- Descartado por ahora: parallelization. No hace falta dividir tareas en paralelo, así que un workflow con agentes corriendo en simultáneo para distintas aplicaciones no es ideal en mi situación.

## Principios que quiero aplicar (Día 23 en adelante)
- Transparencia: que el agente muestre sus pasos (mi log ya lo hace).
- Diseño de tools (el artículo le dedica un apéndice): descripciones claras y parámetros difíciles de usar mal (mis `enum` ya van en esa línea). Me apoyo en un LLM para revisar estas partes y pensar la mayor cantidad posible de evals relevantes.
- Human-in-the-loop antes de acciones irreversibles (`save_report`, `add_document`): tiene que haber revisión humana antes de correr código que pueda dañar el ecosistema.


# Día 23 · Bloque A — Estado persistente

## Qué guardo y dónde
- Un archivo por corrida: `state/<run_id>.json` con `status` (running / done / abandoned / max_turns_reached), `turn`, `messages`, tokens de entrada y salida, y el mensaje original del usuario.
- Al arrancar, si hay una corrida en `running`, el script pregunta si retomarla. Si digo que no, queda `abandoned` y no vuelve a preguntar.

## Decisiones de diseño y por qué
- **Guardo solo cuando el par asistente + tool_results está completo.** La API rechaza un `tool_use` sin su `tool_result`. Por eso el mensaje del asistente se agrega después de ejecutar las tools (antes lo agregaba al recibir la respuesta). Si el corte llega a la mitad, el último estado guardado sigue siendo un historial válido.
- **Escritura atómica** (archivo temporal + `os.replace`): un corte durante el guardado no deja un JSON a medias.
- **`to_plain` con `model_dump(exclude_none=True)`:** los bloques del SDK no son serializables a JSON. El JSON guarda además un campo `caller` en los tool_use; la API lo aceptó al reanudar.
- **`turn` solo avanza cuando el turno terminó completo.** Al retomar se rehace el turno que quedó a medias.

## Las pruebas (resultados reales)
1. **Corte durante la llamada a la API:** el JSON quedó en `running`, turno 2, 5 mensajes. Al retomar no repitió `search_in_csv` ni `calculate_discount`, ejecutó `save_report` y terminó (tokens acumulados: 1995/191 → 4723/551).
2. **Corte durante una tool** (`sleep(10)` en `calculate_discount`): el JSON quedó en `running 1 3`. Al retomar saltó `search_in_csv` y volvió a ejecutar `calculate_discount`, que no había terminado.
3. **Corrida completa:** `done`, y al reiniciar el script ya no ofrece retomar nada.

## Lo que me enseñó el día
- **El agente inventó datos cuando la tool falló.** Con el CSV inaccesible, Claude dijo que "podía demostrar el workflow con datos de ejemplo" y siguió con precios inventados. En la prueba del Día 15 con `furniture` se frenó y no inventó. Mismo código, comportamiento distinto: mi system prompt no dice "si una tool falla, no inventes datos ni continúes". Lo llevo al Día 24 como caso para evals y prompt injection.
- Una corrida cortada con datos malos no hay que retomarla: por eso existe la opción `n` (abandoned).

## Límite que me queda
- Si una tool se ejecuta pero el corte llega **antes de guardar**, al retomar se re-ejecuta. Con `search_in_csv` y `calculate_discount` da igual. `save_report` sobrescribe el mismo archivo, así que casi tampoco importa. Lo que no tolera repetirse es una acción irreversible (mandar un mail, borrar, escribir en un sistema). Eso es el Bloque B: confirmación humana antes de ejecutarla.

# Bloque B — Reintentos y aprobación humana

## Reintentos con espera creciente
- Solo reintento errores transitorios (`TransientToolError`: timeout, conexión). Los permanentes (parámetro inválido, archivo inexistente) fallan al instante: reintentarlos no cambia nada.
- Espera: 1, 2, 4 s (`BASE_DELAY × 2^intento`) más un azar de 0–0,5 s (jitter) para que muchos clientes no reintenten todos a la vez. Máximo 3 reintentos (4 llamadas).
- Si se agotan, el error vuelve a Claude como `tool_result` con `is_error`. El SDK ya reintenta las llamadas a la API; esto cubre mis propias tools.

## Aprobación humana (human-in-the-loop)
- `REQUIRES_APPROVAL = {"save_report"}`. La compuerta está en el código (`ask_approval`), no en el prompt: el modelo no la puede saltear.
- Si rechazo, Claude recibe "Action rejected..." y me avisa que no se ejecutó. Si corto durante la aprobación, al retomar vuelve a preguntar: la aprobación no se guarda en el estado.
- Al retomar, Claude regeneró el reporte con otro texto. Lo que aprobé era ese contenido concreto, así que volver a preguntar es lo correcto.

## Pruebas (resultados reales)
1. `price_low` con 2 fallas simuladas: reintentos a 1,1 s y 2,1 s, luego aprobación `y` y reporte guardado.
2. `furniture` (error permanente): falló al instante, sin reintentos; Claude no inventó datos.
3. Rechazo `n`: no se ejecutó y Claude lo informó.
4. Ctrl+C en `Approve?`: retomó desde el turno 2 y volvió a pedir aprobación.
5. Reintentos agotados (`FLAKY_FAILS = 99`): 3 reintentos (1,0 / 2,1 / 4,3 s), Claude volvió a intentarlo una vez (otra ronda), y después se frenó y lo informó sin inventar.

### Mejoras de cierre (hechas)

1. **Vista previa de aprobación:** `ask_approval` muestra el contenido completo de lo que se va a guardar antes de pedir y/n. Aprobar sin ver el contenido no es supervisión humana real.
2. **Tope de fallos por herramienta:** `MAX_TOOL_FAILURES = 2`, guardado en el estado (`tool_failures`). Los reintentos de código (4 intentos) se multiplican con los que decide Claude, y el tope corta ese ciclo. Verificado: el contador se guarda en el JSON. El mensaje de bloqueo solo aparece si Claude insiste, y en la prueba no insistió.
3. **Tests con pytest (8 tests, sin API ni sleeps reales):** reintentos (se recupera, error permanente no se reintenta, se agotan), estado (running se encuentra, done no) y aprobación (solo "y" aprueba). Verificado rompiendo el código a propósito: con `except Exception` el test de error permanente falla (`4 == 1`).

### Pendiente para el Día 24
- Evaluar en varias corridas si "Never invent data to continue" evita que Claude invente datos cuando falla una tool (hoy lo vi funcionar en una sola corrida).


## Día 24 — Bloque A: observabilidad con Langfuse

- **Qué es:** Langfuse guarda un *trace* por corrida: un árbol con cada llamada a Claude, cada tool, tokens, costo y latencia. Mi `log` casero se pierde al cerrar la terminal y no mide tiempos ni dólares.
- **Cómo lo instrumenté:** `@observe` sobre `run_agent` (raíz), `call_claude` (generation, con modelo y tokens), `execute_with_retries`, `execute_tool` (tool) y `ask_approval`. `langfuse.flush()` al salir, porque los datos se mandan en segundo plano. Keys solo en `.env`.
- **Qué vi:**
  - Los tokens coinciden con mi terminal (5548 vs "6k", redondeo). Costo ≈ US$0.024 por corrida.
  - La llamada más cara no fue la de más tokens de entrada: la salida cuesta 5× más por token, y la más cara fue la que escribió el reporte.
  - La entrada crece en cada vuelta porque reenvío el historial completo (más system prompt y schemas de las tools). No hay "tokens de pensamiento": no usé extended thinking.
  - Reintentos: 3 intentos, 22 ms de trabajo real y ~3 s de espera de backoff. Cuestan tiempo, no tokens.
  - La aprobación humana (`human-approval`) duró 1.8 s. Sin decorarla, era un hueco invisible de ~9 s. Tiempo de humano ≠ tiempo del agente.
- **Errores:** un error dentro de una tool aparece en el árbol (Tree → clic en `tool-attempt` → Preview), no en Log View. `agent-run` sale sin error porque el agente manejó la falla como estaba diseñado: el error de una tool no es el fallo del agente.
- **Detalle:** el `undefined` en el Output de `agent-run` es porque `run_agent` no devuelve nada, no por una excepción.

# Bloque B: seguridad y prompt injection

- **Por qué funciona la inyección:** el modelo recibe system prompt, pregunta y documentos recuperados como una sola secuencia de texto, sin frontera técnica entre instrucciones y datos. No "borra" mi prompt: compite con él.
- **Indirecta:** el atacante no habla con el agente, envenena un documento. Tiene que llegar al top de la búsqueda (LLM08) o nunca llega al modelo; mis dos primeros documentos no entraron al top 3 hasta que les agregué texto del tema.
- **Resultado:** 0/12 acciones del atacante con Sonnet 4.5 y mi prompt, aunque la inyección llegó al modelo 12/12 (el modelo la ignoró sin avisarle al usuario). Ni mi predicción (los 2 primeros funcionan) ni mi prompt original estaban medidos: con N=1 no se concluye nada.
- **Instrumento:** hizo falta un control positivo y una columna "llegó al modelo" para que un 0 signifique algo. Un instrumento que falla en silencio (se me acabó el saldo) imprime ceros que parecen buenas noticias.
- **El caso peligroso:** cuando el usuario sí pide guardar, el atacante solo secuestra un parámetro (nombre o extensión). La aprobación manual se vuelve un trámite.
- **Defensa:** la autorización va en el código de la tool (`policy.py`), no filtrando texto ni confiando en el modelo: nombre simple y `.txt`, dentro de `reports/`, tamaño y procedencia del valor. Filtrar frases como "ignorá todo lo anterior" no escala: el atacante reescribe.
- **Cómo la probé:** tests que simulan un modelo comprometido (sin API) y un test de integración de que lo prohibido no llega ni a la aprobación ni a la ejecución.
- **Hallazgo previo:** `save_report` podía pisar `persistent_agent.py` o `data.csv` (solo había `basename`).
- **Pendiente:** caso 05 y prompts B/C con saldo; evaluar en varias corridas si "Never invent data" evita que invente datos (pendiente desde el Día 23).
