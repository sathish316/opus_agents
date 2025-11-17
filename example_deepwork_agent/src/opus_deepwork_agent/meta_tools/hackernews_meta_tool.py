import logging
from pathlib import Path

from opus_agent_base.tools.openapi_meta_tool import OpenAPIMetaTool

logger = logging.getLogger(__name__)


class HackerNewsMetaTool(OpenAPIMetaTool):
    """
    MetaTool for HackerNews API.

    This tool dynamically creates tools from the HackerNews OpenAPI specification,
    allowing the agent to:
    - Fetch top, new, and best stories
    - Get details for specific stories
    - Retrieve user information

    Example usage with the agent:
    - "Show me the top 5 stories on HackerNews"
    - "Get details about HackerNews story 12345"
    - "Find HackerNews stories about AI and machine learning"
    """

    def __init__(
        self,
        config_manager=None,
        instructions_manager=None,
        model_manager=None,
        use_local_spec=False,
    ):
        # Use publicly available OpenAPI spec from GitHub by default
        # Or use local spec file if specified
        if use_local_spec:
            spec_path = (
                Path(__file__).parent.parent / "specs" / "hackernews_openapi.json"
            )
            spec_source = str(spec_path)
        else:
            # Use publicly available OpenAPI spec from GitHub
            spec_source = "https://raw.githubusercontent.com/andenacitelli/hacker-news-api-openapi/main/exports/api.yaml"

        # Initialize with the OpenAPI spec
        super().__init__(
            name="hackernews_api",
            config_key="meta_tools.hackernews",
            spec_source=spec_source,
            base_url="https://hacker-news.firebaseio.com/v0",
            config_manager=config_manager,
            instructions_manager=instructions_manager,
            model_manager=model_manager,
        )

        logger.info("HackerNews MetaTool initialized")
