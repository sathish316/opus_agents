import logging

from pydantic_ai import RunContext

from opus_todo_agent.custom_tools.meeting_transcript.zoom_meeting_assistant import (
    ZoomMeetingAssistant,
)

logger = logging.getLogger(__name__)


class ZoomTools:
    """
    Tools for Zoom meeting transcripts
    """

    def __init__(self, config_manager, instructions_manager, model_manager):
        self.zoom_assistant = ZoomMeetingAssistant(
            config_manager, instructions_manager, model_manager
        )

    def initialize_tools(self, agent):
        @agent.tool
        def ask_zoom_meeting_transcript(
            ctx: RunContext[str], meeting_id: str, query: str
        ) -> str:
            """
            Ask follow-up questions to zoom meeting transcript.

            If the user asks a question about a zoom meeting id, use this tool to retrieve meeting transcript and answer the question.
            If the user prefixes the question with "Ask zoom meeting transcript" or "Ask zoom meeting", then use this tool.
            """
            logger.info(f"[CustomToolCall] Ask follow-up questions to zoom meeting transcript: {query} for meeting id: {meeting_id}")
            response = self.zoom_assistant.ask_zoom_transcript(meeting_id, query)
            logger.info(f"[CustomToolCall] Received response from model: {len(response)} chars")
            return response
