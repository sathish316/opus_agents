# Cookbook

## Build an Agent to connect to AI Gateways, internal or otherwise

This guide shows how to configure an agent to connect to an AI Gateway, instead of directly to model providers.

1. Configure the environment variables required for the AI Gateway
```bash
export GATEWAY_AUTH_TOKEN="your-auth-token"
export GATEWAY_USER_ID="your-user-id"
# any other params that are required for the AI Gateway
```

2. Configure the agent to use the AI Gateway by specifying the header keys and env variables to get values for these keys

```yaml
model_config:
  - provider: "gateway"
    model: "gpt-5"
    base_url: "https://your-ai-gateway-url"
    header_keys:
      - "X-Gateway-Auth-Token"
      - "X-Gateway-User-Id"
      - "X-Gateway-Param-1"
    header_values_env_keys:
      - "GATEWAY_AUTH_TOKEN"
      - "GATEWAY_USER_ID"
      - "GATEWAY_PARAM_1"
    enabled: true
```

3. Define the agent

Follow the steps in [Guide to Build a new deepwork agent](./GUIDE_BUILD_NEW_DEEPWORK_AGENT.md) for defining an agent.

4. Run the agent

Follow the steps in [Guide to Build a new deepwork agent](./GUIDE_BUILD_NEW_DEEPWORK_AGENT.md) for running an agent that uses the AI Gateway.