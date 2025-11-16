import logging

from opus_agent_base.agent.agent_runner import AgentRunner
from opus_agent_base.config.config_manager import ConfigManager

from opus_todo_agent.todo_agent_builder import TodoAgentBuilder

logger = logging.getLogger(__name__)

async def run_todo_agent():
    """Run Todo Agent using AgentRunner"""
    # build Todo Agent
    logger.info("📝 Starting Todo Agent")
    config_manager = ConfigManager()
    todo_agent = (
        TodoAgentBuilder(config_manager)
            .name("todo-agent")
            .set_system_prompt_keys(["opus_agent_instruction", "todo_agent_instruction"])
            .add_instructions_manager()
            .add_model_manager()
            .instruction(
                "opus_agent_instruction", "prompts/agent/OPUS_AGENT_INSTRUCTIONS.md"
            )
            .instruction(
                "todo_agent_instruction", "prompts/agent/TODO_AGENT_INSTRUCTIONS.md"
            )
            .build()
    )

    # run Todo Agent
    agent_runner = AgentRunner(todo_agent)
    await agent_runner.run_agent()
