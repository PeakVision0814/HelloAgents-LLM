"""
HelloAgents package exports.
"""

import logging

from .utils.logging import configure_package_logging

configure_package_logging()

# Reduce third-party log noise in the console.
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("qdrant_client").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("neo4j").setLevel(logging.WARNING)
logging.getLogger("neo4j.notifications").setLevel(logging.WARNING)

from .version import __author__, __description__, __email__, __version__
from .core.llm import HelloAgentsLLM
from .core.config import Config
from .core.message import Message
from .core.exceptions import HelloAgentsException
from .agents.simple_agent import SimpleAgent
from .agents.react_agent import ReActAgent
from .agents.reflection_agent import ReflectionAgent
from .agents.plan_solve_agent import PlanAndSolveAgent
from .agents.tool_aware_agent import ToolAwareSimpleAgent
from .tools.registry import ToolRegistry, global_registry
from .tools.builtin.search_tool import SearchTool, search
from .tools.builtin.calculator import CalculatorTool, calculate
from .tools.chain import ToolChain, ToolChainManager
from .tools.async_executor import AsyncToolExecutor

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__description__",
    "HelloAgentsLLM",
    "Config",
    "Message",
    "HelloAgentsException",
    "SimpleAgent",
    "ReActAgent",
    "ReflectionAgent",
    "PlanAndSolveAgent",
    "ToolAwareSimpleAgent",
    "ToolRegistry",
    "global_registry",
    "SearchTool",
    "search",
    "CalculatorTool",
    "calculate",
    "ToolChain",
    "ToolChainManager",
    "AsyncToolExecutor",
]
