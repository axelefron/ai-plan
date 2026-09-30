# ============================================================
# Managed agent: Claude runs in an Anthropic cloud container
# and completes a task on its own (create a file, count lines)
# ============================================================

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

# 1) AGENT: the "who" — model, instructions and tools
agent = client.beta.agents.create(
    name="Line Counter",
    model="claude-sonnet-4-5",
    system="You are a helpful agent that completes small file tasks.",
    tools=[
        # Built-in toolset (bash, files, etc.), all enabled
        {"type": "agent_toolset_20260401", "default_config": {"enabled": True}}
    ],
)

# 2) ENVIRONMENT: the "where" — the cloud container it runs in
environment = client.beta.environments.create(
    name="line-counter-env",
    config={
        "type": "cloud",
        "networking": {"type": "unrestricted"},  # internet access
    },
)

# 3) SESSION: one specific run of the agent in that environment
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    title="Count lines demo",
)

# 4) Open the stream FIRST, so you don't miss any events
with client.beta.sessions.events.stream(session_id=session.id) as stream:

    # Send the task to the agent
    client.beta.sessions.events.send(
        session_id=session.id,
        events=[
            {
                "type": "user.message",
                "content": [
                    {
                        "type": "text",
                        "text": "Create a file in the temp directory, "
                                "count its lines, and report back.",
                    }
                ],
            }
        ],
    )

    # 5) Read events live — MUST be INSIDE the "with"
    for event in stream:
        if event.type == "agent.message":            # the agent writes text
            for block in event.content:
                if block.type == "text":
                    print(block.text, end="", flush=True)
        elif event.type == "agent.tool_use":         # the agent uses a tool
            print(f"\n[tool] {event.name}")
        elif event.type == "session.status_idle":    # finished, waiting for input
            print("\n--- Agent done ---")
            break