from dotenv import load_dotenv
from anthropic import Anthropic
import json

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"

tools = [
    {
        "name" : "addition",
        "description" : "Add integers a and b given by the user",
        "input_schema" : {
            "type" : "object",
            "properties" : {
                "a" : {"type" : "integer", "description" : "A whole number e.g. 2"},
                "b" : {"type" : "integer", "description" : "A whole number e.g. 4"},
            },
            "required" : ["a", "b"]
        },
    }
]

def execute_tool(tool_name, tool_input):
    if tool_name == "addition":
        result = tool_input["a"] + tool_input["b"]
        return result

a = int(input("Enter a: "))
b = int(input("Enter b: "))

while True:
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        tools=tools,
        tool_choice={"type": "tool", "name": "addition"},
        messages=[{"role": "user", "content" : f"What is {a} + {b}?"}],
    )
    print("=" * 50)
    print(f"user: What is {a} + {b}?")
    print("=" * 50)

    tool_use = next(block for block in response.content if block.type == "tool_use")
    print(f"Claude called {tool_use.name} with {json.dumps(tool_use.input)}")

    result = execute_tool(tool_use.name, tool_use.input)
    print(f"Tool result: {result}\n")

    tool_result = {
        "type": "tool_result",
        "tool_use_id": tool_use.id,  # ← el ID que Claude te pasó
        "content": str(result)        # ← el resultado de la tool
    }

    followup = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"What is {a} + {b}?"},  # Mensaje original
            {"role": "assistant", "content": response.content},  # Respuesta de Claude con tool_use
            {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool_use.id, "content": str(result)}]}  # El resultado
        ],
    )
    
    try:
        final_text = next(block for block in followup.content if block.type == "text")
        print("=" * 50)
        print(f"Final answer: {final_text.text}")
        print("=" * 50)
    except StopIteration:
        print("=" * 50)
        print("No final text from Claude")
        print("=" * 50)
    break   