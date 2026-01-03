from typing import Any

from pydantic_ai import Agent

from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.model.model_manager import ModelManager
from opus_agent_base.prompt.instructions_manager import InstructionsManager
from opus_agent_base.tools.custom_tool import CustomTool
from opus_agent_base.tools.custom_tools_manager import CustomToolsManager
from opus_agent_base.tools.fastmcp_server_config import FastMCPServerConfig
from opus_agent_base.tools.higher_order_tool import HigherOrderTool
from opus_agent_base.tools.meta_tool import MetaTool


class AgentBuilder:
    """Builder for the agent"""

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.custom_tools: list[CustomTool] = []
        self.higher_order_tools: list[HigherOrderTool] = []
        self.meta_tools: list[MetaTool] = []
        self.mcp_servers_config: list[FastMCPServerConfig] = []

    def name(self, name: str):
        self.name = name
        return self

    def set_system_prompt_keys(self, system_prompt_keys: list[str]):
        self.system_prompt_keys = system_prompt_keys
        return self

    def add_instructions_manager(
        self, instructions_manager: InstructionsManager = None
    ):
        if instructions_manager is not None:
            self.instructions_manager = instructions_manager
        else:
            self.instructions_manager = InstructionsManager()
        return self

    def instruction(self, key: str, file: str):
        self.instructions_manager.put_from_file(key, file)
        return self

    def add_model_manager(self):
        self.model_manager = ModelManager(self.config_manager)
        return self

    def custom_tool(self, custom_tool: CustomTool):
        self.custom_tools.append(custom_tool)
        return self

    def higher_order_tool(self, higher_order_tool: HigherOrderTool):
        self.higher_order_tools.append(higher_order_tool)
        return self

    def meta_tool(self, meta_tool: MetaTool):
        self.meta_tools.append(meta_tool)
        return self

    def add_mcp_server_config(self, mcp_server_config: FastMCPServerConfig):
        self.mcp_servers_config.append(mcp_server_config)
        return self

    def add_mcp_servers_config(self, mcp_servers_config: list[FastMCPServerConfig]):
        self.mcp_servers_config.extend(mcp_servers_config)
        return self

    def set_deps_type(self, deps_type: Any):
        self.deps_type = deps_type
        return self

    def set_output_type(self, output_type: Any):
        self.output_type = output_type
        return self

    def build_agent(self) -> Agent:
        agent = self.build_simple_agent()
        custom_tools_manager = CustomToolsManager(
            self.config_manager,
            self.instructions_manager,
            self.model_manager,
            agent,
        )
        custom_tools_manager.initialize_tools(self.custom_tools)
        return agent

    def build_simple_agent(self) -> Agent:
        system_prompt = "\n".join(
            self.instructions_manager.get(key) for key in self.system_prompt_keys
        )
        agent_kwargs = {
            "system_prompt": system_prompt,
            "model": self.model_manager.get_model(),
            "tools": [],
        }

        # Add deps_type if set
        if hasattr(self, "deps_type") and self.deps_type is not None:
            agent_kwargs["deps_type"] = self.deps_type

        # Add output_type if set
        if hasattr(self, "output_type") and self.output_type is not None:
            agent_kwargs["output_type"] = self.output_type

        return Agent(**agent_kwargs)
