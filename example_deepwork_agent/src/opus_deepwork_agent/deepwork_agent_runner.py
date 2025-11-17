import logging

from opus_deepwork_agent.custom_tools.calendar.clockwise_tools import (
    ClockwiseHigherOrderTool,
)
from opus_deepwork_agent.custom_tools.todo.todoist_tools import TodoistTools
from opus_deepwork_agent.deepwork_agent_builder import DeepWorkAgentBuilder
from opus_deepwork_agent.meta_tools.hackernews_meta_tool import HackerNewsMetaTool
from opus_agent_base.agent.agent_runner import AgentRunner
from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.prompt.instructions_manager import InstructionsManager
logger = logging.getLogger(__name__)


async def run_deepwork_agent():
    """Run DeepWork Agent using AgentRunner"""
    logger.info("🎯 Starting DeepWork Agent")

    # Build DeepWork Agent
    config_manager = ConfigManager()
    instructions_manager = InstructionsManager()
    deepwork_agent = (
        DeepWorkAgentBuilder(config_manager)
        .name("deepwork-agent")
        .set_system_prompt_keys(["opus_agent_instruction", "deepwork_agent_instruction"])
        .add_instructions_manager(instructions_manager)
        .add_model_manager()
        .instruction(
            "opus_agent_instruction", "prompts/agent/OPUS_AGENT_INSTRUCTIONS.md"
        )
        .instruction(
            "deepwork_agent_instruction", "prompts/agent/DEEPWORK_AGENT_INSTRUCTIONS.md"
        )
        .instruction(
            "hackernews_meta_tool_prompt", "prompts/tools/deepwork/HACKERNEWS_METATOOL_PROMPT.md"
        )
        .custom_tool(TodoistTools())
        .higher_order_tool(ClockwiseHigherOrderTool())
        .meta_tool(HackerNewsMetaTool(config_manager, instructions_manager))
        .build()
    )
    # Run DeepWork Agent
    agent_runner = AgentRunner(deepwork_agent)
    await agent_runner.run_agent()
