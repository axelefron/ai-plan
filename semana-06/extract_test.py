from pypdf import PdfReader
from pathlib import Path
import os

# Debug
print(f"Carpeta actual: {os.getcwd()}")
print(f"Contenido de docs/: {os.listdir('docs')[:5]}")

# Encuentra el primer PDF
docs_folder = Path("docs")
pdf_files = sorted(docs_folder.glob("*.pdf"))

print(f"PDFs encontrados: {len(pdf_files)}")

if pdf_files:
    pdf = PdfReader(str(pdf_files[0]))
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    
    print(f"\n=== {pdf_files[0].name} ===")
    print(text[:800])
    print(f"\n... STATS ...")
    print(f"Palabras: {len(text.split())}")