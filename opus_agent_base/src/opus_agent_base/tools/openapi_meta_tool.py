import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional
import httpx

from fastmcp import FastMCP
from opus_agent_base.common.logging_config import console_log
from opus_agent_base.tools.meta_tool import MetaTool

logger = logging.getLogger(__name__)


class OpenAPIMetaTool(MetaTool):
    """
    MetaTool implementation for OpenAPI specifications.

    This tool dynamically creates MCP tools from OpenAPI specs without requiring
    custom code. It can load specs from URLs or local files and automatically
    exposes API endpoints as agent tools.

    Example usage:
        tool = OpenAPIMetaTool(
            name="hackernews_api",
            config_key="meta_tools.hackernews",
            spec_source="https://api.example.com/openapi.json",
            base_url="https://api.example.com",
            config_manager=config_manager
        )
    """

    def __init__(
        self,
        name: str,
        config_key: str,
        spec_source: str,
        base_url: str,
        config_manager=None,
        instructions_manager=None,
        model_manager=None,
        auth_headers: Optional[Dict[str, str]] = None,
        route_filters: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the OpenAPIMetaTool.

        Args:
            name: The name of the meta tool
            config_key: The configuration key path for this tool
            spec_source: URL or file path to the OpenAPI specification
            base_url: Base URL for the API
            config_manager: Configuration manager instance
            instructions_manager: Instructions manager instance
            model_manager: Model manager instance
            auth_headers: Optional authentication headers (e.g., {"Authorization": "Bearer token"})
            route_filters: Optional filters for which routes to expose
        """
        super().__init__(
            name=name,
            config_key=config_key,
            spec_source=spec_source,
            config_manager=config_manager,
            instructions_manager=instructions_manager,
            model_manager=model_manager,
        )
        self.base_url = base_url
        self.auth_headers = auth_headers or {}
        self.route_filters = route_filters or {}
        self.mcp_server: Optional[FastMCP] = None
        self.http_client: Optional[httpx.AsyncClient] = None

    async def load_spec(self) -> Dict[str, Any]:
        """
        Load the OpenAPI specification from a URL or file.

        Returns:
            The loaded OpenAPI specification as a dictionary
        """
        try:
            # Check if spec_source is a URL
            if self.spec_source.startswith(("http://", "https://")):
                logger.info(f"Loading OpenAPI spec from URL: {self.spec_source}")
                async with httpx.AsyncClient() as client:
                    response = await client.get(self.spec_source)
                    response.raise_for_status()
                    self.spec = response.json()
            else:
                # Load from file
                logger.info(f"Loading OpenAPI spec from file: {self.spec_source}")
                spec_path = Path(self.spec_source)
                if not spec_path.exists():
                    raise FileNotFoundError(f"OpenAPI spec file not found: {self.spec_source}")

                with open(spec_path, "r") as f:
                    if spec_path.suffix in [".json"]:
                        self.spec = json.load(f)
                    elif spec_path.suffix in [".yaml", ".yml"]:
                        import yaml
                        self.spec = yaml.safe_load(f)
                    else:
                        raise ValueError(
                            f"Unsupported file format: {spec_path.suffix}. "
                            "Supported formats: .json, .yaml, .yml"
                        )

            logger.info(f"Successfully loaded OpenAPI spec: {self.spec.get('info', {}).get('title', 'Unknown')}")
            return self.spec

        except Exception as e:
            logger.error(f"Error loading OpenAPI spec: {e}")
            raise

    async def create_mcp_server(self):
        """
        Create an MCP server from the loaded OpenAPI specification.

        Returns:
            A FastMCP server instance configured with the OpenAPI spec
        """
        if not self.spec:
            await self.load_spec()

        try:
            # Create HTTP client with auth headers
            headers = self.auth_headers.copy()
            self.http_client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=30.0
            )

            # Create MCP server from OpenAPI spec
            logger.info(f"Creating MCP server from OpenAPI spec: {self.name}")

            # Use FastMCP's from_openapi functionality
            self.mcp_server = FastMCP.from_openapi(
                openapi_spec=self.spec,
                client=self.http_client,
                name=self.name,
            )

            logger.info(f"Successfully created MCP server: {self.name}")
            console_log(f"[MetaTool] Created MCP server from OpenAPI spec: {self.name}")

            return self.mcp_server

        except Exception as e:
            logger.error(f"Error creating MCP server: {e}")
            raise

    async def initialize_tools(self, fastmcp_client_context):
        """
        Initialize tools from the OpenAPI specification.

        This method creates the MCP server and makes its tools available to the agent.

        Args:
            fastmcp_client_context: The FastMCP client context for tool integration
        """
        if not self.is_enabled():
            logger.info(f"MetaTool {self.name} is disabled in configuration")
            return

        try:
            logger.info(f"Initializing OpenAPI MetaTool: {self.name}")
            console_log(f"[MetaTool] Initializing OpenAPI MetaTool: {self.name}")

            # Create the MCP server
            await self.create_mcp_server()

            logger.info(f"Successfully initialized OpenAPI MetaTool: {self.name}")
            console_log(f"[MetaTool] Successfully initialized: {self.name}")

        except Exception as e:
            logger.error(f"Error initializing OpenAPI MetaTool {self.name}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    async def cleanup(self):
        """Clean up resources like HTTP clients."""
        if self.http_client:
            await self.http_client.aclose()
            logger.info(f"Closed HTTP client for {self.name}")
