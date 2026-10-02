from dotenv import load_dotenv
from anthropic import Anthropic
from classifier import system_prompt

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5"

example_message = "My card ending in 9341 went missing at the campus rec center. " \
"I'm a student and I don't have much money so I'm really stressed about this. \
Can you help?"

messages = [
    {"role": "user", "content": f"<message>{example_message}</message>"},
    {"role": "assistant", "content": "```json"},
]

message = client.messages.create(
    model=model,
    max_tokens=8000,
    messages=messages,
    system=system_prompt,
    stop_sequences=["```"],
)

price_input_usd = 1
price_output_usd = 5
one_message_cost = (message.usage.input_tokens / 1_000_000) * price_input_usd + (message.usage.output_tokens / 1_000_000) * price_output_usd

print(message.usage)
print(f"1 message:   ${one_message_cost:.6f}")
print(f"200 messages: ${one_message_cost * 200:.2f}")
print(f"100,000 messages:      ${one_message_cost * 100_000:.2f}")