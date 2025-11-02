from opus_agent_base.agent.agent_runner import AgentRunner
from opus_agent_base.agent.agent_dependencies import AgentDependencies
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
    agent_deps = AgentDependencies(
        config_manager=config_manager,
        system_prompt_keys=sde_agent_builder.system_prompt_keys,
        instructions_manager=instructions_manager,
        model_manager=model_manager,
        mcp_manager=mcp_manager,
        custom_tools=sde_agent_builder.custom_tools,
        higher_order_tools=sde_agent_builder.higher_order_tools,
    )
    agent_runner = AgentRunner(name=sde_agent_builder.name, agent_deps=agent_deps)
    await agent_runner.run_agent()
