"""
Configuration settings for the Multi-Agent LangFuse project.
All environment variables and constants are centralized here.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

# AWS Bedrock Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# LLM Configuration
LLM_MODEL = "bedrock/amazon.nova-pro-v1:0"
LLM_TEMPERATURE = 0.2
LLM_MAX_TOKENS = 4000

# Langfuse Trace Configuration
TRACE_NAME = os.getenv("TRACE_NAME", "multi-agent-crewai-run")
TRACE_USER_ID = os.getenv("TRACE_USER_ID", "local-dev-user")
TRACE_SESSION_ID = os.getenv("TRACE_SESSION_ID", "dev-session-1")
TRACE_PROJECT_NAME = os.getenv("TRACE_PROJECT_NAME", "multi_agent_system")
TRACE_TAGS = ["crewai", "nova-pro", "multi-agent"]

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Project Configuration
PROJECT_NAME = "Multi-Agent LangFuse System"
VERSION = "1.0.0"

def validate_config():
    """
    Validate that all required environment variables are set.
    
    Raises:
        ValueError: If any required environment variable is missing.
    """
    required_vars = {
        "SERPER_API_KEY": SERPER_API_KEY,
        "LANGFUSE_SECRET_KEY": LANGFUSE_SECRET_KEY,
        "LANGFUSE_PUBLIC_KEY": LANGFUSE_PUBLIC_KEY,
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}. "
            "Please check your .env file."
        )
    
    return True
