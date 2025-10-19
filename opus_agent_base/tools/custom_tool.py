import logging
from abc import abstractmethod

logger = logging.getLogger(__name__)


class CustomTool:
    """
    Base class for Custom tools that can be added to the agent
    """

    def __init__(self, name:str, config_key:str, config_manager=None, instructions_manager=None, model_manager=None):
        self.name = name
        self.config_key = config_key
        self.config_manager = config_manager
        self.instructions_manager = instructions_manager
        self.model_manager = model_manager

    @abstractmethod
    def initialize_tools(self, agent):
        """
        Register tools with the agent.
        Must be implemented by subclasses.

        Args:
            agent: The agent instance to register tools with
        """
        raise NotImplementedError("Subclasses must implement this method")
