import logging

logger = logging.getLogger(__name__)


class InstructionsManager:
    """
    Manager for system prompts
    Supports both root system prompt and agent-specific system prompts
    """

    def __init__(self):
        self.system_prompts = {}
        self.root_system_prompt = None

    def get(self, key: str):
        """
        Get a system prompt by key

        Args:
            key: The key to retrieve

        Returns:
            The system prompt value or error if not found
        """
        if key not in self.system_prompts:
            raise KeyError(f"System prompt {key} not found")
        return self.system_prompts[key]

    def put(self, key: str, value):
        """
        Put a system prompt with a key

        Args:
            key: The key to store the system prompt under
            value: The system prompt value to store
        """
        self.system_prompts[key] = value
        logger.info(f"System prompt {key} added")

    def put_from_file(self, key: str, file: str):
        """
        Put a system prompt from a file

        Args:
            key: The key to store the system prompt under
            file: Path to the file containing the system prompt
        """
        self.put(key, self.load(file))

    def load(self, file_path: str) -> str:
        """
        Read system prompt from a file

        Args:
            file_path: Path to the file to read

        Returns:
            The contents of the file as a string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise

    def set_root_system_prompt(self, value: str):
        """
        Set the root system prompt for the agent

        Args:
            value: The root system prompt value to store
        """
        self.root_system_prompt = value
        logger.info("Root system prompt set for agent")

    def set_root_system_prompt_from_file(self, file: str):
        """
        Set the root system prompt from a file

        Args:
            file: Path to the file containing the root system prompt
        """
        self.set_root_system_prompt(self.load(file))

    def get_root_system_prompt(self) -> str:
        """
        Get the root system prompt for the agent

        Returns:
            The root system prompt value or empty string if not set
        """
        if self.root_system_prompt is None:
            logger.warning("Root system prompt not set, returning empty string")
            return ""
        return self.root_system_prompt