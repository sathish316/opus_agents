"""
Opus TODO Agent - Collection of AI Agents and Custom tools for working with Productivity and Collaboration software.
"""

__version__ = "0.1.0"

# Import main modules for convenient access
from . import custom_tools, helper, higher_order_tools, models
from .todo_agent_builder import TodoAgentBuilder
from .todo_agent_runner import run_todo_agent
from .todo_mcp_server_registry import TodoMCPServerRegistry

__all__ = [
    "__version__",
    "custom_tools",
    "helper",
    "higher_order_tools",
    "models",
    "TodoAgentBuilder",
    "run_todo_agent",
    "TodoMcpServerRegistry",
]
