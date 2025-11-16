import logging

from opus_agent_base.agent.agent_runner import AgentRunner
from opus_agent_base.config.config_manager import ConfigManager

from opus_sde_agent.sde_agent_builder import SDEAgentBuilder

logger = logging.getLogger(__name__)

async def run_sde_agent():
    """Run SDE Agent using AgentRunner"""
    # build SDE Agent
    logger.info("💻 Starting SDE Agent")
    config_manager = ConfigManager()
    sde_agent = (
        SDEAgentBuilder(config_manager)
            .name("sde-agent")
            .set_system_prompt_keys(["opus_agent_instruction", "sde_agent_instruction"])
            .add_instructions_manager()
            .add_model_manager()
            .instruction(
                "opus_agent_instruction", "prompts/agent/OPUS_AGENT_INSTRUCTIONS.md"
            )
            .instruction(
                "sde_agent_instruction", "prompts/agent/SDE_AGENT_INSTRUCTIONS.md"
            )
            .build()
    )

    # run SDE Agent
    agent_runner = AgentRunner(sde_agent)
    await agent_runner.run_agent()
