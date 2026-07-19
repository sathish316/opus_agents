import logging
import os

from opus_agent_base.tools.subagent_as_tool import SubagentAsTool
from opus_todo_agent.helper.meeting_transcript.meeting_assistant_helper import (
    MeetingAssistantHelper,
)

logger = logging.getLogger(__name__)


class ZoomMeetingAssistant:
    """
    Assistant for zoom meeting transcripts
    """

    ZOOM_TRANSCRIPT_FILE_EXTENSION = "vtt"

    def __init__(self, config_manager, instructions_manager, model_manager):
        self.config_manager = config_manager
        self.zoom_storage_dir = config_manager.get_setting(
            "meeting_transcript.zoom.storage_dir"
        )
        self.instructions_manager = instructions_manager
        self.model_manager = model_manager
        self.meeting_assistant_helper = MeetingAssistantHelper()
        self.subagent = SubagentAsTool.from_managers(
            name="zoom_meeting_assistant",
            instructions_key="zoom_meeting_assistant_instructions",
            config_manager=config_manager,
            instructions_manager=instructions_manager,
            model_manager=model_manager,
            use_local_model_config_key="meeting_transcript.zoom.use_local_model",
        )

    def ask_zoom_transcript(self, meeting_id: str, query: str) -> str:
        logger.info(
            f"Calling SubAgent to Ask question about meeting "
            f"transcript: {query} for meeting id: {meeting_id}"
        )
        transcript_file = os.path.join(
            self.zoom_storage_dir,
            f"{meeting_id}.{ZoomMeetingAssistant.ZOOM_TRANSCRIPT_FILE_EXTENSION}",
        )
        transcript = self.meeting_assistant_helper.read_transcript_from_file(
            transcript_file
        )
        # check if transcript is empty
        if not transcript:
            logger.error("No transcript found for the meeting - {meeting_id}")
            return ""
        logger.info(f"Retrieved transcript: {len(transcript)} chars")
        # check if transcript is too large
        max_size = self.config_manager.get_setting(
            "meeting_transcript.zoom.max_transcript_size", 0
        )
        transcript = self.meeting_assistant_helper.preprocess_transcript(
            transcript, max_size
        )
        # generate context for the agent
        prompt_template = self.instructions_manager.get(
            "zoom_meeting_assistant_prompt_template"
        )
        prompt = SubagentAsTool.format_prompt(
            prompt_template, context=transcript, question=query
        )
        return self.subagent.run_sync(prompt)
