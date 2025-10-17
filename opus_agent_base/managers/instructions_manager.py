import logging

logger = logging.getLogger(__name__)


class InstructionsManager:
    """
    Base Manager for static instructions and prompts.
    
    This class can be extended to provide domain-specific instructions.
    """

    def __init__(self):
        self.instructions = []
        self.initialize_instructions()

    def initialize_instructions(self):
        """Initialize base instructions. Override this method in subclasses to add domain-specific instructions."""
        logger.info("Instructions initialized")

    def get_all_instructions(self):
        return "\n".join(self.instructions)

    def get_obsidian_rag_instructions(self):
        obsidian_rag_instructions = """
You are a specialised agent for searching notes and answering questions based on the notes.

## Guidelines:
1. Use the tools provided to you to search notes and answer questions
2. Don't use any extraneous knowledge or information that is not in the notes or given to you as context
"""
        return obsidian_rag_instructions

    def get_loom_meeting_assistant_instructions(self):
        loom_meeting_assistant_instructions = """
You are a specialised agent for answering questions based on meeting transcript.

## Guidelines:
1. Use the tools provided to you to answer questions based on the meeting transcript
2. Don't use any extraneous knowledge or information that is not in the meeting transcript or given to you as context
"""
        return loom_meeting_assistant_instructions

    def get_zoom_meeting_assistant_instructions(self):
        zoom_meeting_assistant_instructions = """
You are a specialised agent for answering questions based on meeting transcript.

## Guidelines:
1. Use the tools provided to you to answer questions based on the meeting transcript
2. Don't use any extraneous knowledge or information that is not in the meeting transcript or given to you as context
"""
        return zoom_meeting_assistant_instructions

    def get_slack_assistant_instructions(self):
        slack_assistant_instructions = """
You are a specialised agent for summarizing Slack channel conversations.

## Guidelines:
1. Summarize messages grouped by channel name
2. Highlight key discussions, decisions, and action items
3. Use only information from the provided conversation history
4. Keep summaries concise but informative
5. Convert channel IDs to channel names when possible
"""
        return slack_assistant_instructions
