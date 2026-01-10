"""Agent and task definitions - CrewAI 1.8.0 compatible version"""
from crewai import Agent, Task, Crew, Process, LLM
from tools import search_tool, ask_user
from config import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS, AWS_REGION
from logger import get_logger
import os

logger = get_logger(__name__)

# LLM Configuration for CrewAI 1.8.0 (uses CrewAI's LLM wrapper with Bedrock)
def get_llm_config():
    try:
        # CrewAI 1.8.0 expects LLM configuration with provider details
        llm = LLM(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
            aws_region_name=AWS_REGION,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        logger.info(f"LLM configured: {LLM_MODEL}")
        return llm
    except Exception as e:
        logger.error(f"Failed to configure LLM: {e}")
        raise

nova_pro_llm = get_llm_config()

# Agent Definitions
researcher = Agent(
    role="Researcher",
    goal="Gather evidence from the web and the user, then summarize it.",
    backstory=(
        "You are a meticulous researcher who excels at understanding user needs "
        "and finding relevant information. You use the Serper search tool to find "
        "web-based evidence and the ask_user tool to clarify requirements. "
        "You always cite your sources and organize information clearly."
    ),
    tools=[ask_user, search_tool],
    llm=nova_pro_llm,
    verbose=True,
    allow_delegation=False
)

reviewer = Agent(
    role="Reviewer",
    goal="Synthesize the researcher's findings into a final answer with proper source attribution.",
    backstory=(
        "You are an expert reviewer who evaluates research and produces well-structured answers. "
        "You ensure all claims are properly sourced and create a clear list of references. "
        "You organize information logically and highlight the most important findings."
    ),
    llm=nova_pro_llm,
    verbose=True,
    allow_delegation=False
)

# Task Definitions  
research_task = Task(
    description=(
        "1. Use the ask_user tool to ask: 'What would you like to know?'\n"
        "2. Based on the user's answer, search the web using search_tool\n"
        "3. Return JSON with:\n"
        "   - user_question: the question from step 1\n"
        "   - search_query: your search query\n"
        "   - search_results: results from Serper\n"
        "   - provisional_answer: your draft answer"
    ),
    agent=researcher,
    expected_output="JSON with user_question, search_query, search_results, and provisional_answer"
)

review_task = Task(
    description=(
        "Using the researcher's output:\n"
        "1. Synthesize a final answer that addresses the user's question\n"
        "2. Create a 'sources' list with entries like:\n"
        "   {\"type\": \"serper\", \"detail\": \"<domain or snippet>\", \"role\": \"<how it contributed>\"}\n"
        "   {\"type\": \"user\", \"detail\": \"User query\", \"role\": \"Question definition\"}\n"
        "3. Return JSON with:\n"
        "   - final_answer: comprehensive answer\n"
        "   - sources: list of source objects"
    ),
    agent=reviewer,
    expected_output="JSON with final_answer and sources list"
)

# Crew Configuration
crew = Crew(
    agents=[researcher, reviewer],
    tasks=[research_task, review_task],
    process=Process.sequential,
    verbose=True
)
