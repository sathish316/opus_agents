from fastmcp import Client
from pydantic_ai import Agent
from pydantic_ai.tools import Tool

from typing import AsyncGenerator
from pydantic_ai.messages import UserContent
from mcp.client.session import ClientSession
import asyncio
import os
import logging
import json
import sys

# Add path to import logging_config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from logging_config import setup_logging

# Setup log level
setup_logging(logging.INFO)

logger = logging.getLogger(__name__)

async def call_fastmcp_tool(
    session: ClientSession, mcp_tool_name: str, kwargs: dict, parse_json: bool = True
):
    result = await session.call_tool(mcp_tool_name, kwargs)
    if hasattr(result, "content"):
        if parse_json:
            if isinstance(result.content, list):
                return {"data": [json.loads(str(contentItem.text)) for contentItem in result.content]}
            else:
                return {"data": json.loads(str(result.content))}
        else:
            if isinstance(result.content, list):
                return {"data": [str(contentItem.text) for contentItem in result.content]}
            else:
                return {"data": str(result.content)}
    return {"data": str(result)}

# FastMCP client using default OAuth settings
async def connect_to_google_workspace():
    config = {
        "mcpServers": {
            "google_calendar": {
                # Local stdio server
                "transport": "stdio",
                "command": "uv",
                "args": [
                    "run",
                    "--directory",
                    f"{os.getenv('GOOGLE_WORKSPACE_MCP_PATH')}",
                    "python",
                    "main.py",
                    "--tools",
                    "calendar",
                ],
                "env": {
                    "GOOGLE_OAUTH_CLIENT_ID": os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
                    "GOOGLE_OAUTH_CLIENT_SECRET": os.getenv(
                        "GOOGLE_OAUTH_CLIENT_SECRET"
                    ),
                },
                "cwd": f"{os.getenv('GOOGLE_WORKSPACE_MCP_PATH')}",
                "tool_prefix": "google_calendar",
            }
        }
    }

    async with Client(config) as client:
        await client.ping()

        # List and print all available tools
        tools = await client.list_tools()
        logger.info("[Google Workspace] Available tools:")
        for tool in tools:
            logger.debug(f"Tool attributes: {list(tool.__dict__.keys())}")
            logger.info(f"Name - {tool.name}")
            logger.debug(f"Title - {tool.title}")
            logger.debug(f"Description - {tool.description}")
            logger.debug(f"inputSchema - {tool.inputSchema}")
            logger.debug(f"outputSchema - {tool.outputSchema}")
            logger.debug(f"annotations - {tool.annotations}")

        logger.info(f"[HERE] calling get_events")
        result = await call_fastmcp_tool(
            client, 
            "get_events", 
            {"time_min": "2025-10-04T00:00:00Z", "time_max": "2025-10-04T23:59:59Z", "user_google_email": os.getenv("GOOGLE_USER_EMAIL")},
            parse_json=False
        )
        logger.info(f"{result['data'][0]}")

async def main():
    await connect_to_google_workspace()


if __name__ == "__main__":
    asyncio.run(main())
