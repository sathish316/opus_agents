from dataclasses import dataclass

from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.prompt.instructions_manager import InstructionsManager
from opus_agent_base.model.model_manager import ModelManager
from opus_agent_base.tools.mcp_manager import MCPManager
from opus_agent_base.tools.custom_tool import CustomTool
from opus_agent_base.tools.higher_order_tool import HigherOrderTool


@dataclass
class AgentDependencies:
    """
    Dependencies for the agent
    """
    config_manager: ConfigManager
    system_prompt_keys: list[str]
    instructions_manager: InstructionsManager
    model_manager: ModelManager
    mcp_manager: MCPManager
    custom_tools: list[CustomTool]
    higher_order_tools: list[HigherOrderTool]
