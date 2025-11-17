import logging

from opus_agent_base.tools.meta_tool import MetaTool
from opus_agent_base.common.logging_config import console_log

logger = logging.getLogger(__name__)


class MetaToolsManager:
    """
    Manager for meta tools that dynamically create tools from specifications
    """

    def __init__(
        self,
        config_manager,
        agent,
    ):
        self.config_manager = config_manager
        self.agent = agent
        self.agent_tools = []

    async def initialize_tools(self, meta_tools: list[MetaTool]):
        """
        Initialize all meta tools.

        Args:
            meta_tools: List of MetaTool instances to initialize
        """
        enabled = []
        for tool in meta_tools:
            try:
                agent_tool = await tool.initialize_tools(self.agent)
                self.agent_tools.append(agent_tool)
                logger.info(f"{tool.name} Meta tool initialized")
                enabled.append(tool.name)
            except Exception as e:
                logger.error(f"Failed to initialize meta tool {tool.name}: {e}")
                import traceback
                logger.error(traceback.format_exc())

        console_log(f"Enabled meta tool(s) for - {enabled}")
        logger.info("All Meta tools initialized")

    async def cleanup(self, meta_tools: list[MetaTool]):
        """
        Clean up resources for all meta tools.

        Args:
            meta_tools: List of MetaTool instances to clean up
        """
        for tool in meta_tools:
            try:
                if hasattr(tool, 'cleanup'):
                    await tool.cleanup()
                    logger.info(f"Cleaned up meta tool: {tool.name}")
            except Exception as e:
                logger.error(f"Error cleaning up meta tool {tool.name}: {e}")
