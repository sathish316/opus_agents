import logging

from pydantic_ai import Agent

from opus_todo_agent.helper.chat.slack_helper import SlackHelper

logger = logging.getLogger(__name__)


class SlackAssistant:
    """
    Assistant for Slack message summarization
    """

    def __init__(self, config_manager, instructions_manager, model_manager):
        self.config_manager = config_manager
        self.instructions_manager = instructions_manager
        self.model_manager = model_manager
        self.slack_helper = SlackHelper()
        self._init_agent()

    def _init_agent(self):
        if self.config_manager.get_setting("chat.slack.use_local_model", False):
            model = self.model_manager.get_local_model()
        else:
            model = self.model_manager.get_model()
        self.agent = Agent(
            instructions=self.instructions_manager.get("slack_assistant_instructions"),
            model=model,
        )

    async def fetch_and_summarize_messages_from_channels(
        self,
        fastmcp_client_context,
        channel_scope_type,
        channel_scope_name,
        time_limit,
    ) -> str:
        """
        Fetch and summarize Slack messages from given channels.

        Args:
            fastmcp_client_context: MCP client context for tool calls
            channel_ids: List of Slack channel IDs
            channels: List of channel names
            channel_scope_type: Type of scope (team/project/channel)
            channel_scope_name: Name of the team/project or channel
            time_limit: Time period for conversation history (e.g., "1d", "1w", "5d", "4w")

        Returns:
            Summarized messages grouped by channel
        """
        logger.info(
            f"Calling SubAgent to summarize Slack messages for {channel_scope_type}: {channel_scope_name}, time_limit: {time_limit}"
        )
        # resolve channel scope and name to channel ids
        if channel_scope_type == "team":
            channels = self.slack_helper.get_channels_for_team(
                self.config_manager, channel_scope_name
            )
        elif channel_scope_type == "project":
            channels = self.slack_helper.get_channels_for_project(
                self.config_manager, channel_scope_name
            )
        elif channel_scope_type == "channel":
            channels = [channel_scope_name]
        else:
            raise ValueError(
                f"Invalid channel scope type: {channel_scope_type}"
            )

        channel_ids = self.slack_helper.get_channel_ids(channels)
        logging.info(
            f"[SubAgent] Fetched channels for {channel_scope_type} : {channel_scope_name} as #{channels} with ids: {channel_ids}"
        )

        # Fetch conversation history
        conversation_history = (
            await self.slack_helper.get_conversation_history_for_channels(
                fastmcp_client_context, channel_ids, time_limit
            )
        )

        if not conversation_history:
            logger.error(f"No conversation history found for channels: {channels}")
            return ""

        logger.info(
            f"Retrieved conversation history: {len(str(conversation_history))} chars"
        )

        # FIXME: if conversation history is too large, summarize per channel and truncate it if required

        # Build channel ID to name mapping for the specific channels
        channel_mapping = "\n".join(
            [
                f"{channel_id}: {channel_name}"
                for channel_id, channel_name in zip(channel_ids, channels, strict=False)
            ]
        )

        # Generate prompt
        prompt_template = self.instructions_manager.get("slack_assistant_prompt_template")
        prompt = prompt_template.format(
            channel_scope_type=channel_scope_type,
            channel_scope_name=channel_scope_name,
            time_limit=time_limit,
            conversation_history=str(conversation_history),
            channel_id_to_name_mapping=channel_mapping,
        )

        # Call agent to summarize
        logger.debug(f"Calling SubAgent with prompt: {prompt}")
        response = await self.agent.run(prompt)
        logger.info(f"Received summary from model: {len(response.output)} chars")
        return response.output