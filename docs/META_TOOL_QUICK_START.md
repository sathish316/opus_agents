# MetaTool Quick Start

## What You Get

Zero-code API integration for your agents. Point to an OpenAPI spec, and all endpoints become agent tools automatically.

## 5-Minute Setup

### 1. Create Your Meta Tool (30 seconds)

```python
# my_agent/meta_tools/my_api_tool.py
from opus_agent_base.tools.openapi_meta_tool import OpenAPIMetaTool

class MyAPITool(OpenAPIMetaTool):
    def __init__(self, config_manager=None):
        super().__init__(
            name="my_api",
            config_key="meta_tools.my_api",
            spec_source="https://api.example.com/openapi.json",  # Your OpenAPI spec
            base_url="https://api.example.com",
            config_manager=config_manager,
        )
```

### 2. Add to Agent (30 seconds)

```python
# my_agent/agent_builder.py
from my_agent.meta_tools.my_api_tool import MyAPITool

def _add_meta_tools(self):
    self.meta_tools = [
        MyAPITool(config_manager=self.config_manager),
    ]
```

### 3. Enable in Config (30 seconds)

```yaml
# opus_config.yml
mcp_config:
  meta_tools:
    my_api:
      enabled: true
```

### 4. Use It! (3 minutes)

```bash
uv run main.py

> Call the API and get the data
> Analyze the results and summarize
> Combine with other tools...
```

## Real Example: HackerNews

See the working example in `example_deepwork_agent/`:

```python
# Already implemented and working!
from opus_deepwork_agent.meta_tools.hackernews_meta_tool import HackerNewsMetaTool

# Try it:
> Show me top HackerNews stories
> Find AI articles and add them to my Todoist
```

## Adding Authentication

```python
import os

class SecureAPITool(OpenAPIMetaTool):
    def __init__(self, config_manager=None):
        api_key = os.getenv("MY_API_KEY")

        super().__init__(
            name="secure_api",
            config_key="meta_tools.secure_api",
            spec_source="https://api.example.com/openapi.json",
            base_url="https://api.example.com",
            config_manager=config_manager,
            auth_headers={"Authorization": f"Bearer {api_key}"},
        )
```

## Works With

Any API with an OpenAPI specification:
- ✅ GitHub
- ✅ Stripe
- ✅ Twilio
- ✅ SendGrid
- ✅ Slack
- ✅ +1000s more

## Full Guide

See [GUIDE_ADD_META_TOOL.md](./GUIDE_ADD_META_TOOL.md) for:
- Advanced authentication
- Local spec files
- Route filtering
- Troubleshooting
- Real-world examples

## That's It!

You've just learned how to integrate any OpenAPI-based API into your agent without writing integration code. 🚀
