from dotenv import load_dotenv
from anthropic import Anthropic
load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"

# Start with an empty message list
messages = []

def add_user_message(messages, text):
    user_message = {"role" : "user", "content" : text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role" : "assistant", "content" : text}
    messages.append(assistant_message)

def chat(messages):
    message = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages
    )
    return message.content[0].text

# Add the initial user question
add_user_message(messages, "What is an API?")

# Get Claude's response
answer = chat(messages)
print(answer)

# Add Claude's response to the conversation history
add_assistant_message(messages, answer)

# Add a follow-up question
add_user_message(messages, "And an MCP? What's the difference?")

# Get the follow-up response with full context
final_answer = chat(messages)

print(final_answer)


