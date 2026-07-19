import logging
from collections.abc import Awaitable, Callable
from typing import Any

from pydantic_ai import Agent, RunContext

logger = logging.getLogger(__name__)

PromptBuilder = Callable[..., str | Awaitable[str]]


class SubagentAsTool:
    """
    Wrap a PydanticAI Agent so a parent agent can invoke it as a tool.

    Simplifies the common flow of creating a subagent, building a prompt,
    and returning ``response.output`` to the parent agent.
    """

    def __init__(
        self,
        subagent: Agent,
        *,
        name: str = "subagent",
        tool_name: str | None = None,
    ):
        self.subagent = subagent
        self.name = name
        self.tool_name = tool_name or f"run_{name}"

    @classmethod
    def from_instructions(
        cls,
        *,
        name: str,
        instructions: str,
        model: Any,
        tool_name: str | None = None,
        **agent_kwargs: Any,
    ) -> "SubagentAsTool":
        subagent = Agent(instructions=instructions, model=model, **agent_kwargs)
        return cls(subagent, name=name, tool_name=tool_name)

    @classmethod
    def from_managers(
        cls,
        *,
        name: str,
        instructions_key: str,
        config_manager: Any,
        instructions_manager: Any,
        model_manager: Any,
        use_local_model_config_key: str | None = None,
        tool_name: str | None = None,
        **agent_kwargs: Any,
    ) -> "SubagentAsTool":
        if use_local_model_config_key and config_manager.get_setting(
            use_local_model_config_key, False
        ):
            model = model_manager.get_local_model()
        else:
            model = model_manager.get_model()
        instructions = instructions_manager.get(instructions_key)
        return cls.from_instructions(
            name=name,
            instructions=instructions,
            model=model,
            tool_name=tool_name,
            **agent_kwargs,
        )

    async def run(self, prompt: str, **run_kwargs: Any) -> str:
        logger.info(f"Calling SubAgent [{self.name}]")
        logger.debug(f"SubAgent [{self.name}] prompt: {prompt}")
        response = await self.subagent.run(prompt, **run_kwargs)
        output = response.output
        logger.info(f"SubAgent [{self.name}] response: {len(output)} chars")
        return output

    def run_sync(self, prompt: str, **run_kwargs: Any) -> str:
        logger.info(f"Calling SubAgent [{self.name}]")
        logger.debug(f"SubAgent [{self.name}] prompt: {prompt}")
        response = self.subagent.run_sync(prompt, **run_kwargs)
        output = response.output
        logger.info(f"SubAgent [{self.name}] response: {len(output)} chars")
        return output

    @staticmethod
    def format_prompt(template: str, **kwargs: Any) -> str:
        return template.format(**kwargs)

    def register_prompt_tool(
        self,
        parent_agent: Agent,
        *,
        sync: bool = False,
        tool_name: str | None = None,
    ) -> None:
        """
        Register a single ``prompt`` parameter tool on ``parent_agent`` that
        forwards the prompt to this subagent.
        """
        subagent_tool = self
        registered_tool_name = tool_name or self.tool_name

        if sync:

            @parent_agent.tool(name=registered_tool_name)
            def run_subagent(ctx: RunContext[Any], prompt: str) -> str:
                """Run a subagent with the given prompt and return its response."""
                return subagent_tool.run_sync(prompt)

        else:

            @parent_agent.tool(name=registered_tool_name)
            async def run_subagent(ctx: RunContext[Any], prompt: str) -> str:
                """Run a subagent with the given prompt and return its response."""
                return await subagent_tool.run(prompt)
