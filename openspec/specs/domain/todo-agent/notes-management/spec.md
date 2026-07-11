# Notes Management Specification

## Purpose
Let the user ask questions to their Obsidian notes by indexing the vault and answering queries with retrieval-augmented generation.

## Requirements

### Requirement: Note Indexing
The system SHALL index the user's Obsidian vault into a local vector store (ChromaDB) via a background indexer job so notes are searchable.

#### Scenario: Vault indexed
- **WHEN** the background indexer runs against the configured Obsidian vault
- **THEN** note content is embedded and stored in the local vector store

### Requirement: Ask Questions To Notes
The system SHALL answer natural-language questions over the indexed notes using retrieval-augmented generation, retrieving relevant notes and generating an answer grounded in them.

#### Scenario: Question answered from notes
- **WHEN** the user asks a question about their notes
- **THEN** the system retrieves relevant note passages and answers based on them
