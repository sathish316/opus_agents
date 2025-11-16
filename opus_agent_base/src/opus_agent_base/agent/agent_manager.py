import json
import logging

from fastmcp.client.client import ClientSession
from mcp.types import Tool as MCPTool
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServer
from pydantic_ai.tools import Tool
from singleton_decorator import singleton

from opus_agent_base.agent.agent_builder import AgentBuilder
from opus_agent_base.common.logging_config import console_log
from opus_agent_base.tools.custom_tools_manager import CustomToolsManager
from opus_agent_base.tools.mcp_manager import MCPManager
from opus_agent_base.tools.higher_order_tools_manager import HigherOrderToolsManager

logger = logging.getLogger(__name__)


@singleton
class AgentManager:
    """
    Manager for the agent
    """

    def __init__(self, name: str, builder: AgentBuilder):
        self.name = name
        self.config_manager = builder.config_manager
        self.system_prompt_keys = builder.system_prompt_keys
        self.instructions_manager = builder.instructions_manager
        self.model_manager = builder.model_manager
        self.custom_tools = builder.custom_tools
        self.higher_order_tools = builder.higher_order_tools
        self.mcp_servers_config = builder.mcp_servers_config

    async def initialize_agent(self):
        # System prompt
        logger.info("Initializing Agent")
        agent_system_prompt = "\n".join(
            self.instructions_manager.get(key)
            for key in self.system_prompt_keys
        )

        # Initialize MCP servers
        await self.initialize_mcp_servers()

        # Initialize Agent tools
        await self.initialize_agent_tools()

        # Initialize Agent
        self.agent = Agent(
            system_prompt=agent_system_prompt,
            model=self.model_manager.get_model(),
            tools=self.agent_tools,
        )

        # Add custom tools to Agent
        self.custom_tools_manager = CustomToolsManager(
            self.config_manager,
            self.instructions_manager,
            self.model_manager,
            self.agent,
        )
        self.custom_tools_manager.initialize_tools(self.custom_tools)

        # Add higher order tools to Agent
        self.higher_order_tools_manager = HigherOrderToolsManager(
            self.config_manager, self.agent, self.fastmcp_client_context
        )
        await self.higher_order_tools_manager.initialize_tools(self.higher_order_tools)
        logger.info("Agent initialized")

    async def initialize_mcp_servers(self):
        # Initialize MCP manager and MCP servers
        logger.info("Initializing MCP servers")
        self.mcp_manager = MCPManager(self.config_manager)
        self.mcp_manager.add_mcp_servers(self.mcp_servers_config)
        logger.info("MCP servers initialized")

    async def initialize_agent_tools(self):
        # Initialize Agent tools
        self.agent_tools = []
        self.fastmcp_client_context = await self.mcp_manager.initialize_fastmcp_client_context()
        await self.mcp_manager.inspect_fastmcp_client_tools()

        async def tools_initializer(session: ClientSession):
            enabled_tools = {}
            logger.info("Initializing agent tools")
            client_tools = await session.list_tools()
            for tool in client_tools:
                tool_prefix = tool.name.split("_")[0]
                if tool_prefix in self.config_manager.get_setting(
                    "mcp_config.allowed_tool_prefixes", []
                ):
                    if tool.name in self.config_manager.get_setting(
                        "mcp_config.allowed_tools"
                    ).get(tool_prefix, []):
                        logger.debug(f"Wrapping FastMCP tool: {tool.name}")
                        self.agent_tools.append(self._wrap_tool(tool, self.fastmcp_client_context))
                        self._log_enabled_tools(enabled_tools, tool_prefix, tool.name)
                else:
                    self._log_enabled_tools(enabled_tools, tool_prefix, tool.name)
                    self.agent_tools.append(self._wrap_tool(tool, self.fastmcp_client_context))
            return enabled_tools

        if self.fastmcp_client_context is not None:
            result = await self.fastmcp_client_context(tools_initializer)
            console_log(f"Enabled tools: {result}")

    def get_agent(self):
        return self.agent

    def _wrap_tool(self, tool: MCPTool, fastmcp_client_context) -> Tool:
        async def mcp_tool_function(**kwargs):
            """Dynamically created tool function for MCP tool"""

            async def execute_tool(client: ClientSession):
                result = await client.call_tool(tool.name, kwargs)
                return result

            result = await fastmcp_client_context(execute_tool)
            return result

        return Tool.from_schema(
            name=tool.name,
            description=tool.description,
            json_schema=tool.inputSchema,
            function=mcp_tool_function,
        )

    def _log_enabled_tools(self, enabled_tools, tool_prefix, tool_name):
        if tool_prefix not in enabled_tools:
            enabled_tools[tool_prefix] = set()
        enabled_tools[tool_prefix].add(tool_name)
