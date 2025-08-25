### Setup

$ uv sync
$ source .venv/bin/activate

### Steps to run MCP server and connect from Cursor

$ uv run weather.py

Add the following to mcp.json

"weather": {
  "command": "uv",
  "args": [
	"--directory",
	"/path/to/server",
	"run",
	"weather.py"
  ]
}

### Steps to connect to MCP server from client

$ python run mcp_client.py /path/to/weather.py
