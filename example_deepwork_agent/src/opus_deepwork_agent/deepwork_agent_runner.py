import logging

from opus_agent_base.agent.agent_runner import AgentRunner
from opus_agent_base.config.config_manager import ConfigManager

from opus_deepwork_agent.custom_tools.calendar.clockwise_tools import (
    ClockwiseHigherOrderTool,
)
from opus_deepwork_agent.custom_tools.todo.todoist_tools import TodoistTools
from opus_deepwork_agent.deepwork_agent_builder import DeepWorkAgentBuilder

logger = logging.getLogger(__name__)


async def run_deepwork_agent():
    """Run DeepWork Agent using AgentRunner"""
    logger.info("🎯 Starting DeepWork Agent")

    # Build DeepWork Agent
    config_manager = ConfigManager()
    deepwork_agent = (
        DeepWorkAgentBuilder(config_manager)
        .name("deepwork-agent")
        .set_system_prompt_keys(["opus_agent_instruction", "deepwork_agent_instruction"])
        .add_instructions_manager()
        .add_model_manager()
        .add_mcp_manager()
        .instruction(
            "opus_agent_instruction", "prompts/agent/OPUS_AGENT_INSTRUCTIONS.md"
        )
        .instruction(
            "deepwork_agent_instruction", "prompts/agent/DEEPWORK_AGENT_INSTRUCTIONS.md"
        )
        .custom_tool(TodoistTools())
        .higher_order_tool(ClockwiseHigherOrderTool())
        .build()
    )

    # Run DeepWork Agent
    agent_runner = AgentRunner(name="deepwork-agent", agent_builder=deepwork_agent)
    await agent_runner.run_agent()
