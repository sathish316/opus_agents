import logging

from opus_agent_base.common.logging_config import quick_setup

from opus_agent_base.agent.agent_instance import AgentInstance
from opus_agent_base.tools.custom_tool import CustomTool
from opus_agent_base.tools.higher_order_tool import HigherOrderTool
from opus_agent_base.tools.mcp_manager import MCPManager
from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.prompt.instructions_manager import InstructionsManager

# Setup logging
log_file_path = quick_setup()
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

    async def run_agent(self):
        """Run Agent CLI using PydanticAI CLI"""
        try:
            # Initialize singleton Agent
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
