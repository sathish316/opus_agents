import logging

from pydantic_ai import RunContext

from opus_agent_base.tools.custom_tool import CustomTool
from opus_todo_agent.custom_tools.notes.obsidian_rag import ObsidianRAG
from opus_agent_base.common.logging_config import console_log

logger = logging.getLogger(__name__)

class ObsidianTools(CustomTool):
    """
    Tools for obsidian
    """

    def __init__(self, config_manager=None, instructions_manager=None, model_manager=None):
        super().__init__("obsidian", "productivity.notes.obsidian", config_manager, instructions_manager, model_manager)
        vault_name = self.config_manager.get_setting("notes.obsidian.default_vault_name")
        self.obsidian_rag = ObsidianRAG(config_manager, vault_name, self.instructions_manager, self.model_manager)

    def initialize_tools(self, agent):
        @agent.tool
        def ask_notes(
            ctx: RunContext[str], query: str
        ) -> str:
            """
            Ask notes from obsidian.

            If the user asks a question to their notes, use this tool to retrieve the notes, summarize and answer the question.
            If the user prefixes the question with "Ask my notes" or "Search my notes", use this tool.
            """
            try:
                logger.info(f"[CustomToolCall] Asking notes for query: {query}")
                console_log(f"[CustomToolCall] Asking notes for query: {query}")
                response = self.obsidian_rag.ask_notes(query)
                logger.info(f"[CustomToolCall] Received response from model: {len(response)} chars")
                return response
            except Exception as e:
                logger.error(f"Error asking notes: {e}", exc_info=True)
                import traceback
                logger.error(traceback.format_exc())
                return f"Error retrieving notes: {str(e)}"

