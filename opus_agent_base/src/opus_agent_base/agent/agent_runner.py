import logging

from opus_agent_base.common.logging_config import quick_setup, console_log

from opus_agent_base.agent.agent_instance import AgentInstance
from opus_agent_base.tools.custom_tool import CustomTool
from opus_agent_base.tools.higher_order_tool import HigherOrderTool
from opus_agent_base.tools.mcp_manager import MCPManager
from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.prompt.instructions_manager import InstructionsManager

# Setup logging with ERROR level by default
logger = logging.getLogger(__name__)


class AgentRunner:
    def __init__(
        self,
        name: str,
        config_manager: ConfigManager,
        instructions_manager: InstructionsManager,
        agent_instruction_keys: list[str],
        mcp_manager: MCPManager,
        custom_tools: list[CustomTool],
        higher_order_tools: list[HigherOrderTool],
    ):
        self.name = name
        self.config_manager = config_manager
        self.instructions_manager = instructions_manager
        self.agent_instruction_keys = agent_instruction_keys
        self.mcp_manager = mcp_manager
        self.custom_tools = custom_tools
        self.higher_order_tools = higher_order_tools

        # Read log level from config and reconfigure logging
        log_level = config_manager.get_setting("debug.log_level", "ERROR")
        quick_setup(log_level=log_level)

    async def run_agent(self):
        """Run Agent CLI using PydanticAI CLI"""
        try:
            console_log("🚀 Initializing agent...")
            # Initialize Agent
            agent_instance = AgentInstance(
                name=self.name,
                config_manager=self.config_manager,
                agent_instruction_keys=self.agent_instruction_keys,
                instructions_manager=self.instructions_manager,
                mcp_manager=self.mcp_manager,
                custom_tools=self.custom_tools,
                higher_order_tools=self.higher_order_tools,
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
