import logging

logger = logging.getLogger(__name__)


class InstructionsManager:
    """
    Manager for static instructions and prompts
    """

    def __init__(self):
        self.instructions = []
        self.initialize_instructions()

    def initialize_instructions(self):
        self.initialize_agent_instructions()
        logger.info("Instructions initialized")

    def get_all_instructions(self):
        return "\n".join(self.instructions)

    def initialize_agent_instructions(self):
        # Instructions
        agent_instructions = """
You are a specialised agent for improving the productivity of the user.
"""
        self.instructions.append(agent_instructions)