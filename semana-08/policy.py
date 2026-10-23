import re
from pathlib import Path
from langfuse import observe

REPORTS_DIR = Path(__file__).parent / "reports"
FILENAME_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}\.txt")   # nombre simple, solo .txt
MAX_CONTENT_CHARS = 20_000

def untrusted_text(state):
    """Todo lo que devolvió search_docs en esta corrida: texto de terceros, no confiable."""
    ids, chunks = set(), []
    for m in state["messages"]:
        if not isinstance(m["content"], list):
            continue
        if m["role"] == "assistant":
            ids.update(b["id"] for b in m["content"]
                       if b.get("type") == "tool_use" and b.get("name") == "search_docs")
        else:
            chunks += [str(b.get("content", "")) for b in m["content"]
                       if b.get("type") == "tool_result" and b.get("tool_use_id") in ids]
    return "\n".join(chunks)

@observe(name="policy-check")
def authorize(tool_name, tool_input, state):
    """Devuelve (permitido, motivo). Código determinístico: no depende de qué 'entendió' el modelo."""
    if tool_name == "save_report":
        filename = str(tool_input.get("filename", ""))
        content = str(tool_input.get("content", ""))

        if not FILENAME_RE.fullmatch(filename):
            return False, "filename must be a simple name ending in .txt (letters, digits, - and _ only)"
        if len(content) > MAX_CONTENT_CHARS:
            return False, "content too long"
        if (REPORTS_DIR / filename).resolve().parent != REPORTS_DIR.resolve():
            return False, "path escapes the reports directory"
        if filename in untrusted_text(state) and filename not in state["user_message"]:
            return False, "filename came from a retrieved document, not from the user"
    return True, "ok"
