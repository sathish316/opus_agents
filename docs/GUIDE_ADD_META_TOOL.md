# Guide: Adding a Meta Tool

## What is a Meta Tool?

Meta tools are powerful, specification-based tools that **dynamically create agent tools without writing any code**. It can be used for reusable Agent tools based on OpenAPI specs, Scraper, Bash/Python scripts etc.

## Example: HackerNews API Integration

Let's integrate the HackerNews API to let your agent fetch trending stories, and save interesting ones to your todo list.

With an OpenAPI Meta Tool, this entire integration is effortless:

### Prerequisites

- An OpenAPI specification for your target API e.g. `https://api.example.com/openapi.json`

---

## Step 1: Create Your Meta Tool Class

Create a class that inherits from `OpenAPIMetaTool`. This is the only code you'll write.

**File:** `<agent-src>/meta_tools/hackernews_meta_tool.py`

```python
logger = logging.getLogger(__name__)


class HackerNewsMetaTool(OpenAPIMetaTool):
    """
    MetaTool for HackerNews API.

    This tool dynamically creates tools from the HackerNews OpenAPI specification,
    allowing the agent to:
    - Fetch top stories
    - Get details for specific stories

    Example usage with the agent:
    - "Show me the top 5 stories on HackerNews"
    - "Get details about HackerNews story 12345"
    - "Find HackerNews top posts about Functional programming"
    """

    def __init__(
        self,
        config_manager,
    ):
        spec_properties = {
            "spec_url": "https://raw.githubusercontent.com/andenacitelli/hacker-news-api-openapi/main/exports/api.yaml",
            "base_url": "https://hacker-news.firebaseio.com/v0",
        }

        # Initialize with the OpenAPI spec
        super().__init__(
            name="hackernews_api",
            config_manager=config_manager,
            config_key="meta_tools.hackernews",
            spec_properties=spec_properties,
        )
```

## Step 2: Customize Prompts for your Meta-tool

The HackerNews API is complex requiring you to call a Top stories API to get story IDs and N calls to getItem APIs to fetch the story title.
Sometimes, this has to be fed into the agent as instructions.

2.1 To customize the prompt for your meta-tool, add a prompt markdown file:

**File:** `prompts/tools/deepwork/HACKERNEWS_METATOOL_PROMPT.md`

```markdown
Guidelines:
If the user asks a question related to HackerNews APIs:
1. Use the API name topstories_json to get the top stories
2. Use the API name getItem to get the details of the stories like Title, Time etc.
3. Use the tools `call_dynamic_tool_hackernews_api` to call these APIs with:
    a. api_name: The name of the API to call (required)
    b. Any additional parameters required by that specific API (pass them directly, not wrapped in a dict)
4. Example:
```
call_dynamic_tool_hackernews_api(api_name="topstories_json")
call_dynamic_tool_hackernews_api(api_name="getItem", id=45947810)
```
5. Before returning the result, summarize the stories in this format, with a separator between each story:
* ID
* URL
* Title
* Time
------
```

2.2 Add the prompt to Agent's InstructionManager:

**File:** `<agent-src>/deepwork_agent_runner.py`

```python
    deepwork_agent = (
        DeepWorkAgentBuilder(config_manager)
        .name("deepwork-agent")
        .instruction(
            "hackernews_meta_tool_prompt", "prompts/tools/deepwork/HACKERNEWS_METATOOL_PROMPT.md"
        )
```

2.3 Add the prompt to Agent's instructions:

**File:** `<agent-src>/meta_tools/hackernews_meta_tool.py`

```python
class HackerNewsMetaTool(OpenAPIMetaTool):
    async def initialize_tools(self, agent: Agent):
        """
        HackerNews OpenAPI specific instructions and tools for the agent.

        Args:
            agent: The agent instance to register tools with
        """
        await super().initialize_tools(agent)

        @agent.instructions
        async def use_hackernews_openapi_tool() -> str:
            return self.instruction_manager.get("hackernews_meta_tool_prompt")
```

---

## Step 3: Add Meta Tool to Your Agent

Update your agent builder to include the meta tool.

**File:** `<agent-src>/meta_tools/hackernews_meta_tool.py`

```python
    deepwork_agent = (
        DeepWorkAgentBuilder(config_manager)
        .name("deepwork-agent")
        .meta_tool(HackerNewsMetaTool(config_manager))
```

This is all the code you need to write for a meta-tool. The MetaTool will:
1. Load the OpenAPI specification
2. Parse all endpoints and their parameters
3. Automatically create agent tools that can be used to call these OpenAPI endpoints
4. Additionally, you can configure which APIs are allowed for the Agent using the config parameter `meta_tools.<tool_name>.allowed_apis`

---

## Step 4: Use Your Meta Tool with the Agent

Run your agent and try queries that leverage the HackerNews API:

> Show me the top 5 stories on HackerNews right now

> find the top stories on hackernews front page. If there are any stories about Functional programming, add it to my Todoist list with the tag toread