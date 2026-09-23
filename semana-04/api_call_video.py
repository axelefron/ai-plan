from dotenv import load_dotenv
import anthropic

load_dotenv() # loads the antrhopic API Key from my .env
client = anthropic.Anthropic() # reads the key from the environment automatically

buggy_code = """
def add(a, b):
    return a - b 
"""

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    system="You are a terse senior code reviewer. Give feedback in just one paragraph.",
    messages=[{"role" : "user", "content" : f"Review this code:\n{buggy_code}"},
    ],
)

for block in response.content:
    if block.type == "text":
        print(block.text)