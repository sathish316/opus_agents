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
        instruction_manager
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
        self.instruction_manager = instruction_manager

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
