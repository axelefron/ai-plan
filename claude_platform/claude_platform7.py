from pathlib import Path
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

SKILL_ID = "skill_01KAmNRD7B9EvZxha7wfXiDs"  # the ID from first upload

activity_log = (Path(__file__).parent / "activity_log.txt").read_text()

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=4096,
    container={
        "skills": [
            {
                "type": "custom",
                "skill_id": SKILL_ID,
                "version": "latest",
            }
        ]
    },
    tools=[
        {
            "type": "code_execution_20250825",
            "name": "code_execution",
        }
    ],
    messages=[
        {
            "role": "user",
            "content": f"Generate the daily status report from this activity log:\n\n{activity_log}",
        }
    ],
)

for block in response.content:
    if block.type == "text":
        print(block.text)