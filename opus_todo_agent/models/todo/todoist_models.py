from dataclasses import dataclass


@dataclass
class CompletedTask:
    """Represents a completed task from Todoist"""

    content: str
    id: str
    project_id: str
    completed_date: str
    project_name: str = ""

    def with_project_name(self, project_name: str) -> "CompletedTask":
        """Return a new CompletedTask instance with the project name set"""
        return CompletedTask(
            content=self.content,
            id=self.id,
            project_id=self.project_id,
            completed_date=self.completed_date,
            project_name=project_name,
        )


@dataclass
class Task:
    """Represents an active task from Todoist"""

    content: str
    id: str
    project_id: str
    url: str
    project_name: str = ""

    def with_project_name(self, project_name: str) -> "Task":
        """Return a new Task instance with the project name set"""
        return Task(
            content=self.content,
            id=self.id,
            project_id=self.project_id,
            url=self.url,
            project_name=project_name,
        )
