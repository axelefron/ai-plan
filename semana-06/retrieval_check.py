from chatbot import collection
from rag_system import search, display_results

failed_questions = [
"¿Cómo se calcula el interés diario de mi tarjeta?",
"¿Qué es un credit freeze y cuánto cuesta?",
"Si me roban la tarjeta, ¿cuánto es lo máximo que puedo perder?"
]

for question in failed_questions:
    results = search(collection, question, top_k=10)
    display_results(results, question)