from fastmcp import Client
from pydantic_ai import Agent
from pydantic_ai.tools import Tool

from typing import AsyncGenerator
from pydantic_ai.messages import UserContent
from mcp.client.session import ClientSession
import asyncio

# Instantiate the PydanticAI tool wrapper
def wrap_tool(name: str, description: str, inputSchema: dict, session: ClientSession, mcp_tool_name: str) -> Tool:
    async def mcp_tool_function(**kwargs):
        """Dynamically created tool function for MCP tool"""
        result = await session.call_tool(mcp_tool_name, kwargs)
        print(f"[HERE] Result of calling {mcp_tool_name}: {result}")
        # Handle the result properly - it might be a ToolResult or other type
        if hasattr(result, 'content'):
            return {"data": result.content}
        elif hasattr(result, 'data'):
            return {"data": result.data}
        return {"data": str(result)}
    
    return Tool.from_schema(
        name=name,
        description=description,
        json_schema=inputSchema,
        function=mcp_tool_function
    )

# FastMCP client using default OAuth settings
async def connect_and_call_clockwise():
    async with Client("https://mcp.getclockwise.com/mcp", auth="oauth") as client:
        await client.ping()

        # List and print all available tools
        tools = await client.list_tools()
        # print("Available tools:")
        # for tool in tools:
        #     print(f"Tool attributes: {list(tool.__dict__.keys())}")
        #     print(f"Name - {tool.name}")
        #     print(f"Title - {tool.title}")
        #     print(f"Description - {tool.description}")
        #     print(f"inputSchema - {tool.inputSchema}")
        #     print(f"outputSchema - {tool.outputSchema}")
        #     print(f"annotations - {tool.annotations}")

        # Wrap each capability as a PydanticAI tool
        agent_tools = []
        for tool in tools:
            wrapped_tool = wrap_tool(
                name=tool.name,
                description=tool.description,
                inputSchema=tool.inputSchema,
                session=client, 
                mcp_tool_name=tool.name
            )
            agent_tools.append(wrapped_tool)

        print(f"[HERE] creating Agent")
        agent = Agent(
            model="openai:gpt-5",
            tools=agent_tools,
        )
        print(f"[HERE] invoking Agent")
        result = await agent.run("What events do i have on 29-Sep-2025? List only the title and start time and duration of each event in a table format.")
        print(f"[HERE] Agent response:")
        print(result.output)

async def main():
    await connect_and_call_clockwise()

if __name__ == "__main__":
    asyncio.run(main())
