import json
import re
import sys

# Dónde puede aparecer el nombre de un archivo en los parámetros de una herramienta.

CLAVES = ["file_path", "notebook_path", "path", "command"]

# Un ".env" que sea un nombre de archivo completo, no parte de otro nombre
# Pasa ".env" y ".env.local", pero no ".venv" ni "load_dotenv"

PATRONES = re.compile(r"(^|[/\s\"'=<>|;&(])\.env(?![A-Za-z0-9_-])")

def main():
    try:
        datos = json.load(sys.stdin)
    except Exception:
        sys.exit(0) # Si no puedo leer el JSON, no bloqueo nada

    params = datos.get("tool_input", {})
    for clave in CLAVES:
        valor = params.get(clave)
        if isinstance(valor, str) and PATRONES.search(valor):
            print("Bloqueado por protect_env.py: no se puede acceder a .env", file=sys.stderr)
            sys.exit(2) # Código 2 = bloquear la herramienta

    sys.exit(0)  # Cualquier otro caso: dejar pasar


main()

