import logging
from collections.abc import Callable
from typing import Any

from opus_agent_base.tools.custom_tool import CustomTool

logger = logging.getLogger(__name__)

ToolFunction = Callable[..., Any]


class LambdaAsTool(CustomTool):
    """
    Create Custom tools from plain functions or lambdas without subclassing CustomTool.

    Example:
        def add(a: int, b: int) -> int:
            '''Add two numbers.'''
            return a + b

        LambdaAsTool("calculator", "framework.lambda", add)
    """

    def __init__(
        self,
        name: str,
        config_key: str,
        *tool_functions: ToolFunction,
        config_manager=None,
        instructions_manager=None,
        model_manager=None,
        always_enabled: bool = False,
    ):
        if not tool_functions:
            raise ValueError("LambdaAsTool requires at least one function")

        super().__init__(
            name,
            config_key,
            config_manager,
            instructions_manager,
            model_manager,
        )
        self.tool_functions = tool_functions
        self.always_enabled = always_enabled

    def initialize_tools(self, agent):
        for func in self.tool_functions:
            agent.tool_plain(func)
            logger.info(f"Registered lambda tool: {func.__name__}")


def lambda_as_tool(
    *tool_functions: ToolFunction,
    name: str | None = None,
    config_key: str = "framework.lambda",
    config_manager=None,
    instructions_manager=None,
    model_manager=None,
    always_enabled: bool = False,
) -> LambdaAsTool:
    """
    Convenience factory for creating a LambdaAsTool from one or more functions.

    Example:
        add_tool = lambda_as_tool(
            lambda a, b: a + b,
            name="calculator",
        )
    """
    if not tool_functions:
        raise ValueError("lambda_as_tool requires at least one function")

    tool_name = name or (
        tool_functions[0].__name__
        if len(tool_functions) == 1
        else "lambda_tools"
    )

    return LambdaAsTool(
        tool_name,
        config_key,
        *tool_functions,
        config_manager=config_manager,
        instructions_manager=instructions_manager,
        model_manager=model_manager,
        always_enabled=always_enabled,
    )
