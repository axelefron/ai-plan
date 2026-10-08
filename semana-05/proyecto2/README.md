# Chained Task Agent with Error Handling

Agente de Claude que busca productos en un CSV, calcula descuentos y guarda reportes.

La idea principal del proyecto es probar cómo un agente maneja fallas en sus tools sin romper toda la ejecución ni inventar datos. Para testearlo, forcé tres escenarios: una tool que devuelve un error, una búsqueda que devuelve un resultado vacío y una tool con latencia artificial.

## Tools

- `search_in_csv`: busca productos por categoría o precio dentro de `data.csv`.
- `calculate_discount`: calcula un descuento sobre los precios encontrados.
- `save_report`: guarda el resultado en un `.txt`.

El dataset simula un e-commerce e incluye `id`, `product`, `price`, `stock` y `category`.

## Error handling

Probé tres casos:

| Caso | Comportamiento |
|---|---|
| `furniture` | Fuerza un `ValueError` simulando una pérdida de conexión |
| `peripherals` | Devuelve `""` para simular una búsqueda sin resultados |
| `save_report` | Usa `time.sleep(3)` para simular latencia |

El punto clave fue manejar las excepciones dentro del loop de tools. Si una tool falla, el error vuelve a Claude como un `tool_result` con `is_error: True`. De esta forma, Claude puede decidir cómo continuar en vez de que el programa simplemente termine.

También agregué un log de cada tool call con su input, output, estado de error y tokens utilizados.

## Run

```bash
python3 agent_error_handling.py
```

Ejemplo:

```text id="cq9z41"
Find 3 electronics, apply a 20% discount to their prices, and save the results in a report called electronics_test.txt.
```

Flujo:

```text id="2hox1p"
search_in_csv → calculate_discount → save_report → final response
```

## Tests

```text id="gkik6x"
# Error
Find 2 furniture products and apply a 15% discount. If the search fails, explain why without inventing data.

# Empty result
Find 3 peripherals and apply a 10% discount. If no products are found, save a report explaining the result. Do not use sample prices.

# Normal flow + slow tool
Find 2 electronics, apply a 20% discount, and save a report called electronics_demo.txt.
```

En los tests, el agente pudo manejar tanto errores como resultados vacíos sin inventar productos o precios, y continuar normalmente cuando una tool tardaba en responder.

## Métricas de tokens

Token usage acumulado por ejecución:
- Error case: 2,164 tokens
- Empty result: 3,740 tokens  
- Normal flow: 5,093 tokens

## Takeaway

El `try/except` afuera de `run_agent()` sirve para evitar que el programa muera por un error inesperado, pero no alcanza para que el agente pueda reaccionar.

Al manejar el error dentro del loop y devolverlo como `tool_result`, Claude también recibe información sobre qué falló y puede decidir qué hacer después.