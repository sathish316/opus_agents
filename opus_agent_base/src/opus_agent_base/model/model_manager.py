import logging
import os

from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.providers.openai import OpenAIProvider

logger = logging.getLogger(__name__)

class ModelManager:
    """
    Manager for model configuration and initialization
    """

    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.initialize_config()
        self.initialize_model()

    def initialize_config(self):
        self.models_config = self.config_manager.get_setting("model_config")

    def initialize_model(self):
        self.initialize_openai_model()
        self.initialize_anthropic_model()
        self.initialize_bedrock_model()
        self.initialize_ollama_model()
        logger.info("Model initialized")

    def get_model(self):
        return self.model

    def get_local_model(self):
        return self.local_model

    def initialize_openai_model(self):
        for model_config in self.models_config:
            if model_config["provider"] == "openai" and model_config["enabled"]:
                # TODO: add timeout and max_retries
                self.model = OpenAIChatModel(
                    model_config["model"], provider=OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
                )
                logger.info(f"OpenAI model initialized: {model_config['model']}")

    def initialize_anthropic_model(self):
        for model_config in self.models_config:
            if model_config["provider"] == "anthropic" and model_config["enabled"]:
                # TODO: add timeout and max_retries
                self.model = AnthropicModel(
                    model_config["model"], provider=AnthropicProvider(api_key=os.getenv("ANTHROPIC_API_KEY"))
                )
                logger.info(f"Anthropic model initialized: {model_config['model']}")

    def initialize_bedrock_model(self):
        pass

    def initialize_ollama_model(self):
        for model_config in self.models_config:
            if model_config["provider"] == "ollama" and model_config["enabled"] and model_config["is_local"]:
                self.local_model = OpenAIChatModel(
                    model_name=model_config["model"],
                    provider=OllamaProvider(base_url=model_config["base_url"]),
                )
                logger.info(f"Ollama/OpenAI model initialized: {model_config['model']}")