"""Tools for the multi-agent system.

Provides web search and user interaction capabilities.
"""
from crewai_tools import SerperDevTool
from crewai.tools import tool
from config import SERPER_API_KEY
from logger import get_logger

logger = get_logger(__name__)

# Web search tool using Serper API
try:
    if not SERPER_API_KEY:
        raise ValueError("SERPER_API_KEY not found in environment variables")
    
    search_tool = SerperDevTool(api_key=SERPER_API_KEY)
    logger.info("Serper search tool initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Serper tool: {e}")
    raise


@tool("Ask User")
def ask_user(question: str) -> str:
    """Ask the human user a question in the console and return their exact answer.
    
    Args:
        question: The question to ask the user
        
    Returns:
        str: The user's response
        
    Raises:
        ValueError: If question is empty or None
        EOFError: If input stream is closed
    """
    if not question or not question.strip():
        logger.error("Attempted to ask user an empty question")
        raise ValueError("Question cannot be empty")
    
    try:
        logger.info(f"Asking user: {question}")
        print("\n[ENGINE QUESTION]", question)
        answer = input("[YOUR ANSWER] ")
        
        if not answer.strip():
            logger.warning("User provided empty answer")
            return "No answer provided"
        
        logger.info(f"User answered: {answer[:100]}...")  # Log first 100 chars
        return answer
        
    except EOFError as e:
        logger.error("Input stream closed while waiting for user input")
        raise EOFError("Cannot read user input: input stream closed") from e
    except KeyboardInterrupt:
        logger.warning("User interrupted input with Ctrl+C")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while asking user: {e}")
        raise
