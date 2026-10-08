# Demo del agente

Esta demo muestra cómo se comporta el agente en tres escenarios distintos: una tool que falla, una búsqueda sin resultados y un flujo completo exitoso.

## 1. Error en una tool

```text
Find 2 furniture products and apply a 15% discount. If the search fails, explain why without making up data
```

La búsqueda de `furniture` está configurada intencionalmente para devolver un error de conexión.

En vez de romper el programa, el error vuelve a Claude como resultado de la tool. Claude reconoce la falla y explica que no puede calcular el descuento sin acceder a los productos y sus precios.

En esta ejecución no reintenta la búsqueda ni inventa datos.

## 2. Resultado vacío

```text
Find 3 peripherals and apply a 10% discount. If no products are found, create and save a report explaining the result. Do not use sample prices
```

Para `peripherals`, `search_in_csv` devuelve intencionalmente un resultado vacío.

En esta ejecución Claude reconoce que no encontró productos y, en lugar de inventar precios o calcular un descuento sin datos, utiliza `save_report` para generar `peripherals_discount_report.txt`.

El reporte explica que no se encontraron productos, por qué no pudo calcularse el descuento y qué aspectos de la base de datos convendría revisar.

**Insight:** Esto muestra que una tool puede ejecutarse sin lanzar una excepción y aun así no devolver datos útiles. En este caso, Claude manejó correctamente el resultado vacío, aunque sigue siendo importante validar estos casos desde el código y no depender únicamente del prompt.

## 3. Flujo exitoso

```text
Find 2 electronics, apply a 20% discount and save a report called electronics_demo.txt
```

En este caso se completa correctamente todo el flujo:

```text
search_in_csv → calculate_discount → save_report → respuesta final
```

El agente encuentra dos productos reales en el CSV:

```text
Laptop Dell XPS 13 → $1200
Monitor LG 27 pulgadas → $350
```

Luego pasa esos precios a `calculate_discount` y aplica el 20%:

```text
Total original: $1550
Descuento (20%): $310
Total final: $1240
```

Finalmente, guarda el resultado en `electronics_demo.txt`.

En este caso también se simula una demora de 3 segundos al guardar el reporte.

## Qué muestra la demo

La idea de la demo es probar no solo que las tools funcionan, sino también qué hace el agente cuando algo no sale como esperaba.

Se prueban tres situaciones:

- Una tool que falla y devuelve un error.
- Una tool que funciona pero no devuelve datos.
- Un flujo normal donde el resultado de una tool se usa como input de la siguiente.

Los dos reportes generados se abren automáticamente en VS Code para mostrar los resultados en tiempo real. Al final también se muestra el archivo `data.csv`, utilizado como base de productos.

Cada ejecución muestra su consumo de tokens y, al cerrar el programa con `exit`, se imprime el `SESSION LOG` con las llamadas a las tools, sus resultados y los errores registrados.

## Métricas de tokens

Consumo total por ejecución:

| Test | Input tokens | Output tokens | Total |
|---|---:|---:|---:|
| Furniture — Error | 1,960 | 204 | **2,164** |
| Peripherals — Empty | 3,300 | 440 | **3,740** |
| Electronics — Success | 4,606 | 487 | **5,093** |

Los valores corresponden a la ejecución mostrada en la demo.