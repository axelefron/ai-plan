# Semana 07 · Servidor MCP sobre Chroma

`mcp_chroma_server.py` es un servidor MCP (con `FastMCP`, nombre `DocumentMCP`) que expone la base vectorial de documentos del banco armada en la semana 06 como tools que puede usar un cliente MCP.

- Base: `semana-06/rag_db` (ruta calculada desde la ubicación del script, no desde el directorio actual).
- Colección: `banking_docs`.
- Embeddings: reutiliza `get_embedding_function()` y `clean_text()` de `semana-06/rag_system.py`. El modelo se carga una sola vez (`lru_cache`) la primera vez que una tool abre la base.
- Transporte: `stdio`.

## Las 3 tools

| Tool | Parámetros | Qué hace | ¿Modifica la base? |
|---|---|---|---|
| `search_docs` | `consultation: str`, `n_results: int = 3` | Búsqueda semántica en la colección. Devuelve los fragmentos más parecidos, cada uno precedido por `[Fuente: <título>]`. | No |
| `add_document` | `title: str`, `content: str` | Agrega un documento nuevo como un solo fragmento. | **Sí — es la única que escribe** |
| `list_documents` | — | Lista los títulos de los documentos indexados, sin repetir y en orden alfabético. | No |

### `search_docs`
- Recorta espacios de la consulta; si queda vacía no busca.
- La cantidad de resultados se ajusta a `max(1, min(n_results, 10, total_en_la_base))`: como mínimo 1, como máximo 10 (`MAX_RESULTS`) y nunca más que los fragmentos que hay.

### `add_document`
Antes de escribir valida, en este orden:
1. Título y contenido no vacíos (el título se recorta con `strip()` y el contenido se limpia con `clean_text()`).
2. Contenido de al menos 50 caracteres (`MIN_CHARS`) y como máximo 20000 (`MAX_CHARS`).
3. Que la base exista.
4. Que no haya ya un fragmento con ese mismo `title`.
5. Que no exista ya ese contenido: el id es `doc_` + los primeros 16 caracteres del SHA-256 del contenido, así que el mismo texto con otro título se rechaza.

Si pasa todo, guarda el texto con el formato `Tema: <título con "_" reemplazado por espacios>` + `Contenido:` y metadatos `source="mcp"`, `title`, `char_count` y `part=0`.

### `list_documents`
- Agrupa por `title`: un documento partido en varios fragmentos aparece una sola vez.
- Los fragmentos sin título no se listan; se informa cuántos son.
- Trae los metadatos de todos los fragmentos de una vez (el comentario del código aclara que con miles de documentos habría que paginar).
- A diferencia de `list_documents`, `search_docs` lee `meta['title']` directamente: si un fragmento devuelto no tiene `title`, la tool falla con `KeyError` en vez de devolver un mensaje.

## Qué devuelve cada tool cuando falta la base o está vacía

"Falta la base" incluye dos casos que el código trata igual: que no exista la carpeta `semana-06/rag_db` o que exista pero no tenga la colección `banking_docs`.

| Tool | Sin base | Base vacía |
|---|---|---|
| `search_docs` | `Base no encontrada. Corré rag_system.py primero.` | `La base está vacía. Agregá documentos antes de buscar.` |
| `add_document` | `Base no encontrada. Corré rag_system.py primero.` | No hay caso especial: agrega el documento normalmente (las validaciones de arriba siguen aplicando). |
| `list_documents` | `Base no encontrada. Corré rag_system.py primero.` | `La base está vacía. No hay documentos indexados.` |

Notas:
- En `search_docs` y `add_document`, las validaciones de entrada (consulta vacía, título/contenido vacío, largo) se chequean **antes** de abrir la base, así que con una entrada inválida devuelven ese error aunque la base no exista.
- `list_documents` tiene un caso intermedio: si hay fragmentos pero ninguno tiene título, devuelve `Hay N fragmentos en la base pero ninguno tiene título.`

## Cómo correrlo

Requisitos: el entorno virtual del repo (`.venv`) con `mcp`, `chromadb`, `pypdf` y `sentence-transformers` instalados (los dos últimos los importa `semana-06/rag_system.py`, que el servidor importa al arrancar), y Python 3.12 o superior (el código usa comillas dobles dentro de un f-string).

```bash
.venv/bin/python semana-07/mcp_chroma_server.py
```

El servidor habla por `stdio`: al correrlo a mano queda esperando mensajes MCP por la entrada estándar y no imprime nada (el log está en nivel `ERROR`). Se corta con Ctrl+C. Lo normal es que lo lance el cliente, no uno a mano.

La base tiene que existir antes en `semana-06/rag_db` con la colección `banking_docs`.

> Ojo: el mensaje de error dice "Corré rag_system.py primero", pero hoy el bloque `__main__` de `semana-06/rag_system.py` crea la base en `./rag_db_c500`, no en `./rag_db`. Correrlo tal como está no genera la carpeta que lee este servidor.
>
> Además, `create_rag_database()` borra la colección `banking_docs` antes de recrearla. Si se regenera la base que lee este servidor, se pierden los documentos agregados con `add_document`.

## Conectarlo a Claude Desktop

En el archivo de configuración de Claude Desktop (`claude_desktop_config.json`), agregar una entrada dentro de `mcpServers`. Usar **rutas absolutas** tanto para el intérprete como para el script:

```json
{
  "mcpServers": {
    "banking-docs": {
      "command": "/RUTA/ABSOLUTA/AL/REPO/.venv/bin/python",
      "args": ["/RUTA/ABSOLUTA/AL/REPO/semana-07/mcp_chroma_server.py"]
    }
  }
}
```

- `command`: el Python del `.venv`, para que encuentre `mcp`, `chromadb` y el modelo de embeddings.
- `args`: la ruta al script. No hace falta `cwd`: el script calcula la ruta de la base y de `rag_system.py` a partir de su propia ubicación.
- El nombre de la clave (`banking-docs` en el ejemplo) se puede elegir; no lo usa el código del servidor.

Como `add_document` es la única tool que modifica la base, es la que conviene aprobar a mano cada vez que el cliente la quiera usar.
