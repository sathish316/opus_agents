import logging

from opus_todo_agent.custom_tools.meeting_transcript.loom_tools import LoomTools
from opus_todo_agent.custom_tools.meeting_transcript.zoom_tools import ZoomTools
from opus_todo_agent.custom_tools.notes.obsidian_tools import ObsidianTools
from opus_todo_agent.custom_tools.todo.todoist_tools import TodoistTools

logger = logging.getLogger(__name__)


class CustomToolsManager:
    """
    Manager for custom tools
    """

    def __init__(self, config_manager, instructions_manager, model_manager, agent):
        self.config_manager = config_manager
        self.agent = agent
        self.instructions_manager = instructions_manager
        self.model_manager = model_manager
        self.initialize_tools()

    def initialize_tools(self):
        if self._is_mcp_enabled("productivity", "todo", "todoist"):
            TodoistTools().initialize_tools(self.agent)
            logger.info("Todoist Custom tools initialized")

        if self._is_mcp_enabled("productivity", "notes", "obsidian"):
            ObsidianTools(
                self.config_manager, self.instructions_manager, self.model_manager
            ).initialize_tools(self.agent)
            logger.info("Obsidian Custom tools initialized")

        if self._is_mcp_enabled("productivity", "meeting_transcript", "loom"):
            LoomTools(self.config_manager, self.instructions_manager, self.model_manager).initialize_tools(self.agent)
            logger.info("Loom Custom tools initialized")

        if self._is_mcp_enabled("productivity", "meeting_transcript", "zoom"):
            ZoomTools(self.config_manager, self.instructions_manager, self.model_manager).initialize_tools(self.agent)
            logger.info("Zoom Custom tools initialized")

        logger.info("Custom tools initialized")

    def _is_mcp_enabled(self, domain, category, mcp):
        """
        Check if the MCP server is enabled in a given domain and category.
        Examples of domain are: general, productivity
        Examples of category are: todo, calendar etc.
        Examples of mcp are: todoist, google_calendar, slack etc.
        """
        return self.config_manager.get_setting(f"mcp_config.{domain}.{category}.{mcp}.enabled")
