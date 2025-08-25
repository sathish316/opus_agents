from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
import os
import getpass
import asyncio

# init openai model
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAIA_API_KEY"] = getpass.getpass("Enter OpenAI API key:")

model = init_chat_model("gpt-4o-mini", model_provider = "openai")

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

async def run_agent_workflow(query):
    client = MultiServerMCPClient(multi_server_params)
    tools = await client.get_tools()
    # list tools
    print(f"\nLoaded tools: {[tool.name for tool in tools]}")

    # bind tools to model
    model_with_tools = model.bind_tools(tools)

    # create tool node
    tool_node = ToolNode(tools)

    def should_continue(state: MessagesState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END
    
    # Define call_model function
    async def call_model(state: MessagesState):
        messages = state["messages"]
        response = await model_with_tools.ainvoke(messages)
        return {"messages": [response]}
    
    # create graph
    builder = StateGraph(MessagesState)
    builder.add_node("call_model", call_model)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges("call_model", should_continue)
    builder.add_edge("tools", "call_model")

    # compile graph
    graph = builder.compile()
    
    # execute the graph
    response = await graph.ainvoke({
        "messages": [("user", query)]
    })
    return response["messages"][-1].content
        
        
if __name__ == "__main__":
   # Run the asynchronous run_agent function and wait for the result
   print("Starting MCP Client...")
   result = asyncio.run(run_agent_workflow("What is the product of 5 and 10?"))
   print(result)

   result = asyncio.run(run_agent_workflow("What is the weather in Philadelphia?"))
   print(result)
   