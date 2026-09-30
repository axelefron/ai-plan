from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"

system_prompt = """
You are a patient AI consultant. Do not hand the user the answer directly, make him reason by asking guiding questions. 
Guide them as if they are completely unfamiliar with the topic.
"""

messages = [
    {
        "role" : "user",
        "content" : "What does Higgsfield AI do best?"
    }
]

def chat(messages, system=None, temperature=0.5):
    params = {
        "model" : model,
        "max_tokens" : 1000,
        "messages" : messages,
        "temperature" : temperature
    }

    if system:
        params["system"] = system
    message = client.messages.create(**params)
    
    return message.content[0].text

answer = chat(messages, system=system_prompt)
print(answer)
