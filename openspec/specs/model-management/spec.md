# Model Management Specification

## Purpose
Let the agent run on the user's choice of LLM: frontier models via API keys, or local models for data that must not leave the machine.

## Requirements

### Requirement: Frontier Model Providers
The system SHALL support frontier model providers — OpenAI, Anthropic, and AWS Bedrock — selected via configuration and authenticated with provider API keys from the environment.

#### Scenario: Configured provider is used
- **WHEN** a provider is selected in configuration and its API key is present in the environment
- **THEN** the agent initializes and uses that provider's model

### Requirement: Local Models
The system SHALL support local models (e.g. Ollama-served models such as gpt-oss or Qwen) so that sensitive tools and data can run without leaving the user's machine.

#### Scenario: Local model requested
- **WHEN** a local model is configured
- **THEN** the agent initializes the local model instead of a hosted provider
