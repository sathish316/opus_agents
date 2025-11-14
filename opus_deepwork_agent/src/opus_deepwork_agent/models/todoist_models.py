from dataclasses import dataclass

@dataclass
class Task:
    """Represents an active task from Todoist"""

    content: str
    id: str
    url: str
    project_name: str = ""
