from opus_agent_base.agent.agent_runner import AgentRunner
from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.model.model_manager import ModelManager
from opus_agent_base.prompt.instructions_manager import InstructionsManager
from opus_agent_base.tools.mcp_manager import MCPManager
from opus_todo_agent.todo_agent_builder import TodoAgentBuilder

import logging

logger = logging.getLogger(__name__)

async def run_todo_agent():
    """Run Todo Agent using AgentRunner"""
    # build Todo Agent
    logger.info("📝 Starting Todo Agent")
    config_manager = ConfigManager()
    instructions_manager = InstructionsManager()
    model_manager = ModelManager(config_manager)
    mcp_manager = MCPManager(config_manager)
    todo_agent_builder = TodoAgentBuilder(
        config_manager=config_manager,
        instructions_manager=instructions_manager,
        model_manager=model_manager,
        mcp_manager=mcp_manager,
    )
    todo_agent_builder.build()

    # run Todo Agent
    agent_runner = AgentRunner(
        name=todo_agent_builder.name,
        config_manager=config_manager,
        instructions_manager=instructions_manager,
        agent_instruction_keys=todo_agent_builder.agent_instruction_keys,
        mcp_manager=mcp_manager,
        custom_tools=todo_agent_builder.custom_tools,
        higher_order_tools=todo_agent_builder.higher_order_tools,
    )
    await agent_runner.run_agent()
