from dataclasses import dataclass

@dataclass
class FastMCPServerConfig:
    """
    Configuration for a FastMCP server
    """
    name: str
    config_key: str
    mcp_server_config: dict
