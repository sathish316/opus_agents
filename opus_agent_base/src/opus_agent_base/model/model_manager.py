import logging
import os

from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.providers.openai import OpenAIProvider

from opus_agent_base.common.logging_config import console_log
from opus_agent_base.gateway.openai_compatible_gateway import OpenAIAIGatewayProvider

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
        console_log(f"Enabled {len(self.get_enabled_models())} models: {self.get_enabled_models()}")

    def initialize_model(self):
        self.initialize_openai_model()
        self.initialize_anthropic_model()
        self.initialize_bedrock_model()
        self.initialize_ollama_model()
        logger.info("Model initialized")

    def get_enabled_models(self):
        return [model_config["model"] for model_config in self.models_config if model_config["enabled"]]

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

    def initialize_ai_gateway_model(self):
        for model_config in self.models_config:
            if model_config["provider"] == "gateway" and model_config["enabled"]:
                self.model = OpenAIChatModel(
                    model_name=model_config["model"],
                    provider=OpenAIAIGatewayProvider(model_config=model_config),
                )
                logger.info(f"AI Gateway model initialized: {model_config['model']}")