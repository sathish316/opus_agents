import logging

from opus_agent_base.agent.agent_builder import AgentBuilder
from opus_agent_base.agent.agent_instance import AgentInstance
from opus_agent_base.common.logging_config import console_log, quick_setup

logger = logging.getLogger(__name__)


class AgentRunner:
    def __init__(
        self,
        agent_builder: AgentBuilder,
    ):
        self.agent_builder = agent_builder
        log_level = self.agent_builder.config_manager.get_setting("debug.log_level", "ERROR")
        quick_setup(log_level=log_level)

    async def run_agent(self):
        """Run Agent CLI using PydanticAI CLI"""
        try:
            console_log("🚀 Starting Agent...")
            # Initialize Agent
            agent_instance = AgentInstance(self.agent_builder)
            agent = await agent_instance.get_agent()
            console_log("✅ Agent started")
            await agent.to_cli()

        except ExceptionGroup as eg:
            console_log("❌ Exception running agent")
            logger.error("Exception running agent:")
            for e in eg.exceptions:
                import traceback
                traceback.print_exception(e)
            raise
        except KeyboardInterrupt:
            console_log("\n🛑 Agent interrupted")
            logger.debug("Agent interrupted by user")
        finally:
            console_log("🏁 Agent session ended")
            logger.debug("Agent session ended")
