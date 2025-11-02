import logging

logger = logging.getLogger(__name__)


class InstructionsManager:
    """
    Manager for system prompts, instruction prompts and prompt templates
    """

    def __init__(self):
        self.instructions = {}

    def get(self, key: str):
        """
        Get an instruction by key

        Args:
            key: The key to retrieve

        Returns:
            The instruction value or error if not found
        """
        if key not in self.instructions:
            raise KeyError(f"Instruction {key} not found")
        return self.instructions[key]

    def put(self, key: str, value):
        """
        Put an instruction with a key

        Args:
            key: The key to store the instruction under
            value: The instruction value to store
        """
        self.instructions[key] = value
        logger.info(f"Instruction {key} added")

    def put_from_file(self, key: str, file: str):
        """
        Put an instruction from a file

        Args:
            key: The key to store the instruction under
            file: Path to the file containing the instruction
        """
        self.put(key, self.load(file))

    def load(self, file_path: str) -> str:
        """
        Read content from a file

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