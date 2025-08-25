### Setup

$ uv add "mcp[cli]" httpx fastMCP
or
$ uv sync

$ source .venv/bin/activate

### Steps to start MCP server

$ uv run hello_world_server.py

### Steps to start MCP client to connect to server

$ uv run hello_world_client.py

### Steps to run Local MCP servers from other hosts like Cursor

Add the following to mcp.json to connect Math and Weather Local MCP servers:

"math": {
  "command": "uv",
  "args": [
	"--directory",
	"/path_to_spikes/",
	"run",
	"math_mcp_server.py"
  ]
},
"weather": {
  "command": "uv",
  "args": [
	"--directory",
	"/path_to_spikes/",
	"run",
	"weather_mcp_server.py"
  ]
}

Ask in prompt:
1. What is the product of 200 and 300?
2. What is the weather in Philadelphia?