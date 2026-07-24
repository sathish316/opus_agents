import os

import pytest
from opus_agent_base.tools.lambda_as_tool import lambda_as_tool
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.getenv("RUN_GPT_OSS_INTEGRATION") != "1",
        reason="Set RUN_GPT_OSS_INTEGRATION=1 to run gpt-oss integration tests",
    ),
]


@pytest.mark.asyncio
async def test_gpt_oss_calls_lambda_tool():
    model = OpenAIChatModel(
        model_name=os.getenv("GPT_OSS_MODEL", "gpt-oss:20b"),
        provider=OllamaProvider(
            base_url=os.getenv("GPT_OSS_BASE_URL", "http://127.0.0.1:8080/v1")
        ),
    )
    agent = Agent(
        model,
        system_prompt=(
            "Always use the celsius_to_fahrenheit tool for temperature conversions."
        ),
    )
    lambda_as_tool(
        lambda celsius: (celsius * 9 / 5) + 32,
        name="celsius_to_fahrenheit",
        description="Convert a Celsius temperature to Fahrenheit.",
    ).initialize_tools(agent)

    result = await agent.run("Convert 100 degrees Celsius to Fahrenheit.")

    assert "212" in str(result.output)
