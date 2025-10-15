import logging
import random
from typing import List

from opus_todo_agent.models.todo.todoist_models import CompletedTask, Task

logger = logging.getLogger(__name__)


class TodoistHelper:
    """Todoist helper"""

    def get_unique_project_ids(self, completed_tasks: List[CompletedTask]) -> List[str]:
        """Extract unique project IDs from completed tasks"""
        project_ids = [task.project_id for task in completed_tasks]
        logger.debug(f"Project IDs: {project_ids}")
        return project_ids

    def pick_random_tasks(self, tasks: List[Task], count: int) -> List[Task]:
        """
        Select random tasks from a list of tasks.

        Args:
            tasks: List of tasks to choose from
            count: Number of tasks to select

        Returns:
            List of randomly selected tasks
        """
        if not tasks:
            return []

        if count >= len(tasks):
            return tasks

        return random.sample(tasks, count)

    def get_unique_project_ids_from_tasks(self, tasks: List[Task]) -> List[str]:
        """Extract unique project IDs from tasks"""
        project_ids = [task.project_id for task in tasks]
        logger.debug(f"Project IDs: {project_ids}")
        return project_ids
