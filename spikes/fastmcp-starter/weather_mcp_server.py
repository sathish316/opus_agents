from fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool
async def get_weather(location: str) -> str:
    """Get weather for a given location"""
    return "It's always sunny in {location}"

if __name__ == "__main__":
    mcp.run()