import hashlib
import chromadb
import uuid
import os
import logging
import sys
from opus_agent_base.config.config_manager import ConfigManager
import re

logger = logging.getLogger(__name__)


class ObsidianIndexer:
    """
    Index your obsidian notes into a vector database.
    Input: vault name and vault config. Vault config includes path to the vault and settings.
    """

    def __init__(self, config_manager, obsidian_vault_name):
        self.config_manager = config_manager
        self.obsidian_vault_name = obsidian_vault_name
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
        logging.info(f"Vault config: {self.vault_config}")
        self._init_vector_db()

    def _init_vector_db(self):
        vector_db_path = self.vault_config.get("vector_db_path")
        vector_db_collection = self.vault_config.get("vector_db_collection")
        # init chroma client
        self.client = chromadb.PersistentClient(path=vector_db_path)
        # init collection
        self.collection = self.client.get_or_create_collection(vector_db_collection)

    def create_index(self):
        obsidian_vault_path = self.vault_config.get("vault_path")
        exclude_dirs = [
            re.compile(pattern) for pattern in self.vault_config.get("exclude_dirs", [])
        ]
        # find all md files in the obsidian vault recursively
        md_files = []
        for root, dirs, files in os.walk(obsidian_vault_path):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    if any(
                        re.search(exclude_dir, file_path) != None
                        for exclude_dir in exclude_dirs
                    ):
                        continue
                    md_files.append(file_path)
        # read md files
        count = 0
        max_count = 1000
        for md_file_path in md_files:
            with open(md_file_path, "r", encoding="utf-8") as f:
                if count < max_count:
                    # add document to collection
                    logger.info(f"Adding note to vector_db collection: {md_file_path}")
                    doc_id = str(uuid.uuid4())
                    content = f.read()
                    metadata = {
                        "file_path": md_file_path,
                        "md5_hash": hashlib.md5(content.encode()).hexdigest(),
                    }
                    count += 1
                    self.collection.add(
                        ids=[doc_id],
                        documents=[content],
                        metadatas=[metadata],
                    )

    def update_index(self):
        obsidian_vault_path = self.vault_config.get("vault_path")
        exclude_dirs = [
            re.compile(pattern) for pattern in self.vault_config.get("exclude_dirs", [])
        ]
        # find all md files in the obsidian vault recursively
        md_files = []
        for root, dirs, files in os.walk(obsidian_vault_path):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    if any(
                        re.search(exclude_dir, file_path) != None
                        for exclude_dir in exclude_dirs
                    ):
                        continue
                    md_files.append(file_path)
        # read md files
        count = 0
        max_count = 1000
        for md_file_path in md_files:
            with open(md_file_path, "r", encoding="utf-8") as f:
                if count < max_count:
                    # add or update document to collection
                    logger.info(f"Indexing create/update/nop: {md_file_path}")
                    doc_id = str(uuid.uuid4())
                    content = f.read()
                    metadata = {
                        "file_path": md_file_path,
                        "md5_hash": hashlib.md5(content.encode()).hexdigest(),
                    }
                    count += 1
                    # Check if document already exists by file_path
                    existing_docs = self.collection.get(
                        where={"file_path": md_file_path}
                    )
                    if existing_docs["ids"]:
                        # Document exists, check if content has changed
                        existing_metadata = existing_docs["metadatas"][0]
                        existing_hash = existing_metadata.get("md5_hash")

                        if existing_hash == metadata["md5_hash"]:
                            # Content unchanged, skip
                            logger.info(f"Skipping unchanged note: {md_file_path}")
                        else:
                            # Content changed, update existing document
                            logger.info(f"Updating changed note: {md_file_path}")
                            existing_id = existing_docs["ids"][0]
                            self.collection.upsert(
                                ids=[existing_id],
                                documents=[content],
                                metadatas=[metadata],
                            )
                    else:
                        # Document does not exist, add new document
                        logger.info(f"Adding new note: {md_file_path}")
                        self.collection.add(
                            ids=[doc_id],
                            documents=[content],
                            metadatas=[metadata],
                        )


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python obsidian_indexer.py <vault_name>")
        sys.exit(1)

    vault_name = sys.argv[1]
    config_manager = ConfigManager()

    indexer = ObsidianIndexer(config_manager, vault_name)
    indexer.update_index()
