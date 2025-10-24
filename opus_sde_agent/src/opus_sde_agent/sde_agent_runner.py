from opus_agent_base.agent.agent_runner import AgentRunner
from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.model.model_manager import ModelManager
from opus_agent_base.prompt.instructions_manager import InstructionsManager
from opus_agent_base.tools.mcp_manager import MCPManager
from opus_sde_agent.sde_agent_builder import SDEAgentBuilder

import logging

logger = logging.getLogger(__name__)

async def run_sde_agent():
    """Run SDE Agent using AgentRunner"""
    # build SDE Agent
    logger.info("💻 Starting SDE Agent")
    config_manager = ConfigManager()
    instructions_manager = InstructionsManager()
    model_manager = ModelManager(config_manager)
    mcp_manager = MCPManager(config_manager)
    sde_agent_builder = SDEAgentBuilder(
        config_manager=config_manager,
        instructions_manager=instructions_manager,
        model_manager=model_manager,
        mcp_manager=mcp_manager,
    )
    sde_agent_builder.build()

    # run SDE Agent
    agent_runner = AgentRunner(
        name=sde_agent_builder.name,
        config_manager=config_manager,
        instructions_manager=instructions_manager,
        agent_instruction_keys=sde_agent_builder.agent_instruction_keys,
        mcp_manager=mcp_manager,
        custom_tools=sde_agent_builder.custom_tools,
        higher_order_tools=sde_agent_builder.higher_order_tools,
    )   
    await agent_runner.run_agent()
