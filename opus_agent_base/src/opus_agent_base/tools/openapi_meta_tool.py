import json
import yaml
import logging
from pathlib import Path
from typing import Any, Dict, Optional
import httpx
from pydantic_ai import RunContext
from pydantic_ai.tools import Tool
from fastmcp import FastMCP, Client
from opus_agent_base.common.logging_config import console_log
from opus_agent_base.config.config_manager import ConfigManager
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
            spec_properties={
                "spec_url": "https://api.example.com/openapi.json",
                "base_url": "https://api.example.com",
                "route_filters": [
                    ("method": "GET", "route": "/api/v1/users"),
                    ("method": "POST", "route": "/api/v1/users")
                ]
            }
        )
    """

    def __init__(
        self,
        name: str,
        config_manager: ConfigManager,
        config_key: str,
        spec_properties: Dict[str, Any],
    ):
        """
        Initialize the OpenAPIMetaTool.

        Args:
            name: The name of the meta tool
            config_key: The configuration key path for this tool
            spec_properties: The properties of the specification (URL, file path, etc.)
        """
        super().__init__(
            name=name,
            config_manager=config_manager,
            config_key=config_key,
            spec_properties=spec_properties,
        )
        self.spec_properties = spec_properties
        self.http_client: Optional[httpx.AsyncClient] = None
        self.spec = None

    async def setup_tool(self):
        """
        Setup the tool for use by the Agent.
        """
        logger.info("Setup OpenAPI MetaTool")
        spec = await self.load_spec()
        logger.debug(f"OpenAPI spec loaded: {spec}")
        mcp_server = await self.create_mcp_server()
        logger.debug("OpenAPI MCP Server created for Spec")
        client, tools = await self.create_mcp_client_and_initialize_tools()
        logger.debug("OpenAPI MCP Client and tools created")
        logger.info(f"OpenAPI Tools: {tools}")

    async def load_spec(self) -> Dict[str, Any]:
        """
        Load the OpenAPI specification from a URL or file.

        Returns:
            The loaded OpenAPI specification as a dictionary
        """
        try:
            # Check if spec_source is a URL
            spec_url = self.spec_properties.get("spec_url")
            if spec_url.startswith(("http://", "https://")):
                logger.info(f"Setup OpenAPI MetaTool by loading spec from URL: {spec_url}")
                async with httpx.AsyncClient() as client:
                    response = await client.get(spec_url)
                    response.raise_for_status()
                    # Get response content based on content type
                    content_type = response.headers.get("content-type", "")
                    if "application/json" in content_type:
                        spec_data = response.json()
                    elif "application/yaml" in content_type or "text/yaml" in content_type:
                        spec_data = yaml.safe_load(response.text)
                    else:
                        # Try JSON first, fall back to YAML
                        try:
                            spec_data = response.json()
                        except Exception:
                            spec_data = yaml.safe_load(response.text)
                    self.spec = spec_data

            logger.info(f"Successfully loaded OpenAPI spec: {self.spec}")
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
            # headers = self.auth_headers.copy()
            base_url = self.spec_properties.get("base_url")
            headers = {}
            self.http_client = httpx.AsyncClient(
                base_url=base_url,
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

    async def create_mcp_client_and_initialize_tools(self):
        """
        Create an MCP client and initialize tools from the loaded specification.

        Returns:
            A tuple of (MCP client, initialized tools)
        """
        # Create MCP client and discover tools
        async with Client(self.mcp_server) as client:
            self.client = client
            self.tools = await client.list_tools()
            print("Tools:", [t.name for t in self.tools])
            return self.client, self.tools


    async def call_dynamic_tool(self, tool_name: str, kwargs: dict={}):
        # Call one of the tools generated from OpenAPI
        async with Client(self.mcp_server) as client:
            result = await client.call_tool(tool_name, kwargs)
            print("Result:", result)
            return result

    async def initialize_tools(self, agent):
        """
        Initialize tools from the OpenAPI specification.

        This method creates the MCP server and makes its tools available to the agent.

        Args:
            agent: The agent instance to register tools with
        """
        try:
            logger.info(f"Initializing OpenAPI MetaTool: {self.name}")
            console_log(f"[MetaTool] Initializing OpenAPI MetaTool: {self.name}")

            # Add instructions to the Agent to use the tools
            allowed_apis: Optional[list[str]] = self.config_manager.get_setting(f"meta_tools.{self.name}.allowed_apis", None)
            dynamic_tool_name = f"call_dynamic_tool_{self.name}"

            @agent.instructions
            async def use_openapi_tool() -> str:
                try:
                    available_tools_usage_info = []
                    for tool in self.tools:
                        if allowed_apis is None or tool.name in allowed_apis:
                            # Assumption: description describes input and output parameters
                            tool_usage_info = f"""
## {tool.name}

API name: {tool.name}

Description: {tool.description}"""
                            available_tools_usage_info.append(tool_usage_info)
                    tool_instructions = f"""
# {self.name} APIs using OpenAPI MetaTool

This is a meta-tool to call OpenAPI APIs of {self.name}. Call the tool `{dynamic_tool_name}` to call specific APIs.

Available APIs of {self.name}:
{"----------\n".join(available_tools_usage_info)}

## Usage instructions:

To Call a specific API, call the tool `{dynamic_tool_name}` with:
1. api_name: The name of the API to call (required)
2. Any additional parameters required by that specific API (pass them directly, not wrapped in a dict)

IMPORTANT: Pass parameters directly to the function, not nested in a dictionary.

Example:
```
call_dynamic_tool(api_name="topstories_json")
call_dynamic_tool(api_name="getItem", id="45947810")
```
                    """
                    logger.info(f"OpenAPI Tool Instructions for {self.name}: {tool_instructions}")
                    return tool_instructions
                except Exception as e:
                    logger.error(f"Error calling use_openapi_tool: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                    raise

            logger.info(f"Successfully initialized OpenAPI MetaTool: {self.name}")
            console_log(f"[MetaTool] Successfully initialized: {self.name}")

        except Exception as e:
            logger.error(f"Error initializing OpenAPI MetaTool {self.name}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise


    async def build_agent_tool(self) -> Tool:
        """
        Build an agent tool from the OpenAPI specification.

        Returns:
            An agent tool instance
        """
        try:
            logger.info(f"Building OpenAPI MetaTool: {self.name}")
            console_log(f"[MetaTool] Building OpenAPI MetaTool: {self.name}")

            dynamic_tool_name = f"call_dynamic_tool_{self.name}"
            # Create dynamic tool with flexible schema to accept any parameters
            async def call_dynamic_tool_impl(**kwargs) -> Any:
                # Call one of the tools generated from OpenAPI
                api_name = kwargs.pop('api_name')
                logger.info(f"[OpenAPIMetaToolCall] Calling api_name: {api_name} with params: {kwargs}")
                console_log(f"[OpenAPIMetaToolCall] Calling api_name: {api_name} with params: {kwargs}")
                try:
                    async with Client(self.mcp_server) as client:
                        result = await client.call_tool(api_name, kwargs)
                        return result
                except Exception as e:
                    logger.error(f"Error calling dynamic tool {api_name}: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
                    raise

            # Create a flexible JSON schema that accepts tool_name and any additional parameters
            dynamic_tool_schema = {
                "type": "object",
                "properties": {
                    "api_name": {
                        "type": "string",
                        "description": f"The name of the {self.name} API to call"
                    }
                },
                "required": ["api_name"],
                "additionalProperties": True
            }

            # Register the tool using Tool.from_schema for flexible parameter handling
            dynamic_tool = Tool.from_schema(
                name=dynamic_tool_name,
                description=f"Call any API from the {self.name} OpenAPI specification. Pass api_name and any required parameters.",
                json_schema=dynamic_tool_schema,
                function=call_dynamic_tool_impl,
            )

            logger.info(f"Successfully built OpenAPI MetaTool: {self.name}")
            console_log(f"[MetaTool] Successfully built OpenAPI MetaTool: {self.name}")
            return dynamic_tool

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
