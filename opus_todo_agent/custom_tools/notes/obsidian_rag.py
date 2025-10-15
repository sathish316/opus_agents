import chromadb
from pydantic_ai import Agent
import logging
from pydantic_ai import RunContext

logger = logging.getLogger(__name__)


class ObsidianRAG:
    """
    RAG for obsidian notes
    """

    NOTES_RAG_PROMPT_TEMPLATE = """
Answer the question based only on the following context:
{context}
 - -
Answer the question based on the above context:
{question}
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
        print(f"Vault config: {self.vault_config}")
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
            instructions=self.instructions_manager.get_obsidian_rag_instructions(),
            model=self.model_manager.get_model(),
        )

    def retrieve_notes(self, query: str) -> str:
        results = self.collection.query(
            query_texts=[query],
            n_results=self.vault_config.get("num_results", 3),
        )

        # print search results
        for i, query_results in enumerate(results["documents"]):
            print(f"\nQuery {i+1}")
            print("\n".join(query_results))
        return "\n----------\n".join(query_results)

    def ask_notes(self, query: str) -> str:
        logger.info(f"Calling SubAgent to Ask question about notes: {query}")
        notes = self.retrieve_notes(query)
        logger.info(f"Retrieved notes: {len(notes)} chars")
        if not notes:
            logger.error("No notes found for the query")
            return ""
        prompt = ObsidianRAG.NOTES_RAG_PROMPT_TEMPLATE.format(
            context=notes, question=query
        )
        response = self.agent.run_sync(prompt)
        return response.output
