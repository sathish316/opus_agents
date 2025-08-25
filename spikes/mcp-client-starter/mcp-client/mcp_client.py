import asyncio
from contextlib import AsyncExitStack
from typing import Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv()

class MCPClient:
    def __init__(self):
        # init session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_local_mcp_server(self, server_script_path: str):
        """Connect to local MCP server

        Args:
            server_script_path (str): Path to the MCP server script in .py
        """
        # assume it is always a python script
        # create mcp client with server script path and initialize it
        command = "python"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None,
        )
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # list available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to MCP server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process query using Claude and available tools"""
        # create a list of messages
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        # list available tools
        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema,
        } for tool in response.tools]
        print("\nProcessing query with tools:", [tool['name'] for tool in available_tools])
        
        # claude API call
        response = self.anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=messages,
            tools=available_tools
        )
        
        # process response
        tool_results = []
        final_text = []
        
        for content in response.content:
            if content.type == "text":
                final_text.append(content.text)
            elif content.type == "tool_use":
                tool_name = content.name
                tool_args = content.input

                # execute tool call
                result = await self.session.call_tool(tool_name, tool_args)
                tool_results.append({"call": tool_name, "result": result})
                final_text.append(f"Calling {tool_name} with args: {tool_args}")

                # add tool_use message to messages
                if hasattr(content, 'text') and content.text:
                    messages.append({
                        "role": "assistant",
                        "content": content.text
                    })

                messages.append({
                    "role": "user",
                    "content": result.content
                })

                # get next response from Claude
                response = self.anthropic.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1000,
                    messages=messages
                )

                final_text.append(response.content[0].text)
            
        return "\n".join(final_text)
        
    async def chat_loop(self):
        """Run a chat loop"""
        print("\nMCP client started")
        print("\nType your queries or type 'exit' to exit")
        while True:
            try:
                query = input("\n> ").strip()

                if query.lower() == 'exit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {e}")

    async def cleanup(self):
        """cleanup resources"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python mcp_client.py <server_script>")
        sys.exit(1)
    
    client = MCPClient()
    try:
        await client.connect_to_local_mcp_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    import sys
    asyncio.run(main())
