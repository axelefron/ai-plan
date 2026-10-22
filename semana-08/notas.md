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
