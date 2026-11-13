# ai-plan

## Este repo
Es mi repo de estudio del plan de 13 semanas para aprender a construir agentes de IA. Cada semana tiene su carpeta: `semana-01` a `semana-13`. Las API keys y los módulos compartidos viven en la raíz.

## Python
- Usá siempre `python3` y `pip3`. Nunca `python` ni `pip` a secas.
- Trabajá con el entorno virtual `.venv` de la raíz. Instalá librerías ahí.

## Secretos
- Las API keys viven solo en el archivo `.env` de la raíz.
- Nunca escribas una key dentro de un `.py`, un `.md` ni un comentario.
- Nunca leas, muestres ni edites `.env`, y nunca lo commitees.

## Git
- Un solo commit por día, al final, no uno por cada cambio.
- Mensaje con este formato: `Día N: resumen corto`.
- Antes de commitear, mostrame `git status` para que yo revise qué entra.

## Qué no se toca
- La carpeta ~/Internship-applications-summer27 es solo lectura (no modificar ni borrar nada ahí). Tampoco borrar archivos sin preguntarme antes.

## Tests
- Corré `pytest` desde la carpeta de la semana que estoy trabajando, no desde la raíz.

## Revisión de código
Después de crear o modificar archivos de código en este repo, invocá al subagente code-reviewer con esos cambios antes de dar la tarea por terminada, y mostrame su resultado completo.
