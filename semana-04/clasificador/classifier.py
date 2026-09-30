from dotenv import load_dotenv
from anthropic import Anthropic
import json
import csv

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5"

system_prompt = """
    You classify messages that customers send to the support team of a
    credit/debit card issuer in the United States.

    For each message, output exactly these four fields:

    category — use exactly one of these values:
    lost_stolen_card
    charge_dispute
    account_locked
    account_reactivation
    general_inquiry

    sentiment — use exactly one of these values:
    positive
    neutral
    negative

    priority — use exactly one of these values:
    high    money is at risk right now, or the customer cannot access their funds
    medium  a real problem, but no immediate urgency
    low     an informational question

    summary — one sentence, 15 words maximum, describing what the customer needs.

    Rules:
    - Use only the exact values listed above. Never invent new ones.
    - If a message covers more than one situation, pick the category that reflects
    what the customer most needs resolved.
    - Never include card numbers, SSNs, names or any other personal data in the
    summary. Refer to a card only as "the card ending in XXXX".

    Return ONLY a JSON object with the keys category, sentiment, priority and
    summary. No commentary, no explanation, no extra keys.
"""

def add_user_message(messages, text):
    user_message = {"role" : "user", "content" : text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role" : "assistant", "content" : text}
    messages.append(assistant_message)

def chat(messages, system=None, stop_sequences=None):
    params = {
        "model": model,
        "max_tokens": 8000,
        "messages": messages,
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    message = client.messages.create(**params)
    return message.content[0].text

def classify(text):
    messages = []
    add_user_message(messages, f"<message>{text}</message>")
    add_assistant_message(messages, "```json")
    response = chat(messages, system=system_prompt, stop_sequences=["```"])
    clean_json = json.loads(response.strip())
    return clean_json

if __name__ == "__main__":
    test1 = "lost card"
    test2 = "Someone must have taken my card ending in 5493 from the university library. I didn't notice until I tried to pay for lunch. There's a charge for $34.99 at a gas station. I want dispute this charge but I also need new card immediately."
    test3 = "my card ending in 5491 - account was paused, how long does it take to reactive"
    test4 = "lost card ending 7834 in Denver. need replacement sent to my home address in Boston ASAP"
    test5 = "Can you push a software update to automatically transfer recurring charges to new card numbers like other financial institutions do? This manual process is ridiculous."

    print(classify(test1))
    print(classify(test2))
    print(classify(test3))
    print(classify(test4))
    print(classify(test5))