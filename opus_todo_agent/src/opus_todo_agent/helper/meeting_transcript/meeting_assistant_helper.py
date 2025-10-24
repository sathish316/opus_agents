import logging

import tiktoken
from pydantic_ai import Agent

logger = logging.getLogger(__name__)

class MeetingAssistantHelper:
    """
    Helper for meeting assistant.
    Common set of helper methods for zoom and loom meeting transcripts.
    """

    def __init__(self):
        pass

    def read_transcript_from_file(self, transcript_path: str) -> str:
        with open(transcript_path, "r") as f:
            transcript = f.read()
        return transcript

    def preprocess_transcript(self, transcript: str, max_size: int) -> str:
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(transcript)
        logger.info(f"Retrieved transcript: {len(transcript)} chars, {len(tokens)} tokens")
        if max_size > 0:
            # Truncate by tokens
            if len(tokens) > max_size:
                truncated_tokens = tokens[:max_size]
                transcript = encoding.decode(truncated_tokens)
                logger.info(f"Truncated transcript: {len(transcript)} chars, {len(truncated_tokens)} tokens")
        return transcript

    def ask_transcript(self, agent: Agent, prompt_template: str, transcript: str, query: str) -> str:
        prompt = prompt_template.format(context=transcript, question=query)
        response = agent.run_sync(prompt)
        return response.output