from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

# El arreglo 'tools' define qué herramientas están disponibles para Claude:
# nombre, descripción y el esquema JSON para las entradas.
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to get weather for",
                }
            },
            "required": ["city"],
        },
    }
]

# 'run_tool' es una simulación de ejecución de la herramienta.
def run_tool(name, tool_input):
    if name == "get_weather":
        return f"Weather in {tool_input['city']}: 30c, sunny"
    raise ValueError(f"Unknown tool: {name}")


messages = [
    {"role": "user", "content": "What should I wear in Naples today?"}
]

# El bucle del agente (Agent Loop).
while True:
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=500,
        tools=tools,
        messages=messages,
    )

    if response.stop_reason == "end_turn":
        # Claude ha terminado la respuesta final. Imprimimos el texto y salimos.
        for block in response.content:
            if block.type == "text":
                print(block.text)
        break

    if response.stop_reason == "tool_use":
        # Identificamos los bloques de uso de herramientas y los ejecutamos.
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = run_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        # Agregamos la respuesta de Claude y el resultado de la herramienta al historial
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})