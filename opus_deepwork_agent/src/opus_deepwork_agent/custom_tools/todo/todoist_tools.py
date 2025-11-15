import logging
from typing import List, Optional

from opus_agent_base.common.logging_config import console_log
from opus_agent_base.tools.custom_tool import CustomTool
from opus_deepwork_agent.custom_tools.todo.todoist_client import TodoistClient
from opus_deepwork_agent.models.todoist_models import Task
from pydantic_ai import RunContext

logger = logging.getLogger(__name__)


class TodoistTools(CustomTool):
    """
    Todoist tools
    """

    def __init__(
        self, config_manager=None, instructions_manager=None, model_manager=None
    ):
        # Initialize base class with tool name and config key
        super().__init__(
            "todoist_deepwork",  # Tool name
            "deepwork.todo.todoist",  # Config key path
            config_manager,
            instructions_manager,
            model_manager,
        )
        self.todoist_client = TodoistClient()

    def initialize_tools(self, agent):
        @agent.tool
        def get_deep_work_tasks(
            ctx: RunContext[str],
            tag_name: str = "deepwork",
            project_name: Optional[str] = None,
        ) -> List[Task]:
            """
            Get tasks tagged for DeepWork from Todoist.
            If the user asks to schedule a deepwork slot on the calendar, use the tool `schedule_deepwork_slot_in_calendar`

            Args:
                tag_name: Queries Todoist for tasks with specific tag (defaults to 'deepwork').
                project_name: Optional project name to filter. If not provided, searches all projects.

            Returns:
                List of `Task` objects
                Each task includes: id, content, project_name, and a clickable URL.
            """
            logger.info(f"[CustomToolCall] Fetching DeepWork tasks with Tag:{tag_name}, Project:{project_name}")
            console_log(f"[CustomToolCall] Fetching DeepWork tasks with Tag:{tag_name}, Project:{project_name}")

            try:
                # Fetch tasks with the specified tag
                tasks = self.todoist_client.get_tasks_with_tag(
                    tag_name=tag_name, project_name=project_name
                )
                logger.info(f"Found {len(tasks)} task(s)")
                return tasks

            except Exception as e:
                import traceback

                logger.error(f"Error fetching tasks: {e}")
                logger.error(traceback.format_exc())
                return []
