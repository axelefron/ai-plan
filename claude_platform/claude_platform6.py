from pathlib import Path
from dotenv import load_dotenv
import anthropic
from anthropic.lib import files_from_dir

load_dotenv()
client = anthropic.Anthropic()

skill_dir = Path(__file__).parent / "status-report-skill"

skill = client.skills.create(
    display_name="Status Report Generator",
    files=files_from_dir(skill_dir),  # folder containing SKILL.md
)

print(skill.id)  # reference this ID in future requests