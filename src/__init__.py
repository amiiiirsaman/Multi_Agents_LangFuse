"""
Multi-Agent LangFuse System Package

A production-ready multi-agent system using CrewAI, Amazon Bedrock (Nova Pro),
and LangFuse for observability.
"""

__version__ = "1.0.0"
__author__ = "amiiiirsaman"
__description__ = "Multi-agent system with researcher-reviewer workflow"

from .config import validate_config
from .logger import setup_logging, get_logger
from .main import run, init_langfuse

__all__ = [
    "validate_config",
    "setup_logging",
    "get_logger",
    "run",
    "init_langfuse",
]
