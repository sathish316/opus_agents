import logging

from opus_agent_base.prompt.instructions_manager import InstructionsManager
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServer
from singleton_decorator import singleton

from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.model.model_manager import ModelManager
from opus_agent_base.tools.custom_tool import CustomTool
from opus_agent_base.tools.custom_tools_manager import CustomToolsManager
from opus_agent_base.tools.higher_order_tool import HigherOrderTool
from opus_agent_base.tools.higher_order_tools_manager import HigherOrderToolsManager
from opus_agent_base.tools.mcp_manager import MCPManager

logger = logging.getLogger(__name__)


@singleton
class AgentManager:
    """
    Manager for the agent
    """

    def __init__(
        self,
        name: str,
        config_manager: ConfigManager,
        agent_instruction_keys: list[str],
        instructions_manager: InstructionsManager,
        mcp_manager: MCPManager,
        custom_tools: list[CustomTool],
        higher_order_tools: list[HigherOrderTool],
    ):
        self.name = name
        self.config_manager = config_manager
        self.agent_instruction_keys = agent_instruction_keys
        self.instructions_manager = instructions_manager
        self.model_manager = None
        self.mcp_manager = mcp_manager
        self.custom_tools = custom_tools
        self.higher_order_tools = higher_order_tools

    async def initialize_agent(self):
        # setup agent instructions
        instructions = "\n".join(
            self.instructions_manager.get(key) for key in self.agent_instruction_keys
        )

        # model manager
        self.model_manager = ModelManager(self.config_manager)

        # agent
        self.agent = Agent(
            instructions=instructions,
            model=self.model_manager.get_model(),
            toolsets=self.mcp_manager.servers,
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
        fastmcp_client_context = await self.mcp_manager.initialize_fastmcp_client_context()
        self.higher_order_tools_manager = HigherOrderToolsManager(self.config_manager,
            self.agent,
            fastmcp_client_context
        )
        await self.higher_order_tools_manager.initialize_tools(self.higher_order_tools)
        logger.info("Agent initialized")

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
