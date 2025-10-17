import logging
import traceback
from typing import Optional

from opus_agent_base.agent_runner import AgentInstance as BaseAgentInstance
from opus_todo_agent.custom_tools_manager import CustomToolsManager
from opus_todo_agent.higher_order_tools_manager import HigherOrderToolsManager

logger = logging.getLogger(__name__)


class AgentInstance(BaseAgentInstance):
    """Singleton class to manage agent lifecycle"""

    _instance: Optional["AgentInstance"] = None
    _initialized: bool = False

    async def initialize(self):
        """Initialize Agent"""
        if AgentInstance._initialized:
            logger.info("♻️  Agent initialized, reusing existing instance")
            return self

        await super().initialize()

        try:
            # custom tools manager
            self.custom_tools_manager = CustomToolsManager(
                self.config_manager,
                self.instructions_manager,
                self.model_manager,
                self.agent,
            )

            # higher order tools manager
            self.higher_order_tools_manager = HigherOrderToolsManager(
                self.agent,
                self.mcp_manager.fastmcp_client_context,
                self.config_manager,
                self.instructions_manager,
                self.model_manager,
            )
            await self.higher_order_tools_manager.initialize_tools()

            AgentInstance._initialized = True
            logger.info("✅ opus-todo-agent initialized successfully")
            await self.agent_manager.inspect_tools()

            return self

        except Exception as e:
            logger.error(f"❌ Failed to initialize Agent: {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise