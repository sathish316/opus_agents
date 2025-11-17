# Guide: Adding a Meta Tool

## What is a Meta Tool?

Meta tools are powerful, specification-based tools that **dynamically create agent tools from API specifications without writing any code**. They eliminate the need for manual API integration code by leveraging standard API descriptions like OpenAPI specs.

Meta tools are ideal when:
- You want to integrate APIs without writing custom integration code
- An OpenAPI (or similar) specification exists for the API
- You need to rapidly prototype integrations with external services
- You want to expose any REST API directly to your agent with minimal setup

## How Meta Tools Differ from Custom Tools

| Feature | Custom Tool | Meta Tool |
|---------|-------------|-----------|
| **Code Required** | Write Python code for each endpoint | Zero code - uses spec file |
| **Setup Time** | Hours to days | Minutes |
| **Maintenance** | Manual updates when API changes | Auto-updates from spec |
| **Best For** | Complex business logic, custom workflows | Standard REST APIs with OpenAPI specs |

## Example: HackerNews API Integration

Let's integrate the HackerNews API to let your agent fetch trending stories, analyze articles, and save interesting ones to your todo list.

With a Meta Tool, this entire integration takes **less than 5 minutes** and requires **no API integration code**.

### Prerequisites

- An OpenAPI specification for your target API
  - Can be a URL (e.g., `https://api.example.com/openapi.json`)
  - Can be a local file (`.json`, `.yaml`, `.yml`)

---

## Step 1: Create Your Meta Tool Class

Create a class that inherits from `OpenAPIMetaTool`. This is the only code you'll write.

**File:** `example_deepwork_agent/src/opus_deepwork_agent/meta_tools/hackernews_meta_tool.py`

```python
import logging
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
    ):
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
```

**That's it!** This is all the code you need to write. The MetaTool will:
1. Load the OpenAPI specification
2. Parse all endpoints and their parameters
3. Automatically create agent tools for each endpoint
4. Handle request/response formatting
5. Manage authentication (if configured)

---

## Step 2: Add Meta Tool to Your Agent

Update your agent builder to include the meta tool.

**File:** `example_deepwork_agent/src/opus_deepwork_agent/deepwork_agent_builder.py`

```python
from opus_agent_base.agent.agent_builder import AgentBuilder
from opus_agent_base.config.config_manager import ConfigManager
from opus_deepwork_agent.meta_tools.hackernews_meta_tool import HackerNewsMetaTool


class DeepWorkAgentBuilder(AgentBuilder):
    """Builder for DeepWork Agent"""

    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)

    def build(self) -> AgentBuilder:
        """Build the DeepWork agent with all components"""
        self._add_mcp_servers_config()
        self._add_meta_tools()
        return self

    def _add_meta_tools(self):
        """Add meta tools (HackerNews API)"""
        self.meta_tools = [
            HackerNewsMetaTool(
                config_manager=self.config_manager,
            ),
        ]
```

Alternatively, you can add meta tools directly to the agent runner:

**File:** `example_deepwork_agent/src/opus_deepwork_agent/deepwork_agent_runner.py`

```python
DeepWorkAgentBuilder(config_manager)
    .name("deepwork-agent")
    .meta_tool(HackerNewsMetaTool(config_manager=config_manager))
    .build()
```

---

## Step 3: Enable the Meta Tool in Config

Add configuration for your meta tool in the YAML config file.

**File:** `opus_config.deepwork.yml`

```yaml
# MCP Server Configuration
mcp_config:
  general:
    datetime:
      enabled: true

  # Meta Tools Configuration
  meta_tools:
    hackernews:
      enabled: true  # Enable the HackerNews meta tool

  deepwork:
    todo:
      todoist:
        enabled: true
    calendar:
      clockwise:
        enabled: true
```

---

## Step 4: Use Your Meta Tool with the Agent

Run your agent and try queries that leverage the HackerNews API:

```bash
# Start the agent
uv run main.py

# Try these prompts:
> Show me the top 5 stories on HackerNews right now

> Find interesting articles about AI on HackerNews and add them to my Todoist with tag "toread"

> Get details about HackerNews story ID 12345

> What are the trending topics on HackerNews today?

> Find articles about machine learning on HackerNews and summarize the top 3
```

The agent will automatically:
1. Use the meta tool to fetch HackerNews data
2. Parse and understand the results
3. Combine with other tools (like Todoist) for complex workflows

---

## Advanced: Adding Authentication

Many APIs require authentication. Meta tools support various auth methods:

### API Key Authentication

```python
class SecureAPIMetaTool(OpenAPIMetaTool):
    def __init__(self, config_manager=None, **kwargs):
        import os

        # Get API key from environment
        api_key = os.getenv("MY_API_KEY")
        if not api_key:
            raise ValueError("MY_API_KEY environment variable not set")

        # Pass auth headers
        auth_headers = {
            "Authorization": f"Bearer {api_key}"
        }

        super().__init__(
            name="secure_api",
            config_key="meta_tools.secure_api",
            spec_source="https://api.example.com/openapi.json",
            base_url="https://api.example.com",
            config_manager=config_manager,
            auth_headers=auth_headers,
        )
```

### Setting API Keys

```bash
# Set in your environment
export MY_API_KEY="your_api_key_here"

# Or in .env file
echo "MY_API_KEY=your_api_key_here" >> .env
```

---

## Advanced: Using Local OpenAPI Specs

You can use local specification files instead of URLs:

```python
from pathlib import Path

class LocalAPIMetaTool(OpenAPIMetaTool):
    def __init__(self, config_manager=None, **kwargs):
        # Get path to local spec file
        spec_path = Path(__file__).parent.parent / "specs" / "my_api_openapi.json"

        super().__init__(
            name="local_api",
            config_key="meta_tools.local_api",
            spec_source=str(spec_path),  # Use local file
            base_url="https://api.example.com",
            config_manager=config_manager,
        )
```

Supported formats:
- `.json` - JSON OpenAPI specs
- `.yaml` / `.yml` - YAML OpenAPI specs

---

## Advanced: Filtering Endpoints

You can filter which endpoints are exposed to the agent using route filters:

```python
class FilteredAPIMetaTool(OpenAPIMetaTool):
    def __init__(self, config_manager=None, **kwargs):
        # Only expose GET endpoints
        route_filters = {
            "methods": ["GET"],  # Only GET requests
            "tags": ["public"],  # Only endpoints tagged as "public"
        }

        super().__init__(
            name="filtered_api",
            config_key="meta_tools.filtered_api",
            spec_source="https://api.example.com/openapi.json",
            base_url="https://api.example.com",
            config_manager=config_manager,
            route_filters=route_filters,
        )
```

---

## Example: Weather API Integration

Here's another complete example using a weather API:

```python
import os
from opus_agent_base.tools.openapi_meta_tool import OpenAPIMetaTool


class WeatherAPIMetaTool(OpenAPIMetaTool):
    """
    MetaTool for Weather API.

    Enables agent to:
    - Get current weather for any location
    - Fetch weather forecasts
    - Search weather by coordinates
    """

    def __init__(self, config_manager=None, **kwargs):
        # Get API key from environment
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            raise ValueError("WEATHER_API_KEY environment variable not set")

        super().__init__(
            name="weather_api",
            config_key="meta_tools.weather",
            spec_source="https://api.weather.com/openapi.json",
            base_url="https://api.weather.com/v1",
            config_manager=config_manager,
            auth_headers={"X-API-Key": api_key},
        )
```

**Config:**
```yaml
mcp_config:
  meta_tools:
    weather:
      enabled: true
```

**Usage:**
```bash
> What's the weather in San Francisco?
> Will it rain tomorrow in New York?
> Get me a 5-day forecast for Tokyo
```

---

## Troubleshooting

### Meta Tool Not Working

1. **Check if enabled in config:**
   ```yaml
   mcp_config:
     meta_tools:
       your_tool_name:
         enabled: true
   ```

2. **Verify OpenAPI spec is accessible:**
   - For URLs: Check that the URL is publicly accessible
   - For files: Verify the file path is correct and file exists

3. **Check logs:**
   ```bash
   # Look for meta tool initialization messages
   [MetaTool] Initializing OpenAPI MetaTool: your_tool_name
   [MetaTool] Successfully initialized: your_tool_name
   ```

### Authentication Errors

1. **Verify environment variables are set:**
   ```bash
   echo $MY_API_KEY
   ```

2. **Check auth header format:**
   - API Key: `{"X-API-Key": "key"}` or `{"Authorization": "Bearer key"}`
   - Basic Auth: `{"Authorization": "Basic base64_encoded_credentials"}`

### OpenAPI Spec Issues

1. **Invalid spec format:**
   - Ensure spec is valid OpenAPI 3.x format
   - Use online validators: https://editor.swagger.io/

2. **Missing operationIds:**
   - OpenAPI specs should have unique `operationId` for each endpoint
   - FastMCP uses these to generate tool names

---

## Key Concepts

### Meta Tool Architecture

```
┌─────────────────────────────────────────────┐
│           Your Agent                        │
│  ┌────────────────────────────────────┐    │
│  │      HackerNewsMetaTool            │    │
│  │  (5 lines of code)                 │    │
│  └────────────┬───────────────────────┘    │
│               │                             │
│               ▼                             │
│  ┌────────────────────────────────────┐    │
│  │    OpenAPIMetaTool (Base Class)    │    │
│  │  - Loads OpenAPI spec               │    │
│  │  - Parses endpoints                 │    │
│  │  - Creates MCP server               │    │
│  │  - Generates tools automatically    │    │
│  └────────────┬───────────────────────┘    │
│               │                             │
│               ▼                             │
│  ┌────────────────────────────────────┐    │
│  │      FastMCP (from_openapi)        │    │
│  │  Converts OpenAPI → MCP Tools      │    │
│  └────────────┬───────────────────────┘    │
└───────────────┼─────────────────────────────┘
                │
                ▼
        ┌──────────────────┐
        │   External API    │
        │  (HackerNews)     │
        └──────────────────┘
```

### When to Use Meta Tools vs Custom Tools

**Use Meta Tools when:**
- ✅ OpenAPI spec exists for the API
- ✅ You need standard REST API calls
- ✅ You want rapid prototyping
- ✅ API has many endpoints (meta tool handles all automatically)
- ✅ Minimal custom logic needed

**Use Custom Tools when:**
- ✅ No OpenAPI spec available
- ✅ Complex business logic required
- ✅ Need to combine multiple APIs
- ✅ Custom data transformations needed
- ✅ Special authentication flows

**Use Higher-Order Tools when:**
- ✅ Orchestrating multiple tool calls
- ✅ Building workflows across services
- ✅ Agent-to-agent coordination needed

---

## Real-World Examples

### 1. GitHub API Integration

```python
class GitHubMetaTool(OpenAPIMetaTool):
    def __init__(self, config_manager=None, **kwargs):
        github_token = os.getenv("GITHUB_TOKEN")

        super().__init__(
            name="github_api",
            config_key="meta_tools.github",
            spec_source="https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json",
            base_url="https://api.github.com",
            config_manager=config_manager,
            auth_headers={"Authorization": f"Bearer {github_token}"},
        )
```

**Agent Usage:**
```bash
> Show me my open pull requests
> Create an issue in my repo about the bug we discussed
> Get the latest release notes for project XYZ
```

### 2. Stripe API Integration

```python
class StripeMetaTool(OpenAPIMetaTool):
    def __init__(self, config_manager=None, **kwargs):
        stripe_key = os.getenv("STRIPE_SECRET_KEY")

        super().__init__(
            name="stripe_api",
            config_key="meta_tools.stripe",
            spec_source="https://raw.githubusercontent.com/stripe/openapi/master/openapi/spec3.json",
            base_url="https://api.stripe.com",
            config_manager=config_manager,
            auth_headers={"Authorization": f"Bearer {stripe_key}"},
        )
```

**Agent Usage:**
```bash
> Show me today's payments
> Create an invoice for customer XYZ
> What's my MRR for this month?
```

---

## Next Steps

- **Multiple APIs?** Create multiple meta tools and add them all to your agent
- **Need custom logic?** Combine meta tools with [Custom Tools](./GUIDE_ADD_CUSTOM_TOOL.md)
- **Building workflows?** Use [Higher-Order Tools](./GUIDE_ADD_HIGHER_ORDER_TOOL.md) to orchestrate
- **Creating a new agent?** See [Guide to Build an Agent](./GUIDE_BUILD_NEW_DEEPWORK_AGENT.md)

---

## Summary

Meta tools represent a paradigm shift in agent development:

- **Zero integration code** - Just point to an OpenAPI spec
- **Instant API access** - All endpoints become agent tools automatically
- **Self-documenting** - Agent understands API from the spec
- **Easy maintenance** - Update spec, tools update automatically
- **Production-ready** - Built on FastMCP and industry standards

You've now learned how to integrate any OpenAPI-based API into your agent in minutes, not hours. This pattern works for thousands of public APIs including GitHub, Stripe, Twilio, SendGrid, and many more!
