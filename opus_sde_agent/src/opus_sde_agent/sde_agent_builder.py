from opus_agent_base.agent.agent_runner import AgentInstance
from opus_agent_base.tools.custom_tool import CustomTool
from opus_agent_base.tools.higher_order_tool import HigherOrderTool
from opus_agent_base.tools.mcp_server_registry import MCPServerRegistry
from opus_sde_agent.higher_order_tools.project_management.github_issues_tools import (
    GithubIssuesHigherOrderTool,
)
from opus_sde_agent.sde_mcp_server_registry import SDEMCPServerRegistry


class SDEAgentBuilder:
    def __init__(
        self, config_manager, instructions_manager, model_manager, mcp_manager
    ):
        self.name = "sde-agent"
        self.agent_instruction_keys = [
            "opus_agent_instruction",
            "sde_agent_instruction",
        ]
        self.config_manager = config_manager
        self.instructions_manager = instructions_manager
        self.model_manager = model_manager
        self.mcp_manager = mcp_manager
        self.custom_tools: list[CustomTool] = []
        self.higher_order_tools: list[HigherOrderTool] = []

    def build(self) -> AgentInstance:
        """Build the sde agent"""
        self._add_instructions()
        self._add_prompt_templates()
        self._add_mcp_servers()
        self._add_fastmcp_servers()
        self._add_custom_tools()
        self._add_higher_order_tools()

    def _add_instructions(self):
        self.instructions_manager.put_from_file(
            "opus_agent_instruction", "prompts/agent/OPUS_AGENT_INSTRUCTIONS.md"
        )
        self.instructions_manager.put_from_file(
            "sde_agent_instruction", "prompts/agent/SDE_AGENT_INSTRUCTIONS.md"
        )
        self.instructions_manager.put_from_file(
            "acceptance_criteria_for_github_issue_from_code", "prompt_templates/tools/sde/ACCEPTANCE_CRITERIA_FOR_GITHUB_ISSUE_FROM_CODE.md"
        )
        self.instructions_manager.put_from_file(
            "github_issues_assistant_instructions", "prompts/tools/sde/GITHUB_ISSUES_ASSISTANT_INSTRUCTIONS.md"
        )

    def _add_prompt_templates(self):
        pass

    def _add_mcp_servers(self):
        mcp_server_registry = MCPServerRegistry()
        sde_mcp_server_registry = SDEMCPServerRegistry(self.config_manager)
        mcp_servers_config = [
            mcp_server_registry.get_filesystem_mcp_server(),
            mcp_server_registry.get_search_mcp_server(),
            mcp_server_registry.get_code_execution_mcp_server(),
        ]
        mcp_servers_config = [config for config in mcp_servers_config if config is not None]
        self.mcp_manager.add_servers(mcp_servers_config)

    def _add_fastmcp_servers(self):
        mcp_server_registry = MCPServerRegistry()
        sde_mcp_server_registry = SDEMCPServerRegistry(self.config_manager)
        fastmcp_servers_config = [
            mcp_server_registry.get_datetime_mcp_server(),
            # code
            sde_mcp_server_registry.get_github_fastmcp_server(),
            # containers
            sde_mcp_server_registry.get_docker_fastmcp_server(),
            sde_mcp_server_registry.get_k8s_fastmcp_server(),
            # project management
            sde_mcp_server_registry.get_jira_fastmcp_server(),
            sde_mcp_server_registry.get_linear_fastmcp_server(),
            # observability
            sde_mcp_server_registry.get_prometheus_fastmcp_server(),
            sde_mcp_server_registry.get_loki_fastmcp_server(),
            sde_mcp_server_registry.get_grafana_fastmcp_server(),
            sde_mcp_server_registry.get_grafana_tempo_fastmcp_server(),
        ]
        fastmcp_servers_config = [config for config in fastmcp_servers_config if config is not None]
        self.mcp_manager.add_fastmcp_servers(fastmcp_servers_config)

    def _add_custom_tools(self):
        self.custom_tools: list[CustomTool] = []

    def _add_higher_order_tools(self):
        self.higher_order_tools: list[HigherOrderTool] = [
            GithubIssuesHigherOrderTool(
                config_manager=self.config_manager,
                instructions_manager=self.instructions_manager,
                model_manager=self.model_manager,
            ),
        ]

