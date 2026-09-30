# ============================================================
# MCP example: see step by step what Claude does with Linear
# ============================================================
#
# How it works:
#   1. You send a question + the address of the MCP server (Linear)
#   2. Anthropic's servers connect to Linear and ask it: "which tools do you have?"
#   3. Claude reads that list and decides which tool it needs
#   4. Anthropic calls that tool on Linear (not your computer)
#   5. Linear returns data -> Claude reads it -> writes the answer
#   All of this happens INSIDE a single API call.
# ============================================================

import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()                     # loads ANTHROPIC_API_KEY and LINEAR_MCP_TOKEN
client = anthropic.Anthropic()

# ------------------------------------------------------------
# Your question. Change it to test different things:
#   "List my Linear teams"
#   "What issues are assigned to me?"
#   "Show my 5 most recent issues with their status"
# ------------------------------------------------------------
QUESTION = "List my Linear teams and my 5 most recent issues."

print("=" * 60)
print("QUESTION:", QUESTION)
print("=" * 60)

# ------------------------------------------------------------
# The call: one request, but inside it Claude can call Linear
# several times
# ------------------------------------------------------------
response = client.beta.messages.create(
    model="claude-opus-5",
    max_tokens=2048,
    messages=[{"role": "user", "content": QUESTION}],

    # WHERE to connect
    mcp_servers=[
        {
            "type": "url",
            "url": "https://mcp.linear.app/mcp",
            "name": "linear",
            "authorization_token": os.environ["LINEAR_MCP_TOKEN"],
        }
    ],

    # WHICH tools from that server Claude can use (here: all of them)
    tools=[{"type": "mcp_toolset", "mcp_server_name": "linear"}],

    betas=["mcp-client-2025-11-20"],
)

# ------------------------------------------------------------
# The response is a LIST of blocks, in the order things happened.
# We go through them one by one to see the full flow.
# ------------------------------------------------------------
step = 1
for block in response.content:

    # Claude decides to use a Linear tool
    if block.type == "mcp_tool_use":
        print(f"\n[STEP {step}] Claude CALLS a Linear tool")
        print(f"   Server:    {block.server_name}")
        print(f"   Tool:      {block.name}")
        print(f"   Arguments: {json.dumps(block.input, ensure_ascii=False)}")
        step += 1

    # Linear responds with real data
    elif block.type == "mcp_tool_result":
        print(f"\n[STEP {step}] Linear RETURNS data")
        if block.is_error:
            print("   There was an error in the call!")
        for item in block.content:            # the result comes as a list of pieces
            if item.type == "text":
                print("   " + item.text[:500])  # first 500 characters so it doesn't flood the terminal
                if len(item.text) > 500:
                    print("   ... (truncated)")
        step += 1

    # Claude writes text (it may think out loud or give the final answer)
    elif block.type == "text":
        print(f"\n[STEP {step}] Claude WRITES:")
        print(block.text)
        step += 1

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------
calls = [b for b in response.content if b.type == "mcp_tool_use"]
print("\n" + "=" * 60)
print(f"Calls to Linear: {len(calls)} -> {[c.name for c in calls]}")
print(f"Input tokens:    {response.usage.input_tokens}")
print(f"Output tokens:   {response.usage.output_tokens}")
print(f"Why it stopped:  {response.stop_reason}")  # end_turn = finished normally
print("=" * 60)