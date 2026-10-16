import asyncio
import sys
import json
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from mcp import types, ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import AnyUrl
from typing import Any
load_dotenv()
claude = AsyncAnthropic()
model = "claude-haiku-5-5"


class MCPClient:
    def __init__(self, session_context):
        self._session = session_context

    def session(self):
        return self._session

    # list tools function
    async def list_tools(self) -> list[types.Tool]:
        result = await self.session().list_tools()
        return result.tools

    # call a tool function
    async def call_tool(self, tool_name: str, tool_input: dict) -> types.CallToolResult | None:
        return await self.session().call_tool(tool_name, tool_input)

    # read resource function
    async def read_resource(self, uri: str) -> str:
        result = await self.session().read_resource(AnyUrl(uri))
        resource = result.contents[0]
        return resource.text

    # implementing list prompts
    async def list_prompts(self) -> list[types.Prompt]:
        result = await self.session().list_prompts()
        return result.prompts

    # getting individual prompts
    async def get_prompt(self, prompt_name, args: dict[str, str]):
        result = await self.session().get_prompt(prompt_name, args)
        return result.messages

# connect to MCP server
async def main():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["example_server_mcp.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            client = MCPClient(session)

            # get available tools
            tools = await client.list_tools()

            claude_tools = []
            for tool in tools:
                claude_tools.append({
                    "name": tool.name,
                    "description": tool.description or "",
                    "input_schema": tool.inputSchema
                })

            # ask questions
            while True:
                question = input("\nAsk a question (or 'exit'): ").strip()

                if question.lower() == "exit":
                    break
                if not question:
                    continue

                # read document resource
                document = await client.read_resource("docs://documents/report.pdf")

                # build user message
                user_message = f"<document>\n{document}\n</document>\n\n<question>{question}</question>"

                messages = [{"role": "user", "content": user_message}]

                # send question to Claude (max 10 API calls)
                for attempt in range(10):
                    response = await claude.messages.create(
                        model=model,
                        max_tokens=1024,
                        tools=claude_tools,
                        messages=messages
                    )

                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })

                    # final answer
                    if response.stop_reason != "tool_use":
                        for block in response.content:
                            if block.type == "text":
                                print("\nClaude:", block.text)
                        break

                    # execute tools
                    tool_results = []

                    for block in response.content:
                        if block.type == "tool_use":
                            print("Using tool:", block.name)

                            result = await client.call_tool(
                                block.name,
                                block.input
                            )

                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result.content,
                                "is_error": result.isError
                            })

                    messages.append({
                        "role": "user",
                        "content": tool_results
                    })

if __name__ == "__main__":
    asyncio.run(main())
