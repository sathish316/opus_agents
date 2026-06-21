import httpx
import pytest
import yaml

from opus_agent_base.agent.agent_builder import AgentBuilder
from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.model.model_manager import ModelManager

LOCAL_LLM_BASE_URL = "http://127.0.0.1:8080/v1"
LOCAL_LLM_MODEL = "gpt-oss:20b"


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def is_local_llm_available() -> bool:
    try:
        response = httpx.get(f"{LOCAL_LLM_BASE_URL}/models", timeout=2.0)
        return response.status_code == 200
    except (httpx.HTTPError, OSError):
        return False


@pytest.fixture
def local_llm_config(tmp_path):
    instructions_file = tmp_path / "instructions.md"
    instructions_file.write_text(
        "You are a helpful assistant.\n"
        "When asked to convert Celsius to Fahrenheit, call celsius_to_fahrenheit.\n"
        "Reply with only the numeric Fahrenheit value."
    )

    config_dir = tmp_path / ".opusai"
    config_dir.mkdir()
    config_file = config_dir / "opus-config.yml"
    config_file.write_text(
        yaml.dump(
            {
                "model_config": [
                    {
                        "provider": "ollama",
                        "model": LOCAL_LLM_MODEL,
                        "enabled": True,
                        "is_local": True,
                        "base_url": LOCAL_LLM_BASE_URL,
                    }
                ],
                "mcp_config": {
                    "framework": {
                        "lambda": {
                            "enabled": True,
                        }
                    }
                },
                "debug": {"log_level": "ERROR"},
            }
        )
    )
    return ConfigManager(str(config_dir), "opus-config.yml"), instructions_file


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.skipif(
    not is_local_llm_available(),
    reason="Local LLM server is not available at http://127.0.0.1:8080/v1",
)
async def test_lambda_tool_with_local_gpt_oss(local_llm_config):
    config_manager, instructions_file = local_llm_config
    model_manager = ModelManager(config_manager)
    local_model = model_manager.get_local_model()
    assert local_model is not None

    builder = (
        AgentBuilder(config_manager)
        .set_system_prompt_keys(["instructions"])
        .add_instructions_manager()
        .instruction("instructions", str(instructions_file))
        .add_model_manager()
        .lambda_tool(celsius_to_fahrenheit, name="temperature")
    )
    agent = builder.build_agent()
    agent.model = local_model

    result = await agent.run("Convert 100 degrees Celsius to Fahrenheit.")

    output = str(result.output).strip()
    assert "212" in output
