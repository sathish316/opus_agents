import logging
import traceback
from typing import Optional

from singleton_decorator import singleton

from opus_agent_base.agent.agent_manager import AgentManager
from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.prompt.instructions_manager import InstructionsManager
from opus_agent_base.tools.custom_tool import CustomTool
from opus_agent_base.tools.higher_order_tool import HigherOrderTool
from opus_agent_base.tools.mcp_manager import MCPManager

logger = logging.getLogger(__name__)

class AgentInstance:
    """Singleton class to manage agent lifecycle"""

    _instance: Optional["AgentInstance"] = None
    _initialized: bool = False

    def __new__(
        cls,
        name: str,
        config_manager: ConfigManager,
        agent_instruction_keys: list[str],
        instructions_manager: InstructionsManager,
        mcp_manager: MCPManager,
        custom_tools: list[CustomTool],
        higher_order_tools: list[HigherOrderTool],
    ):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

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
        """Initialize is called every time, but we only set up once."""
        # Don't reinitialize if already done
        if AgentInstance._initialized:
            return
        self.agent_manager = AgentManager(
            name,
            config_manager,
            agent_instruction_keys,
            instructions_manager,
            mcp_manager,
            custom_tools,
            higher_order_tools,
        )

    async def initialize(self):
        """Initialize Agent"""
        if AgentInstance._initialized:
            logger.info("♻️  Agent initialized, reusing existing instance")
            return self

        logger.info("🚀 Initializing Agent...")

        try:
            # initialize agent
            await self.agent_manager.initialize_agent()
            self.agent = self.agent_manager.get_agent()

            AgentInstance._initialized = True
            logger.info("✅ Agent initialized successfully")
            await self.agent_manager.inspect_tools()

            return self

        except Exception as e:
            logger.error(f"❌ Failed to initialize Agent: {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise

    async def get_agent(self):
        """Get the initialized agent instance."""
        if not AgentInstance._initialized:
            await self.initialize()
        return self.agent
