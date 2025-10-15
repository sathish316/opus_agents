import json
import logging
import os

from rapidfuzz import fuzz, process

from opus_todo_agent.helper.fastmcp_client_helper import FastMCPClientHelper

logger = logging.getLogger(__name__)


class SlackHelper:
    """
    Helper for Slack
    """

    def __init__(self):
        self.fastmcp_client_helper = FastMCPClientHelper()

    def get_channels_for_team(self, config_manager, team_name):
        team_to_channels = config_manager.get_setting("chat.slack.team_to_channels")
        if team_to_channels:
            # exact match team name
            if team_name in team_to_channels:
                return team_to_channels.get(team_name, [])
            # fuzzy match team name
            best_match = process.extractOne(team_name, team_to_channels.keys())
            if best_match:
                (key, _, _) = best_match
                return team_to_channels.get(key, [])
            # error message if no match
            logger.error(
                f"No match found for team name: {team_name}. Please check if team to channels is configured in config file"
            )
        return []

    def get_channels_for_project(self, config_manager, project_name):
        project_to_channels = config_manager.get_setting(
            "chat.slack.project_to_channels"
        )
        if project_to_channels:
            # exact match project name
            if project_name in project_to_channels:
                return project_to_channels.get(project_name, [])
            # fuzzy match team name
            best_match = process.extractOne(project_name, project_to_channels.keys())
            if best_match:
                (key, _, _) = best_match
                return project_to_channels.get(key, [])
            # error message if no match
            logger.error(
                f"No match found for project name: {project_name}. Please check if project to channels is configured in config file"
            )
        return []

    def get_channel_id(self, channel_name):
        # exact match channel name
        cached_channels_list = self._get_cached_channels_list()
        cached_channel_info = next(
            (item for item in cached_channels_list if item["name"] == channel_name),
            None,
        )
        if cached_channel_info:
            return cached_channel_info.get("id")
        # fuzzy match channel name
        best_match_id = None
        best_match_score = 0.0
        for channel_info in cached_channels_list:
            score = fuzz.WRatio(channel_name, channel_info["name"])
            if score > best_match_score:
                best_match_score = score
                best_match_id = channel_info.get("id")
        if best_match_id:
            return best_match_id
        # error message if no match
        logger.error(
            f"No match found for channel name: {channel_name}. Please check if channels are upto-date in channels json file"
        )
        return None

    def get_channel_ids(self, channel_names: list[str]):
        return [self.get_channel_id(channel_name) for channel_name in channel_names]

    def _get_cached_channels_list(self):
        # read channels name from the file .channels_cache.json in same directory
        channel_cache_files = [".channels_cache_v2.json", ".channels_cache.json"]
        channel_cache_file = next(
            (
                cache_file
                for cache_file in channel_cache_files
                if os.path.exists(cache_file)
            ),
            None,
        )
        if channel_cache_file:
            cached_channels_list = json.load(open(channel_cache_file))
            return cached_channels_list
        else:
            logger.error("Channels json not found")
            return []

    def get_channel_id_to_name_mapping(self):
        # read channels name from the file .channels_cache.json in same directory
        cached_channels_list = self._get_cached_channels_list()
        return {item["id"]: item["name"] for item in cached_channels_list}

    async def get_conversation_history_for_channels(
        self, fastmcp_client_context, channel_ids, time_limit
    ):
        """
        Get slack conversation history for a given channel and time period

        Args:
            channel_ids: List of slack channel ids
            time_limit: Time period for the conversation history

        Returns:
            List of slack conversation history for the given channels and time period

        """
        logger.info(
            f"[Tool call] Fetching Slack Conversation History for channels: {channel_ids} and time period: {time_limit}"
        )
        all_results = []
        mcp_tool_name = "slack_conversations_history"
        for channel_id in channel_ids:
            # FIXME: if pagination is required, fetch the next page and append to conversation history
            channel_result = await self.fastmcp_client_helper.call_fastmcp_tool(
                fastmcp_client_context,
                mcp_tool_name,
                {"channel_id": channel_id, "limit": time_limit},
                parse_json=False,
            )
            logger.debug(f"Channel result: {channel_result}")
            all_results.append(channel_result)
        return all_results
