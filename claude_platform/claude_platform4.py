from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=10000,
    thinking={"type": "adaptive", "display": "summarized"},
    output_config={"effort": "medium"},  
    messages=[
        {
            "role": "user",
            "content": "Plan a round road trip from Naples to Sanibel today, "
                       "weighing weather, drive time and some food options for lunch in Sanibel and dinner in Naples city."
                       "I am 20 years old and I am with my dad. We like the beach and are open to general recommendations",
        }
    ],
)

for block in response.content:
    if block.type == "thinking":
        print(f"--- Thinking ---\n{block.thinking}\n")
    elif block.type == "text":
        print(f"--- Answer ---\n{block.text}\n")