import logging

from opus_agent_base.config.config_manager import ConfigManager
from opus_agent_base.common.datetime_helper import DatetimeHelper
from pydantic_ai import RunContext

from opus_agent_base.tools.higher_order_tool import HigherOrderTool
from opus_todo_agent.helper.chat.slack_helper import SlackHelper
from opus_todo_agent.higher_order_tools.chat.slack_assistant import SlackAssistant
from opus_agent_base.common.logging_config import console_log

logger = logging.getLogger(__name__)


class SlackHigherOrderTool(HigherOrderTool):
    """
    Slack tools on top of Slack MCP that can be added to the agent
    """
    def __init__(
        self,
        config_manager=None,
        instructions_manager=None,
        model_manager=None,
    ):
        super().__init__("slack", "productivity.chat.slack", config_manager, instructions_manager, model_manager)
        self.slack_helper = SlackHelper()
        self.datetime_helper = DatetimeHelper()
        self.slack_assistant = SlackAssistant(self.config_manager, self.instructions_manager, self.model_manager)

    async def initialize_tools(self, agent, fastmcp_client_context):
        @agent.tool
        async def get_slack_conversation_history_for_team_or_project(
            ctx: RunContext[str],
            channel_scope_type: str,
            team_name: str = "",
            project_name: str = "",
            channel_name: str = "",
            time_limit: str = "1d",
            summarize: bool = True,
        ) -> str:
            """
            Brief the user about Slack channel updates for a given team or project or individual slack channel

            Supported filters for channel_scope_type are:
            1. team
            2. project
            3. channel

            If the user asks to List recent messages for a project, pass the project name.
            If the user asks to brief them about a project's slack channels, pass the project name.

            If the user asks to list recent messages for a team, pass the team name.
            If the user asks to brief them about a team's slack channels, pass the team name.

            Supported filters for time_limit are:
            1. "1d" - representing one day of messages
            2. "1w" - representing one week of messages
            3. n days representing n days of messages - For example: "5d" representing 5 days of messages
            4. n weeks representing n weeks of messages - For example: "4w" representing 4 weeks of messages
            5. Default is "1d"

            Use this tool to retrieve Slack conversation history for a given channel scope and time period.
            This tool uses a SubAgent called SlackAssistant to fetch and summarize the conversation history.
            Return the output of this tool directly to the User without any modification.
            """
            try:
                logging.info(
                    f"[CustomToolCall] Fetching slack conversation history for channel_scope_type: {channel_scope_type}, team_name: {team_name}, project_name: {project_name}, channel_name: {channel_name}, time_limit: {time_limit}"
                )
                console_log(
                    f"[CustomToolCall] Fetching slack conversation history for channel_scope_type: {channel_scope_type}, team_name: {team_name}, project_name: {project_name}, channel_name: {channel_name}, time_limit: {time_limit}"
                )
                channel_scope_name = team_name or project_name or channel_name
                conversation_summary = await self.slack_assistant.fetch_and_summarize_messages_from_channels(
                    fastmcp_client_context,
                    channel_scope_type,
                    channel_scope_name,
                    time_limit,
                )
                return conversation_summary

            except Exception as e:
                import traceback

                logging.error(f"Stacktrace: {traceback.format_exc()}")
                logging.error(f"Error fetching slack conversation history: {e}")
                return

            return conversation_summary
