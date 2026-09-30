from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

# 1. Definimos las funciones reales
def get_weather(city: str) -> str:
    return f"Weather in {city}: 72°F, sunny"

def get_forecast(city: str) -> str:
    return f"Forecast for {city}: Sunny today, rain tomorrow, clear on day 3."

# 2. Definimos las herramientas en un diccionario limpio
tools = [
    {
        "name": "get_weather",
        "description": "Get today's current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "The city to check"}},
            "required": ["city"],
        },
    },
    {
        "name": "get_forecast",
        "description": "Get the weather forecast for the next few days for a city.",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "The city to check"}},
            "required": ["city"],
        },
    },
]

# Mapa para vincular el nombre de la herramienta con su función
tool_map = {"get_weather": get_weather, "get_forecast": get_forecast}

messages = [{"role": "user", "content": "I'm packing for a three-day trip to Denver. What's the weather today and over the next few days?"}]

# 3. Bucle compacto
response = client.messages.create(model="claude-sonnet-5", max_tokens=1024, tools=tools, messages=messages)

while response.stop_reason == "tool_use":
    messages.append({"role": "assistant", "content": response.content})
    tool_results = []
    
    for block in response.content:
        if block.type == "tool_use":
            result = tool_map[block.name](**block.input)
            tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
            
    messages.append({"role": "user", "content": tool_results})
    response = client.messages.create(model="claude-sonnet-5", max_tokens=1024, tools=tools, messages=messages)

print("".join([b.text for b in response.content if b.type == "text"]))