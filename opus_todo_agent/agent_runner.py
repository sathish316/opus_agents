import logging
import traceback
from typing import Optional

from agent_manager import AgentManager
from custom_tools_manager import CustomToolsManager
from higher_order_tools_manager import HigherOrderToolsManager
from instructions_manager import InstructionsManager
from logging_config import quick_setup
from mcp_manager import MCPManager
from model_manager import ModelManager

from opus_todo_agent.common.config_manager import ConfigManager

# Setup logging first thing
log_file_path = quick_setup()
logger = logging.getLogger(__name__)


class AgentInstance:
    """Singleton class to manage agent lifecycle"""

    _instance: Optional["AgentInstance"] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize is called every time, but we only set up once."""
        # Don't reinitialize if already done
        if AgentInstance._initialized:
            return

    async def initialize(self):
        """Initialize Agent"""
        if AgentInstance._initialized:
            logger.info("♻️  Agent initialized, reusing existing instance")
            return self

        logger.info("🚀 Initializing Agent...")

        try:
            # config manager
            self.config_manager = ConfigManager()

            # model manager
            self.model_manager = ModelManager(self.config_manager)

            # instructions manager
            self.instructions_manager = InstructionsManager()

            # MCP manager
            self.mcp_manager = MCPManager(self.config_manager)

            # agent manager
            self.agent_manager = AgentManager(
                self.model_manager,
                self.instructions_manager,
                self.mcp_manager,
                self.config_manager,
            )
            self.agent_manager = await self.agent_manager.async_init()
            self.agent = self.agent_manager.get_agent()

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


async def run_agent():
    """Run Pydantic AI agent CLI"""
    try:
        # Initialize singleton Agent
        agent_instance = AgentInstance()
        agent = await agent_instance.get_agent()

        # Run Agent CLI
        await agent.to_cli()

    except ExceptionGroup as eg:
        logger.error("ExceptionGroup caught in TaskGroup:")
        # Print each inner exception with its traceback
        for e in eg.exceptions:
            import traceback

            traceback.print_exception(e)
        raise
    except KeyboardInterrupt:
        logger.info("🛑 Agent interrupted by user")
    finally:
        logger.info("🏁 Agent session ended")
