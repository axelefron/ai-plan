## Día 21 · Claude Code in Action (resumen)

**Idea central:** Claude Code es un agente que corre en la terminal: lee archivos, ejecuta comandos y edita código con herramientas (el mismo `while` del Proyecto 2, pero ya armado y con permisos). Yo sigo siendo el que revisa cada cambio.

### 1. Contexto = lo que Claude "sabe" en este momento
- Tiene una ventana de contexto limitada; todo lo que lee y escribe ocupa lugar.
- `CLAUDE.md` en la raíz del repo ✱: instrucciones permanentes (comandos, convenciones, qué no tocar). `/init` ✱ genera uno.
- Mencionar archivos puntuales (`@archivo`) ✱ en vez de dejar que explore todo.
- `/clear` ✱ al cambiar de tarea y `/compact` ✱ para resumir cuando el contexto se llena.

### 2. Flujo de trabajo
- Pedir en pasos chicos y verificables; revisar el diff antes de aceptar.
- Plan mode ✱: primero que proponga el plan, yo lo corrijo y después ejecuta.
- Pensar más (extended thinking ✱) solo para problemas difíciles; cuesta más tokens.
- Darle una forma de verificar su trabajo (tests, correr el script): sin eso, no sabe si funcionó.

### 3. Extender Claude Code
- **MCP:** se le conectan servidores propios o ajenos (igual que Desktop). Mi `mcp_chroma_server.py` sirve acá también.
- Comandos personalizados ✱ y hooks ✱ (acciones automáticas antes/después de usar una tool).

### 4. GitHub
- Integración para PRs y code review; Claude puede revisar cambios y comentar.

### 5. Buenas prácticas
- Permisos: aprobar lo que entiendo, rechazar el resto.
- Tareas acotadas, un objetivo por conversación.

### Mi regla desde hoy
Claude Code escribe, yo reviso línea por línea. Si no puedo explicar una línea, la rechazo.

### Lo mío (completar)
- Lo que más me sorprendió: - **HOOK** --> muy importante, fuerza el codigo para que Claude no lo ejecute, son reglas que el Claude README.md no puede ejecutar. Sirve para definir reglas que no debe incumplir nunca, con mas peso que la guía de los .md. Por ejemplo, se pone en un hook que nunca haga un git push o submit de un.env file.
- Lo que no entendí del todo: cosas para los planes de empresas, los plugins de repos propios, no me interesa por ahora.


## Mi subagente code-reviewer

**Qué armé**
- Un subagente a nivel usuario (`~/.claude/agents/code-reviewer.md`), así lo uso en cualquier proyecto.
- Solo lectura: tools Read, Grep, Glob y Bash. Modelo sonnet, color purple.
- Explica los cambios en español, marca [RIESGO] y [ENTENDER], da un veredicto y me deja 3 preguntas sin respuesta para chequear que entendí.

**Cómo lo probé**
- Le pedí que creara un archivo: se negó (es de solo lectura). No sé si lo frena `disallowedTools` o su prompt.
- La trampa: un script con la key escrita en el código y sin try/except. Con aviso previo del Claude principal no la analizó; en la prueba limpia sí la detectó. Una corrida dio "aprobado con observaciones" y otra "rechaza": eso me enseñó que el veredicto tiene que ser consistente.
- Lo usé para revisar `list_documents` (la 3ra tool de mi servidor MCP): aprobó con observaciones bajas.

**Lo que aprendí**
- El revisor solo sabe lo que le cuenta el Claude principal. Si el principal le dice "esto es a propósito", no lo mira. Por eso la prueba limpia dio distinto.
- "proactively" en la description no alcanzó (ni con ejemplos) para que delegue solo. Con la regla en `CLAUDE.md` sí delegó. Probablemente fue la regla, pero no lo puedo separar del todo porque cambié las dos cosas juntas.
- `{... for ...}` con llaves arma un set: por eso `list_documents` no repite títulos. (Yo había contestado que no eliminaba nada: estaba mal.)
- `sorted()` y `sorted(key=str.casefold)` dan el mismo orden con acentos: `['Banco', 'zeta', 'Árbol']`. casefold arregla mayúsculas, no acentos.
- Tool MCP: dentro de un proyecto, "¿qué documentos tengo indexados?" no usó mi tool (la leyó como archivos del proyecto). En un chat fuera del proyecto, con el pedido explícito, devolvió los 27 títulos. La description de la tool es lo que decide cuándo se elige.
- Lo que aprueba un revisor que solo lee no prueba que funcione: la prueba real fue Claude Desktop.

**Respuestas a las preguntas de los revisores**
- ¿Por qué el id sale del hash del contenido y no del título?: Porque puedo tener el mismo contenido con títulos distintos. El hash permite detectar que es el mismo documento aunque le cambie el nombre. Además, dos documentos distintos pueden tener el mismo título.
- ¿Alcanza con borrar la key en un commit posterior?: No, porque sigue en el historial de Git. Tengo que revocarla, generar una nueva y guardarla en una variable de entorno. También sacar la anterior del historial si quedó publicada.
- ¿Cómo evitaría que `add_document` corra sin mi aprobación?: Configuraría el cliente para que me pida permiso cada vez que quiera usar esa tool, sin aprobación automática. La tool además valida los datos, pero eso no reemplaza mi permiso.

**Explicación de MCP en 2 minutos (para alguien no técnico)**
MCP es una forma estándar de conectar una IA con herramientas y fuentes de información. Es como darle acceso a funciones que puede usar para hacer algo concreto, como buscar documentos o agregar información a una base.

En mi proyecto, conecto la IA con una base de documentos del banco. Si alguien pregunta sobre un procedimiento, la IA puede usar la herramienta de búsqueda para encontrar fragmentos relevantes y responder citando las fuentes. Si le pido agregar un documento, puede usar otra herramienta, con mi aprobación.

El servidor MCP no es el que piensa ni redacta la respuesta: ejecuta la herramienta y devuelve el resultado. La IA usa ese resultado para seguir la conversación. MCP define cómo se comunican.

**Pendiente**
- Lecciones 3 y 4 del curso de subagentes.


## Lección 3 — Diseñar subagentes que funcionen

Los 4 patrones del curso y cómo quedó mi code-reviewer:
- **Descripción específica:** la description no solo decide cuándo corre el subagente, también guía el prompt que el Claude principal le escribe. Le agregué que pase la ruta exacta de los archivos, lo que pidió el usuario y que NO diga qué es intencional.
- **Formato de salida definido:** ya lo tenía (5 secciones). Le da puntos de parada y evita que se extienda de más.
- **Reportar obstáculos:** me faltaba. Sumé una 6ta sección "Obstáculos" (setup, quirks, lo que no pudo verificar).
- **Tools limitadas:** Read, Grep, Glob y Bash (para git diff). Sin Edit ni Write.

Cómo lo probé:
- Pedí un archivo con una key falsa escrita "a propósito". El prompt de entrada que escribió el principal no decía ni la key ni "a propósito". El revisor la detectó solo como riesgo alto y dio "Rechazaría".
- Me quedó claro que la description es una palanca más fuerte de lo que pensaba: controla qué le cuenta el principal al subagente.
- Todavía son pocas pruebas, no lo doy por cerrado.
