import os

from openai import AsyncOpenAI
from pydantic_ai.providers.openai import OpenAIProvider


class AsyncOpenAIAIGatewayClient(AsyncOpenAI):
    """OpenAI client for AIGateway."""

    def _prepare_request(self, request):
        headers_config = zip(self.header_keys, self.header_values_env_keys, strict=True)
        headers = {
            key: os.getenv(env_val)
            for key, env_val in headers_config
            if os.getenv(env_val)
        }
        request.headers.update(headers)
        return super()._prepare_request(request)

    def configure_headers(
        self, header_keys: list[str], header_values_env_keys: list[str]
    ):
        self.header_keys = header_keys
        self.header_values_env_keys = header_values_env_keys


class OpenAIAIGatewayProvider(OpenAIProvider):
    """
    Provider for OpenAI compatible AI Gateways
    """
    def __init__(self, model_config: dict[str, str], *args, **kwargs):
        client = self._build_openai_compatible_client(model_config)
        super().__init__(*args, openai_client=client, **kwargs)
        self._configure_openai_compatible_client(client, model_config)

    def _build_openai_compatible_client(self, model_config: dict[str, str]):
        base_url = model_config.get("base_url")
        timeout = int(model_config.get("timeout", 300))
        client = AsyncOpenAIAIGatewayClient(
            base_url=base_url + "/v1/openai/v1",
            api_key="NA",
            timeout=timeout,
        )
        return client

    def _configure_openai_compatible_client(
        self, client: AsyncOpenAIAIGatewayClient, model_config: dict[str, str]
    ):
        header_keys = model_config.get("header_keys", [])
        header_values_env_keys = model_config.get("header_values_env_keys", [])
        client.configure_headers(header_keys, header_values_env_keys)
