class MCPServerConfig:
    """
    Configuration for an MCP server
    """

    def __init__(self, name: str, config_key: str, type: str, mcp_server):
        """
        Args:
            name: The name of the MCP server
            config_key: The config key of the MCP server
            type: The type of the MCP server - allowed values are "stdio", "streamable-http"
            mcp_server: The MCP server instance
        """
        self.name = name
        self.config_key = config_key
        self.type = type
        self.mcp_server = mcp_server