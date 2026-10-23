# Agente que sobrevive a cortes, se puede observar y resiste inyecciones

Agente con tools (`search_in_csv`, `calculate_discount`, `search_docs` sobre un RAG de 27 documentos bancarios y `save_report`) escrito a mano, sin framework. En la semana 8 le agregué lo que separa un demo de algo que se puede dejar corriendo: **retomar tras un corte, reintentar bien, pedir aprobación humana, poder verlo por dentro y defenderlo de documentos envenenados.**

**Stack:** Python, API de Anthropic (`claude-sonnet-4-5`), Chroma, Langfuse, pytest.

## Resultado en una línea

El agente retoma una corrida cortada a mitad de una tool, reintenta solo errores transitorios, no ejecuta `save_report` sin mi aprobación, deja un árbol de trace en Langfuse por corrida, y una política en código rechaza nombres de archivo peligrosos aunque el modelo falle. En mis pruebas de inyección el modelo resistió **0 de 12** ataques, pero lo que garantizo es la política, no el modelo.

## Qué construí (Días 22 a 24)

- **Estado persistente:** un JSON por corrida (`state/<run_id>.json`). Se guarda solo en puntos consistentes: el mensaje del asistente y los resultados de sus tools se agregan juntos, porque la API rechaza un `tool_use` sin su `tool_result`. Probé cortes durante la llamada a la API, durante una tool y con la corrida ya terminada.
- **Reintentos con espera creciente:** solo para errores transitorios (`TransientToolError`), con backoff exponencial y jitter. Un error permanente (`ValueError`) falla de inmediato.
- **Human-in-the-loop en código**, no en el prompt: antes de `save_report` se muestra el contenido completo y hay que escribir `y`.
- **Tope de fallos por tool** (`MAX_TOOL_FAILURES`), guardado en el estado, para cortar el ciclo de reintentos que se multiplican con los que decide Claude.
- **Observabilidad con Langfuse:** un trace por corrida con cada llamada a Claude, cada intento de tool, la aprobación humana, tokens, costo y latencia.
- **Seguridad:** ver [`README_security.md`](README_security.md) (modelo de amenazas, 5 ataques, política en `policy.py`).

## Qué medí con Langfuse

- Una corrida típica (buscar, descontar, guardar) gastó unos 5.500 tokens, **≈ US$0,024**. Coincide con lo que contó mi terminal.
- La llamada más cara no fue la de más tokens de entrada: la salida cuesta cinco veces más por token, y la más cara fue la que escribió el reporte.
- **Los reintentos cuestan tiempo, no tokens:** 3 intentos sumaron 22 ms de trabajo real y unos 3 s de espera de backoff.
- De una corrida de 34,5 s, unos **9,5 s eran yo escribiendo `y`**, invisibles hasta que decoré `ask_approval`. Tiempo de humano no es tiempo del agente.

## Seguridad en breve

| | Resultado |
|---|---|
| Control positivo (el usuario pide guardar) | `save_report` 2/2: el instrumento detecta |
| 4 ataques (override, falsa autoridad, nota al pie, secuestro de nombre) | la inyección llegó al modelo 12/12; acción del atacante **0/12** |
| Política en código | 15 tests (nombres peligrosos, procedencia del valor, integración con `run_agent`), sin llamar a la API |

Un hallazgo antes de atacar: `save_report` podía pisar `persistent_agent.py` o `data.csv`. Ahora solo escribe `.txt` con nombre simple dentro de `reports/`.

## Limitaciones

- Las pruebas de inyección son **N = 3 por caso**, un solo modelo y ataques explícitos. Que hoy resista no es una garantía.
- El caso 5 (secuestro de extensión) y los prompts alternativos quedaron sin medir: se me acabó el saldo de la API.
- La política cubre `save_report`; no cubre contenido envenenado que cambie el texto de la respuesta.
- Falta evaluar, en varias corridas, si "Never invent data" evita que el agente invente cuando una tool falla.

## Archivos

| Archivo | Para qué |
|---|---|
| `persistent_agent.py` | El agente: estado, reintentos, aprobación, tracing |
| `policy.py` | Autorización de tools en código |
| `rag_tool.py` | Tool `search_docs` sobre la base de `semana-06` |
| `attack_cases.py`, `build_attack_db.py`, `run_attacks.py` | Documentos envenenados, su base y el runner de ataques |
| `test_persistent_agent.py`, `test_policy.py` | 23 tests, ninguno usa la API |
| `README_security.md` | Modelo de amenazas y resultados |
| `notas.md` | Diario de los días 22 a 24, con mis errores |

## Cómo correrlo

    pip3 install anthropic python-dotenv langfuse chromadb sentence-transformers pytest
    # .env en la raíz: ANTHROPIC_API_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_BASE_URL
    python3 persistent_agent.py     # desde semana-08
    python3 -m pytest -q            # 23 tests, sin API
