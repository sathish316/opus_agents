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
        self.mcp_manager = builder.mcp_manager
        self.custom_tools = builder.custom_tools
        self.higher_order_tools = builder.higher_order_tools

    async def initialize_agent(self):
        # System prompt
        agent_system_prompt = "\n".join(
            self.instructions_manager.get(key)
            for key in self.system_prompt_keys
        )

        # initialize agent tools
        self.tools = []
        enabled_tools = {}
        fastmcp_client_context = (
            await self.mcp_manager.initialize_fastmcp_client_context()
        )

        async def tools_initializer(session: ClientSession):
            logger.info("Initializing agent tools")
            logger.debug(
                f"Allowed tool prefixes for allowed tools: {self.config_manager.get_setting('mcp_config.allowed_tool_prefixes', [])}"
            )
            # logger.info(f"Allowed docker tools: {self.config_manager.get_setting('mcp_config.allowed_tools.docker', [])}")
            # logger.info(f"Allowed k8s tools: {self.config_manager.get_setting('mcp_config.allowed_tools.k8s', [])}")
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
                        self.tools.append(self.wrap_tool(tool, fastmcp_client_context))
                        self._log_enabled_tools(enabled_tools, tool_prefix, tool.name)
                else:
                    self.tools.append(self.wrap_tool(tool, fastmcp_client_context))
                    self._log_enabled_tools(enabled_tools, tool_prefix, tool.name)

        if fastmcp_client_context is not None:
            await fastmcp_client_context(tools_initializer)
            console_log(f"Enabled tools: {enabled_tools}")

        # agent
        self.agent = Agent(
            system_prompt=agent_system_prompt,
            model=self.model_manager.get_model(),
            toolsets=self.mcp_manager.servers,
            tools=self.tools,
        )

        # add custom tools to Agent
        self.custom_tools_manager = CustomToolsManager(
            self.config_manager,
            self.instructions_manager,
            self.model_manager,
            self.agent,
        )
        self.custom_tools_manager.initialize_tools(self.custom_tools)

        # add higher order tools to Agent
        self.higher_order_tools_manager = HigherOrderToolsManager(
            self.config_manager, self.agent, fastmcp_client_context
        )
        await self.higher_order_tools_manager.initialize_tools(self.higher_order_tools)
        logger.info("Agent initialized")

    def get_agent(self):
        return self.agent

    def wrap_tool(self, tool: MCPTool, fastmcp_client_context) -> Tool:
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

    async def inspect_tools(self):
        agent_inspect_tools_enabled = self.config_manager.get_setting(
            "debug.inspect_tools", False
        )
        if agent_inspect_tools_enabled:
            await self._inspect_mcp_tools()
            await self._inspect_function_tools()

    async def _inspect_mcp_tools(self):
        for toolset in self.agent.toolsets:
            if isinstance(toolset, MCPServer):
                tools = await toolset.list_tools()
                for tool in tools:
                    toolset_id = getattr(toolset, "id", None)
                    toolset_command = getattr(toolset, "command", None)
                    logger.info(
                        f"AgentMCPTool: {toolset_id or toolset_command}-{tool.name}"
                    )

    async def _inspect_function_tools(self):
        function_toolset = getattr(self.agent, "_function_toolset", None)
        if function_toolset:
            for function_tool_key, _ in function_toolset.tools.items():
                logger.info(f"AgentFunctionTool: {function_tool_key}")

    def _log_enabled_tools(self, enabled_tools, tool_prefix, tool_name):
        if tool_prefix not in enabled_tools:
            enabled_tools[tool_prefix] = set()
        enabled_tools[tool_prefix].add(tool_name)
