import logging
import os
from typing import Dict, List, Optional

import requests
from opus_deepwork_agent.models.todoist_models import Task

logger = logging.getLogger(__name__)

class TodoistClient:
    """Todoist API client"""

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
            raise TodoistAPIError(f"HTTP request failed: {e}")

    def get_tasks_with_tag(
        self, tag_name: str = "deepwork", project_name: Optional[str] = None
    ) -> List[Task]:
        """
        Retrieve tasks filtered by a specific tag.

        Args:
            tag_name: The tag to filter by (default: "deepwork")
            project_id: Optional project ID to filter tasks

        Returns:
            List of Task objects matching the criteria
        """
        url = "https://api.todoist.com/rest/v2/tasks"

        # Build filter query
        if project_name:
            filter_query = f"@{tag_name} & #{project_name}"
        else:
            filter_query = f"@{tag_name}"

        logger.info(f"Fetching tasks with filter: {filter_query}")
        headers = {}
        headers["Authorization"] = f"Bearer {self.api_key}"
        params = {"filter": filter_query}
        response = response = requests.get(url, headers=headers, params=params)
        tasks_data = response.json()

        return self._convert_to_tasks(tasks_data)

    def _convert_to_tasks(self, tasks_data) -> List[Task]:
        """Convert JSON response to Task objects"""
        return [
            Task(
                content=task_data.get("content", ""),
                id=task_data.get("id", ""),
                project_name=task_data.get("project_name", ""),
                url=task_data.get("url", ""),
            )
            for task_data in tasks_data
        ]
