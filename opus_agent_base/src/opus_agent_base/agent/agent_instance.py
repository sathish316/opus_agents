import logging
import traceback
from typing import Optional

from singleton_decorator import singleton

from opus_agent_base.agent.agent_manager import AgentManager
from opus_agent_base.agent.agent_dependencies import AgentDependencies

logger = logging.getLogger(__name__)

class AgentInstance:
    """Singleton class to manage agent lifecycle"""

    _instance: Optional["AgentInstance"] = None
    _initialized: bool = False

    def __new__(
        cls,
        name: str,
        agent_deps: AgentDependencies,
    ):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        name: str,
        agent_deps: AgentDependencies,
    ):
        """Initialize is called every time, but we only set up once."""
        # Don't reinitialize if already done
        if AgentInstance._initialized:
            return
        self.agent_manager = AgentManager(
            name,
            agent_deps,
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
