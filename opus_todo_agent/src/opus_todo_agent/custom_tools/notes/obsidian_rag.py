import chromadb
from pydantic_ai import Agent
import logging

logger = logging.getLogger(__name__)

import os

# Disable tokenizers parallelism to avoid warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"


class ObsidianRAG:
    """
    RAG for obsidian notes
    """

    def __init__(
        self, config_manager, obsidian_vault_name, instructions_manager, model_manager
    ):
        self.config_manager = config_manager
        self.obsidian_vault_name = obsidian_vault_name
        self.instructions_manager = instructions_manager
        self.model_manager = model_manager
        vault_config_list = self.config_manager.get_setting(
            f"notes.obsidian.vault_configurations"
        )
        self.vault_config = next(
            (
                vault_config
                for vault_config in vault_config_list
                if vault_config.get("vault_name") == self.obsidian_vault_name
            ),
            None,
        )
        assert (
            self.vault_config is not None
        ), f"Vault config not found for {self.obsidian_vault_name}"
        logger.info(f"Vault config: {self.vault_config}")
        self._init_vector_db()
        self._init_agent()

    def _init_vector_db(self):
        vector_db_path = self.vault_config.get("vector_db_path")
        vector_db_collection = self.vault_config.get("vector_db_collection")
        # init chroma client
        self.client = chromadb.PersistentClient(path=vector_db_path)
        # init collection
        self.collection = self.client.get_or_create_collection(vector_db_collection)

    def _init_agent(self):
        self.agent = Agent(
            instructions=self.instructions_manager.get("obsidian_notes_instructions"),
            model=self.model_manager.get_model(),
        )

    def retrieve_notes(self, query: str) -> str:
        """
        Retrieve relevant notes from the vector database based on the query.

        Returns:
            A string containing all retrieved notes separated by '----------'
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=self.vault_config.get("num_results", 3),
        )

        if not results:
            logger.error(f"No notes found for the query: {query}")
            return "No notes found for the query"

        # ChromaDB returns documents as a list of lists: [[doc1, doc2, doc3]]
        # The outer list represents queries (we only have 1 query)
        # The inner list contains the matching documents
        documents_list = results["documents"]

        # Log search results for debugging
        for i, docs in enumerate(documents_list):
            logger.debug(f"\nQuery {i+1}")
            logger.debug(docs)

        # Extract documents from the nested list structure
        # Since we only pass one query, we get documents_list[0]
        retrieved_documents = documents_list[0] if documents_list else []

        # Join all documents with a separator
        return "\n----------\n".join(retrieved_documents)

    def ask_notes(self, query: str) -> str:
        logger.info(f"Calling SubAgent to Ask question about notes: {query}")
        notes = self.retrieve_notes(query)
        logger.info(f"Retrieved notes: {len(notes)} chars")
        if not notes:
            logger.error("No notes found for the query")
            return ""
        prompt_template = self.instructions_manager.get(
            "obsidian_notes_prompt_template"
        )
        prompt = prompt_template.format(context=notes, question=query)
        response = self.agent.run_sync(prompt)
        return response.output
