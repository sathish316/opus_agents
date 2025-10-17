import logging

from opus_agent_base.managers.custom_tools_manager import BaseCustomToolsManager
from opus_todo_agent.custom_tools.meeting_transcript.loom_tools import LoomTools
from opus_todo_agent.custom_tools.meeting_transcript.zoom_tools import ZoomTools
from opus_todo_agent.custom_tools.notes.obsidian_tools import ObsidianTools
from opus_todo_agent.custom_tools.todo.todoist_tools import TodoistTools

logger = logging.getLogger(__name__)


class CustomToolsManager(BaseCustomToolsManager):
    """
    Domain-specific manager for custom tools in opus_todo_agent.
    
    Extends BaseCustomToolsManager to register productivity-specific tools.
    """

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
