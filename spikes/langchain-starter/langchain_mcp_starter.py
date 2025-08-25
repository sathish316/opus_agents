from mcp import ClientSession, StdioServerParameters
from langchain_mcp_adapters.client import MultiServerMCPClient
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import asyncio
import getpass
import os
from langchain.chat_models import init_chat_model

# init openai model
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAIA_API_KEY"] = getpass.getpass("Enter OpenAI API key:")

model = init_chat_model("gpt-4o-mini", model_provider = "openai")

# init MCP server
server_params = StdioServerParameters(
    command = "python",
    args=["/Users/skumar32/code/atlassian/aiops/agentic-rca-engine/spikes/fastmcp-starter/math_mcp_server.py"]
)

# init multiple MCP servers
multi_server_params = {
        "math": {
            "command": "python",
            "args": ["/Users/skumar32/code/atlassian/aiops/agentic-rca-engine/spikes/fastmcp-starter/math_mcp_server.py"],
            "transport": "stdio"
        },
        "weather": {
            "command": "python",
            "args": ["/Users/skumar32/code/atlassian/aiops/agentic-rca-engine/spikes/fastmcp-starter/weather_mcp_server.py"],
            "transport": "stdio"
        }
    }

async def run_agent(query):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # load tools
            tools = await load_mcp_tools(session)
            print(f"\nLoaded tools: {[tool.name for tool in tools]}")
            # create agent
            agent = create_react_agent(model, tools)
            # invoke agent
            response = await agent.ainvoke({
                "messages": [("user", query)]
            })
            return response["messages"][-1].content
        

async def run_multi_agent(query):
    client = MultiServerMCPClient(multi_server_params)
    tools = await client.get_tools()
    # list tools
    print(f"\nLoaded tools: {[tool.name for tool in tools]}")
    # create agent
    agent = create_react_agent(model, tools)
    # invoke agent
    response = await agent.ainvoke({
        "messages": [("user", query)]
    })
    return response["messages"][-1].content
        
        
if __name__ == "__main__":
   # Run the asynchronous run_agent function and wait for the result
   print("Starting MCP Client...")
   result = asyncio.run(run_agent("What is the product of 5 and 10?"))
   print(result)

   result = asyncio.run(run_multi_agent("What is the product of 5 and 10?"))
   print(result)
   
   result = asyncio.run(run_multi_agent("What is the weather in Philadelphia?"))
   print(result)
