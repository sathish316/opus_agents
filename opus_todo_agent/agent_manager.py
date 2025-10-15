import logging

from pydantic_ai import Agent
from singleton_decorator import singleton
from pydantic_ai.mcp import MCPServer

logger = logging.getLogger(__name__)

@singleton
class AgentManager:
    """
    Manager for the agent
    """

    def __init__(self, model_manager, instructions_manager, mcp_manager, config_manager):
        self.model_manager = model_manager
        self.instructions_manager = instructions_manager
        self.mcp_manager = mcp_manager
        self.config_manager = config_manager
        self.initialize()

    def initialize(self):
        self.initialize_agent()

    def initialize_agent(self):
        # agent definition
        self.agent = Agent(
            instructions=self.instructions_manager.get_all_instructions(),
            model=self.model_manager.get_model(),
            toolsets=self.mcp_manager.servers,
        )
        logger.info("Agent initialized")

    async def async_init(self):
        await self.mcp_manager.initialize_higher_order_mcp_servers()
        return self

    def get_agent(self):
        return self.agent

    async def inspect_tools(self):
        agent_inspect_tools_enabled = self.config_manager.get_setting("debug.inspect_tools", False)
        if agent_inspect_tools_enabled:
            await self._inspect_mcp_tools()
            await self._inspect_function_tools()

    async def _inspect_mcp_tools(self):
        for toolset in self.agent.toolsets:
            if isinstance(toolset, MCPServer):
                tools = await toolset.list_tools()
                for tool in tools:
                    toolset_id = getattr(toolset, 'id', None)
                    toolset_command = getattr(toolset, 'command', None)
                    logger.info(f"AgentMCPTool: {toolset_id or toolset_command}-{tool.name}")

    async def _inspect_function_tools(self):
        function_toolset = getattr(self.agent, '_function_toolset', None)
        if function_toolset:
            for (function_tool_key, _) in function_toolset.tools.items():
                logger.info(f"AgentFunctionTool: {function_tool_key}")
