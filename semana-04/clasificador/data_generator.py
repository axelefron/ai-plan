from dotenv import load_dotenv
from anthropic import Anthropic
import json
import csv

load_dotenv()

client = Anthropic()
model = "claude-haiku-4-5"

def add_user_message(messages, text):
    user_message = {"role" : "user", "content" : text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role" : "assistant", "content" : text}
    messages.append(assistant_message)

def chat(messages, stop_sequences=None):
    message = client.messages.create(
    model=model,
    max_tokens=8000,
    messages=messages,
    stop_sequences=stop_sequences
    )
    return message.content[0].text

prompt_generator = """
    Generate 20 realistic messages that customers send to the support team
    of a credit/debit card issuer in the United States.

    Cover a mix of these situations:
    - a card was lost or stolen
    - a charge on the statement the customer does not recognize or disputes
    - the account got locked or frozen and the customer cannot log in
    - the customer wants a closed or paused account reactivated
    - a general question about fees, limits, statements or replacement cards

    Make them look like real people wrote them:
    - vary the length a lot: some are 5 words, some are a full paragraph
    - vary the tone: calm, confused, frustrated, angry, polite
    - include typos, lowercase, run-on sentences and missing punctuation in some
    - a few should be written by non-native English speakers
    - include just 3 or 4 that are genuinely ambiguous: the customer mixes two
    problems, or it is unclear what they actually want

    Never include full card numbers, SSNs, full addresses or any other data
    that could look like real private information. Use only last 4 digits,
    like "the card ending in 4412".

    Return ONLY a JSON array of strings. No numbering, no keys, no objects,
    no commentary. Just a list of 20 message strings.
"""

all_messages = []

angles = [
    "customers whose card was lost or stolen while traveling out of town or abroad",
    "customers whose card was lost or stolen at a restaurant, a shopping mall or a university campus in the US",
    "customers complaining about the fees charged for a replacement card or expedited shipping",
    "customers whose account got locked or frozen within hours of reporting the card lost or stolen",
    "customers trying to reactivate an account that was paused or closed, some happy with the process and some not",
    "customers asking what happens to their autopays and subscriptions when the card number is cancelled",
    "customers who are not sure whether the card was lost or actually stolen, and do not know how to report it",
    "customers asking whether they can keep the same card number instead of getting a brand new one",
    "customers unsure whether to open a new account or just request a replacement card after losing theirs",
    "customers frustrated about having to re-link every subscription and payment after receiving a new card number",
]

for i in range(10):
    messages = []
    add_user_message(messages, f"{prompt_generator}\n\nFor this batch: {angles[i]}")
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])
    batch = json.loads(text.strip())
    all_messages.extend(batch)
    print(f"Batch {i +1}/10 - {len(all_messages)} so far")

with open("messages.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["text"])
    for message in all_messages:
        writer.writerow([message])

print(len(all_messages))