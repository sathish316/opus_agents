import inspect
import logging
from collections.abc import Callable
from functools import wraps
from typing import Any

from opus_agent_base.tools.custom_tool import CustomTool

logger = logging.getLogger(__name__)

ToolFunction = Callable[..., Any]


class LambdaAsTool(CustomTool):
    """Register a plain function or lambda as an agent tool."""

    def __init__(
        self,
        function: ToolFunction,
        *,
        name: str | None = None,
        description: str | None = None,
    ):
        if not callable(function):
            raise TypeError("function must be callable")

        function_name = getattr(function, "__name__", None)
        resolved_name = name or function_name
        if not resolved_name or resolved_name == "<lambda>":
            raise ValueError("name is required when registering a lambda")

        resolved_description = description or inspect.getdoc(function)
        if not resolved_description:
            raise ValueError(
                "description is required when the function has no docstring"
            )

        super().__init__(resolved_name, "framework.lambda")
        self.description = resolved_description
        self.function = self._create_tool_function(function)
        self.always_enabled = True

    def _create_tool_function(self, function: ToolFunction) -> ToolFunction:
        if inspect.iscoroutinefunction(function):

            @wraps(function)
            async def tool_function(*args, **kwargs):
                return await function(*args, **kwargs)

        else:

            @wraps(function)
            def tool_function(*args, **kwargs):
                return function(*args, **kwargs)

        tool_function.__name__ = self.name
        tool_function.__qualname__ = self.name
        tool_function.__doc__ = self.description
        return tool_function

    def initialize_tools(self, agent):
        agent.tool_plain(self.function, name=self.name)
        logger.info("Registered lambda tool: %s", self.name)


def lambda_as_tool(
    function: ToolFunction,
    *,
    name: str | None = None,
    description: str | None = None,
) -> LambdaAsTool:
    """Create a tool from a plain function or lambda."""
    return LambdaAsTool(function, name=name, description=description)
