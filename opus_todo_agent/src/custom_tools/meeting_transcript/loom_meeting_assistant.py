import logging
import os

from pydantic_ai import Agent

from opus_todo_agent.helper.meeting_transcript.meeting_assistant_helper import (
    MeetingAssistantHelper,
)

logger = logging.getLogger(__name__)


class LoomMeetingAssistant:
    """
    Assistant for loom meeting transcripts
    """

    LOOM_TRANSCRIPT_FILE_EXTENSION = "srt"

    def __init__(self, config_manager=None, instructions_manager=None, model_manager=None):
        self.config_manager = config_manager
        self.loom_storage_dir = config_manager.get_setting(
            "meeting_transcript.loom.storage_dir"
        )
        self.instructions_manager = instructions_manager
        self.model_manager = model_manager
        self.meeting_assistant_helper = MeetingAssistantHelper()
        self._init_agent()

    def _init_agent(self):
        if self.config_manager.get_setting(
            "meeting_transcript.loom.use_local_model", False
        ):
            model = self.model_manager.get_local_model()
        else:
            model = self.model_manager.get_model()
        self.agent = Agent(
            instructions=self.instructions_manager.get("loom_meeting_assistant_instructions"),
            model=model,
        )

    def ask_loom_transcript(self, meeting_id: str, query: str) -> str:
        logger.info(
            f"Calling SubAgent to Ask question about meeting transcript: {query} for meeting id: {meeting_id}"
        )
        transcript_file = os.path.join(
            self.loom_storage_dir,
            f"{meeting_id}.{LoomMeetingAssistant.LOOM_TRANSCRIPT_FILE_EXTENSION}",
        )
        transcript = self.meeting_assistant_helper.read_transcript_from_file(
            transcript_file
        )
        # check if transcript is empty
        if not transcript:
            logger.error("No transcript found for the meeting - {meeting_id}")
            return ""
        # check if transcript is too large
        max_size = self.config_manager.get_setting(
            "meeting_transcript.loom.max_transcript_size", 0
        )
        transcript = self.meeting_assistant_helper.preprocess_transcript(
            transcript, max_size
        )
        # generate context for the agent
        prompt_template = self.instructions_manager.get("loom_meeting_assistant_prompt_template")
        response = self.meeting_assistant_helper.ask_transcript(
            self.agent, prompt_template, transcript, query
        )
        return response
