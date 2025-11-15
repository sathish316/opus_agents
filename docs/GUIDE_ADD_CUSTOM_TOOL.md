# Guide: Adding a Custom Tool

## What is a Custom Tool?

Custom tools are Python-based tools that perform an action or directly integrate with external APIs (like Todoist, Slack, etc.) without using MCP servers. They provide a way to add Skills to your agent.

Custom tools are ideal when:
- You want direct control over API integration
- No MCP server exists for your service
- You need to implement custom business logic

## Example: Query Tasks from Todoist with specific Tags

Let's say you want to query DeepWork tasks from Todoist and schedule them on your calendar. 

This guide will walk you through creating a custom tool that queries tasks tagged with "deepwork" from Todoist, with optional project filtering.

### Prerequisites

- Todoist API key (set as `TODOIST_API_KEY` environment variable)

---

## Step 1: Define Data Models

Create data models for your API responses. This ensures type safety and makes your code more maintainable.

**File:** `opus_todo_agent/src/opus_todo_agent/models/todo/todoist_models.py`

```python
from dataclasses import dataclass

@dataclass
class Task:
    """Represents an active task from Todoist"""

    content: str
    id: str
    url: str
    project_name: str = ""
```

---

## Step 2: Create API Clients

Create a client class to handle all API interactions. This separates concerns and makes testing easier.

**File:** `opus_todo_agent/src/opus_todo_agent/custom_tools/todo/todoist_client.py`

```python
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
```

---

## Step 3: Implement Custom Tools for Todoist

Now create Custom tool that the agent will use. This inherits from `CustomTool` base class.
The instructions that you specify in the tool comment are available to an AI agent to get context of the tool and when to invoke it.

**File:** `opus_todo_agent/src/opus_todo_agent/custom_tools/todo/todoist_tools.py`

```python
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
```

---

## Step 4: Add custom tool to your Agent

If you're extending an existing Agent, make these changes in `todo_agent_builder.py`. If you're building a new agent by following the GUIDE_BUILD_AN_AGENT.md, make these changes in `deepwork_agent_builder.py`

```python
    def _add_custom_tools(self):
        self.custom_tools: list[CustomTool] = [
            TodoistTools(),
        ]
```

Another option to add custom tools is to add tools to the AgentBuilder in `todo_agent_runner.py` or `deepwork_agent_runner.py`

```python
    DeepWorkAgentBuilder(config_manager)
        .name("deepwork-agent")
        .custom_tool(TodoistTools())
```

---

## Step 5: Enable the tool in config

Add configuration for your tool in the YAML config file.

**File:** `opus-config.yaml`

```yaml
mcp_config:
  productivity:
    todo:
      todoist:
        enabled: true  # Enable the Todoist custom tool

# Optional: Set your API key via environment variable
# export TODOIST_API_KEY="your_api_key_here"
```

---

## Step 6: Test Your Custom Tool

Run your agent and try these queries:

```bash
# Start the agent
uv run main.py

# Try these prompts:
> Show me my deep work tasks
> What deep work tasks do I have in the Research project?
> List all deep work tasks tagged with focus
> Show me my deep work tasks organized by project
```

## Next Steps

- Check out [Guide to Add higher order tool](./GUIDE_ADD_HIGHER_ORDER_TOOL.md)
- Check out [Guide to Build a new deepwork agent](./GUIDE_BUILD_NEW_DEEPWORK_AGENT.md) for adding these skills to an Agent

---

You've created a production-ready custom tool that queries Todoist for deep work tasks. This pattern can be adapted for any API integration or custom business logic, that is available as a skill to your Agent.

