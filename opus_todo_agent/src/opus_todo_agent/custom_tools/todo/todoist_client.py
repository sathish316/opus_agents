import logging
import os
from typing import Dict, List, Optional, Tuple

import requests

from opus_todo_agent.models.todo.todoist_models import CompletedTask, Task

logger = logging.getLogger(__name__)


class TodoistAPIError(Exception):
    """Custom exception for Todoist API errors"""

    pass


class TodoistClient:
    """Todoist client"""

    def __init__(self):
        self.api_key = self._get_api_key()

    def _get_api_key(self) -> str:
        """Get Todoist API key from environment variable"""
        api_key = os.getenv("TODOIST_API_KEY")
        if not api_key:
            raise ValueError("TODOIST_API_KEY environment variable not set")
        return api_key

    def _make_request(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> requests.Response:
        """Make HTTP request with error handling"""
        if headers is None:
            headers = {}

        headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise ValueError(f"HTTP request failed: {e}")

    def get_completed_tasks_for_date_range(
        self, from_date: str, to_date: str
    ) -> List[CompletedTask]:
        """Get completed tasks for a specific date range"""
        url = "https://api.todoist.com/sync/v9/completed/get_all"
        params = {"since": from_date, "until": to_date}

        response = self._make_request(url, params=params)
        data = response.json()

        items = data.get("items", [])
        if not items:
            return []

        completed_tasks = []
        for item in items:
            task = CompletedTask(
                content=item.get("content", ""),
                id=item.get("task_id", ""),
                project_id=item.get("v2_project_id", ""),
                completed_date=item.get("completed_at", ""),
            )
            completed_tasks.append(task)

        return completed_tasks

    def get_project_names_for_ids(self, project_ids: List[str]) -> Dict[str, str]:
        """
        Get project names for project IDs using the v1 API.
        Note: This function appears to have an issue in the original Go code
        as it tries to parse "results" which doesn't exist in the API response.

        Args:
            project_ids: List of project IDs (not used in current implementation)

        Returns:
            Dictionary mapping project ID to project name
        """
        url = "https://api.todoist.com/api/v1/projects"

        response = self._make_request(url)
        data = response.json()

        # Note: The original Go code looked for "results" but v1 API returns array directly
        # This is likely a bug in the original code
        if isinstance(data, dict):
            projects = data.get("results", [])
        else:
            projects = data

        project_names = {}
        for project in projects:
            project_id = project.get("id", "")
            project_name = project.get("name", "")
            if project_id and project_name:
                project_names[str(project_id)] = project_name

        return project_names

    def get_project_names_for_v1_ids(self, project_ids: List[str]) -> Dict[str, str]:
        """
        Get project names for project IDs using the sync API.

        Args:
            project_ids: List of project IDs (not used in current implementation)

        Returns:
            Dictionary mapping project ID to project name
        """
        url = "https://api.todoist.com/sync/v9/sync"
        headers = {"Content-Type": "application/json"}
        params = {"resource_types": '["projects"]'}

        response = self._make_request(
            url, method="POST", headers=headers, params=params
        )
        data = response.json()

        projects = data.get("projects", [])
        if not projects:
            return {}

        project_names = {}
        for project in projects:
            project_id = project.get("id", "")
            project_name = project.get("name", "")
            if project_id and project_name:
                project_names[project_id] = project_name

        return project_names

    def get_tasks_for_project(self, project_id: str) -> List[Task]:
        """
        Retrieve tasks from a specific project.

        Args:
            project_id: The project ID to get tasks from

        Returns:
            List of Task objects
        """
        url = "https://api.todoist.com/rest/v2/tasks"
        params = {"project_id": project_id}

        response = self._make_request(url, params=params)
        tasks_data = response.json()
        return self._convert(tasks_data)

    def get_tasks_for_tag(self, tag_filter: str) -> List[Task]:
        """
        Retrieve tasks filtered by a specific tag.

        Args:
            tag_filter: The tag to filter by (without @ symbol)

        Returns:
            List of Task objects
        """
        url = "https://api.todoist.com/rest/v2/tasks"
        params = {"filter": f"@{tag_filter}"}

        response = self._make_request(url, params=params)
        tasks_data = response.json()
        return self._convert(tasks_data)

    def find_project_by_name_or_id(self, project_identifier: str) -> Tuple[str, str]:
        """
        Find a project by name or ID.

        Args:
            project_identifier: Project name or ID to search for

        Returns:
            Tuple of (project_id, project_name)

        Raises:
            TodoistAPIError: If project is not found
        """
        url = "https://api.todoist.com/rest/v2/projects"

        response = self._make_request(url)
        projects = response.json()

        # Perform exact match first
        for project in projects:
            project_id = str(project.get("id", ""))
            project_name = project.get("name", "")

            # Check if the identifier matches either ID or name (case-insensitive)
            if (
                project_id == project_identifier
                or project_name.lower() == project_identifier.lower()
            ):
                return project_id, project_name

        # Perform partial match next
        for project in projects:
            project_id = str(project.get("id", ""))
            project_name = project.get("name", "")

            # Check if the identifier is contained in the project name (case-insensitive)
            if project_identifier.lower() in project_name.lower():
                return project_id, project_name

        raise TodoistAPIError(f"Project not found: {project_identifier}")

    def _convert(self, tasks_data) -> List[Task]:
        """Convert tasks data json to Task objects"""
        return [
            Task(
                content=task_data.get("content", ""),
                id=task_data.get("id", ""),
                project_id=task_data.get("project_id", ""),
                url=task_data.get("url", ""),
            )
            for task_data in tasks_data
        ]

    def get_all_project_names(self) -> List[str]:
        """Get all project names"""
        url = "https://api.todoist.com/rest/v2/projects"
        logger.info(f"Getting all Todoist project names")
        response = self._make_request(url)
        projects = response.json()
        logger.info(f"Found {len(projects)} projects")
        return [project.get("name", "") for project in projects]
