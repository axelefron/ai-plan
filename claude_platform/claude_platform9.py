# ============================================================
# Example: Context management (server-side compaction) + MCP
# A chat with Linear where the API summarizes old history
# on its own when the context gets too large.
# ============================================================
#
# The idea:
#   - Every turn you resend the ENTIRE history (messages)
#   - With MCP, each call already costs ~30k tokens in tool definitions
#   - After a few turns the history grows until the context fills up
#   - With compaction, when input crosses the "trigger", the API
#     replaces the old turns with a summary and keeps going
# ============================================================

import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()                     # loads ANTHROPIC_API_KEY and LINEAR_MCP_TOKEN
client = anthropic.Anthropic()

# The conversation history. It grows every turn
messages = []

print("Chat with Linear. Type 'exit' to quit.\n")

while True:
    # ---- 1) Your question ----
    question = input("You: ").strip()
    if question.lower() in ("exit", "quit"):
        break
    messages.append({"role": "user", "content": question})

    # ---- 2) The call: MCP + compaction together ----
    response = client.beta.messages.create(
        model="claude-opus-5",
        max_tokens=2048,
        messages=messages,  # the ENTIRE history, not just the last question

        # MCP: the connection to Linear
        mcp_servers=[
            {
                "type": "url",
                "url": "https://mcp.linear.app/mcp",
                "name": "linear",
                "authorization_token": os.environ["LINEAR_MCP_TOKEN"],
            }
        ],
        tools=[{"type": "mcp_toolset", "mcp_server_name": "linear"}],

        # NEW: context management
        context_management={
            "edits": [
                {
                    "type": "compact_20260112",
                    # When to summarize. Without "trigger" it uses the default threshold
                    # (much higher). A low value lets you see it happen within a few turns.
                    # If the API rejects it, raise it (there's a minimum).
                    "trigger": {"type": "input_tokens", "value": 50000},
                }
            ]
        },

        # Two betas at once: one for MCP, one for compaction
        betas=["mcp-client-2025-11-20", "compact-2026-01-12"],
    )

    # ---- 3) Show what happened ----
    for block in response.content:
        if block.type == "compaction":
            # The summary the API created of the old turns
            print("\n*** COMPACTION: the API summarized the previous history ***")
        elif block.type == "mcp_tool_use":
            print(f"  [Calls Linear] {block.name} {json.dumps(block.input, ensure_ascii=False)}")
        elif block.type == "mcp_tool_result":
            print(f"  [Linear returns data]{' (ERROR)' if block.is_error else ''}")
        elif block.type == "text":
            print(f"\nClaude: {block.text}\n")

    # ---- 4) Save Claude's answer into the history ----
    # IMPORTANT: append response.content AS IS (including the compaction block).
    # On the next turn, the API sees that block and drops everything before it,
    # using the summary in its place.
    messages.append({"role": "assistant", "content": response.content})

    # ---- 5) Context meter ----
    print(f"  [Tokens this turn: input={response.usage.input_tokens}, "
          f"output={response.usage.output_tokens}]\n")