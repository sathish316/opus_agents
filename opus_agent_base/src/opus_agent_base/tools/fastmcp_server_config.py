class FastMCPServerConfig:
    """
    Configuration for an FastMCP server
    """

    def __init__(self, name: str, config_key: str, mcp_server_config):
        """
        Args:
            name: The name of the FastMCP server
            config_key: The config key of the FastMCP server
            mcp_server_config: The MCP server configuration
        """
        self.name = name
        self.config_key = config_key
        self.mcp_server_config = mcp_server_config