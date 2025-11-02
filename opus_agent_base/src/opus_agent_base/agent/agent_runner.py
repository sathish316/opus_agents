import logging

from opus_agent_base.common.logging_config import quick_setup, console_log
from opus_agent_base.agent.agent_dependencies import AgentDependencies

from opus_agent_base.agent.agent_instance import AgentInstance

logger = logging.getLogger(__name__)


class AgentRunner:
    def __init__(
        self,
        name: str,
        agent_deps: AgentDependencies,
    ):
        self.name = name
        self.agent_deps = agent_deps

        # Read log level from config and reconfigure logging
        log_level = self.agent_deps.config_manager.get_setting("debug.log_level", "ERROR")
        quick_setup(log_level=log_level)

    async def run_agent(self):
        """Run Agent CLI using PydanticAI CLI"""
        try:
            console_log("🚀 Initializing agent...")
            # Initialize Agent
            agent_instance = AgentInstance(
                name=self.name,
                agent_deps=self.agent_deps,
            )
            agent = await agent_instance.get_agent()
            console_log("✅ Agent ready")
            await agent.to_cli()

        except ExceptionGroup as eg:
            console_log("❌ Error: ExceptionGroup caught")
            logger.error("ExceptionGroup caught in TaskGroup:")
            # Print each inner exception with its traceback
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
