# RAG sobre documentos bancarios: construirlo y medirlo

Chatbot que responde preguntas sobre un corpus de 27 PDFs de banca y finanzas personales, **cita el documento de cada dato** y **dice "no sé" cuando los documentos no tienen la respuesta**, en vez de inventar.

Lo construí en dos pasos: primero el sistema (Día 17) y después una evaluación para saber qué tan bien funciona y por qué falla (Día 18). Este README resume lo segundo.

**Stack:** `pypdf` → chunks → `Chroma` (embeddings `paraphrase-multilingual-MiniLM-L12-v2`) → Claude Haiku (`claude-haiku-5-5`).

## Resultado en una línea

Con un set de 15 preguntas, el bot acierta **10/15 con datos y citas correctos**. En ninguna inventó un dato: los 5 fallos son 3 "no sé" y 2 datos reales pero de otro documento. Probé 3 mejoras, una por vez, y **ninguna superó al baseline**. Eso me mostró dónde está el problema real: la recuperación, no el prompt.

## Cómo lo medí

- **Set congelado de 15 preguntas** (`eval_questions.csv`), cada una con su documento y su dato correctos.
- **Predicciones escritas antes de cada corrida**, y una sola variable cambiada por experimento.
- **Dos niveles de métrica:** recuperación (¿el documento correcto entra al top 3?), que no cuesta nada de API, y respuesta final (¿acierta, cita mal o dice "no sé"?), que solo corrí para configuraciones que mejoraran la recuperación.
- **Reglas de corrección fijas desde el inicio:** acierta solo si aparece el dato correcto; "no sé" si dice que no está; cita mal si da un dato citando un documento que no lo respalda.

## Resultados

| Configuración | hit@3 | Acierta | Cita mal | No sé |
|---|---|---|---|---|
| **Baseline** (1 chunk por PDF, top_k=3, prompt v2) | 10/15 | **10** | 2 | 3 |
| Chunks de 500 caracteres con solapamiento | 9/15 | no corrí respuestas (no mejoró la recuperación) | | |
| top_k = 5 | 10/15 | no corrí respuestas (ningún documento nuevo entró) | | |
| Prompt v3 (regla de relevancia) | 10/15 | 9 | **0** | 6 |

Antes de esto, en el Día 17, pasé el prompt de la v1 a la v2 y medí con 5 preguntas fuera de tema: de 1/5 respuestas limpias a 5/5, y de 1.710 a 469 tokens de salida (muestra chica, una sola corrida).

## Qué aprendí

1. **El cuello de botella es la recuperación.** Las 10 preguntas donde el documento correcto llegó al top 3 salieron bien; las 5 donde no llegó fallaron. El prompt convierte esos fallos en "no sé" en lugar de inventar, que es el fallo que se puede vender.
2. **Hay dos causas distintas de fallo en la recuperación.**
   - *Documentos largos:* el modelo de embeddings solo lee ~128 tokens, así que el dato del final no cuenta. Cortar en chunks de 500 caracteres lo arregló en un caso (el documento pasó del puesto 20 al 3).
   - *Documentos cortos:* quedan lejos en el ranking (puestos 10, 13 y 16 de 27) aunque tengan la respuesta. No es truncamiento; el modelo no emparenta bien esas preguntas con esos textos.
3. **Arreglar una cosa rompe otra.** Los chunks chicos de los documentos largos desplazaron a documentos cortos que antes entraban (2 preguntas perdidas por 1 ganada).
4. **El prompt v3 cambia un tipo de error por otro:** eliminó las citas incorrectas (2 → 0), pero responde "no disponible" de más y perdió un acierto. Con 15 preguntas y una sola corrida no alcanza para declarar un ganador.
5. **Ampliar top_k no ayuda** cuando el documento correcto está muy abajo en el ranking.

## Limitaciones (lo que no puedo afirmar)

- **n = 15, una corrida por pregunta**, y el modelo no es determinista. Son señales, no estadística.
- Falta un segundo set con preguntas más naturales, idealmente escritas por alguien que no conozca los documentos.
- Algunos documentos del corpus se contradicen entre sí. Eso no lo arregla ninguna mejora de recuperación.
- Hoy el sistema **no está listo para producción**: falla en 1 de cada 3 preguntas. Lo que sí tengo es una forma de medirlo y un diagnóstico de dónde falla.

## Próximos pasos

Cambiar el modelo de embeddings (opciones multilingües con ventana más larga, como `bge-m3` o `multilingual-e5`) y repetir exactamente la misma evaluación. Después, probar búsqueda híbrida (BM25 + embeddings) o un reranker.

## Archivos

| Archivo | Para qué |
|---|---|
| `rag_system.py` | Carga los PDFs, genera chunks y construye la base vectorial |
| `chatbot.py` | Consulta la base y llama a Claude (prompts v2 y v3) |
| `eval_questions.csv` | Las 15 preguntas con documento y dato correctos |
| `eval_retrieval.py` | Evaluación de recuperación (sin costo de API) |
| `eval_run.py` | Evaluación de respuestas completas |
| `eval_results_baseline.csv`, `eval_results_v3.csv` | Resultados corregidos |
| `notas.md` | Diario completo de experimentos, incluidas mis predicciones y mis errores |

## Cómo correrlo

```bash
pip3 install pypdf chromadb sentence-transformers anthropic python-dotenv
# Poné tu clave en un archivo .env:  ANTHROPIC_API_KEY=...
python3 rag_system.py     # construye la base vectorial
python3 chatbot.py        # hace preguntas
python3 eval_retrieval.py # mide la recuperación
```

Nota: `rag_system.py` quedó configurado en el último experimento (chunks de 500, base `./rag_db_c500`). Para reproducir el baseline hay que usar `chunk_size=None` y `db_path="./rag_db"` en su bloque `__main__`.
