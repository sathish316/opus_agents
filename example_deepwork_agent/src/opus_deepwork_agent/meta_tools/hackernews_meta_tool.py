import logging

from opus_agent_base.tools.openapi_meta_tool import OpenAPIMetaTool
from pydantic_ai import Agent
from opus_agent_base.common.logging_config import console_log

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

        logger.info("HackerNews MetaTool initialized")

    async def initialize_tools(self, agent: Agent):
        """
        HackerNews OpenAPI specific instructions and tools for the agent.

        Args:
            agent: The agent instance to register tools with
        """
        await super().initialize_tools(agent)
        logger.info(f"Initializing HackerNews OpenAPI MetaTool: {self.name}")
        console_log(f"[MetaTool] Initializing HackerNews OpenAPI MetaTool: {self.name}")

        @agent.instructions
        async def use_hackernews_openapi_tool() -> str:
            return """
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
5. Before returning the result, summarize the stories in this format:
* ID
* URL
* Title
* Time
            """