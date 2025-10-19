import logging

from pydantic_ai import RunContext

from opus_agent_base.tools.custom_tool import CustomTool
from opus_todo_agent.custom_tools.meeting_transcript.loom_meeting_assistant import (
    LoomMeetingAssistant,
)

logger = logging.getLogger(__name__)

class LoomTools(CustomTool):
    """
    Tools for Loom meeting transcripts
    """

    def __init__(self, config_manager=None, instructions_manager=None, model_manager=None):
        super().__init__("loom", "productivity.meeting_transcript.loom", config_manager, instructions_manager, model_manager)
        self.loom_assistant = LoomMeetingAssistant(self.config_manager, self.instructions_manager, self.model_manager)

    def initialize_tools(self, agent):
        @agent.tool
        def ask_loom_meeting_transcript(
            ctx: RunContext[str], meeting_id: str, query: str
        ) -> str:
            """
            Ask follow-up questions to loom meeting transcript.

            If the user asks a question about a loom meeting id, use this tool to retrieve meeting transcript and answer the question.
            If the user prefixes the question with "Ask loom meeting transcript" or "Ask loom meeting", then use this tool.
            """
            logger.info(f"[CustomToolCall] Ask follow-up questions to loom meeting transcript: {query} for meeting id: {meeting_id}")
            response = self.loom_assistant.ask_loom_transcript(meeting_id, query)
            logger.info(f"[CustomToolCall] Received response from model: {len(response)} chars")
            return response

