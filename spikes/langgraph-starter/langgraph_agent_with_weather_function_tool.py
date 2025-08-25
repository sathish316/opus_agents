from langgraph.prebuilt import create_react_agent

def get_weather(city: str) -> str:
    """Get weather for a given city"""
    return f"It's always sunny in {city}"

agent = create_react_agent(
    model = "anthropic:claude-3-7-sonnet-latest",
    tools = [get_weather],
    prompt = "You are a helpful assistant"
)

# run the agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in Bangalore?"}]}
)

import json
print(json.dumps(response, indent=2, default=str))

print(response)