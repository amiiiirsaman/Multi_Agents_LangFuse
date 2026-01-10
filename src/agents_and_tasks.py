"""Agent and task definitions for the multi-agent system.

Defines the researcher and reviewer agents along with their respective tasks.
Implements a sequential workflow for evidence gathering and synthesis.
"""
from crewai import Agent, Task, Crew, Process, LLM
from tools import search_tool, ask_user
from config import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
from logger import get_logger

logger = get_logger(__name__)

# ============================================================================
# LLM Configuration
# ============================================================================

def get_llm_config():
    """Create and return a configured LLM instance.
    
    Returns:
        LLM: Configured LLM instance for Amazon Nova Pro
    """
    try:
        llm = LLM(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
        )
        logger.info(f"LLM configured: {LLM_MODEL} (temp={LLM_TEMPERATURE})")
        return llm
    except Exception as e:
        logger.error(f"Failed to configure LLM: {e}")
        raise


nova_pro_llm = get_llm_config()

# ============================================================================
# Agent Definitions
# ============================================================================

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
)
logger.info("Researcher agent initialized")

reviewer = Agent(
    role="Reviewer",
    goal="Review all evidence and write the best, balanced answer with sources.",
    backstory=(
        "You are a critical thinker and expert synthesizer. Your role is to "
        "review all research findings, validate sources, and produce comprehensive "
        "answers that are accurate, well-structured, and properly cited. "
        "You ensure every claim is backed by evidence."
    ),
    tools=[],  # Reasoning only - no tools needed
    llm=nova_pro_llm,
    verbose=True,
)
logger.info("Reviewer agent initialized")

# ============================================================================
# Task Definitions
# ============================================================================

research_task = Task(
    description=(
        "Your mission is to thoroughly understand the user's question and gather "
        "relevant evidence:\n\n"
        "STEP 1: Use the 'ask_user' tool to clarify exactly what the user wants to know. "
        "Ask follow-up questions if needed to fully understand the context and requirements.\n\n"
        "STEP 2: Based on the clarified question, formulate an effective search query "
        "and use the Serper web search tool to find relevant information. "
        "Search at least once, but search multiple times with different queries if needed "
        "for comprehensive coverage.\n\n"
        "STEP 3: Analyze the search results and extract key points from the top 3-5 sources. "
        "Note the source domains/sites for citation purposes.\n\n"
        "STEP 4: Formulate a provisional answer based on the evidence you've gathered.\n\n"
        "Your output MUST be a valid JSON object with these exact keys:\n"
        "- 'user_question': The final clarified question from the user\n"
        "- 'serper_query': The search query/queries you used (comma-separated if multiple)\n"
        "- 'serper_results': A bullet list of key findings from top sources with site names\n"
        "- 'provisional_answer': Your initial answer based on the evidence\n\n"
        "Example output format:\n"
        '{\n'
        '  "user_question": "What are the latest...",\n'
        '  "serper_query": "latest developments AI safety 2026",\n'
        '  "serper_results": "• OpenAI released new safety guidelines (openai.com)\\n• ...",\n'
        '  "provisional_answer": "Based on recent sources..."\n'
        '}'
    ),
    expected_output=(
        "A valid JSON object containing: user_question (string), serper_query (string), "
        "serper_results (string with bullet points), and provisional_answer (string)."
    ),
    agent=researcher,
)
logger.info("Research task configured")

review_task = Task(
    description=(
        "Your mission is to synthesize a high-quality final answer with proper attribution:\n\n"
        "STEP 1: Carefully read the JSON output from the research_task. "
        "This contains the user's question, search queries, results, and provisional answer.\n\n"
        "STEP 2: Critically evaluate the evidence:\n"
        "- Assess the quality and relevance of each source\n"
        "- Identify any gaps or contradictions\n"
        "- Consider the credibility of sources\n\n"
        "STEP 3: Synthesize a comprehensive final answer that:\n"
        "- Directly addresses the user's question\n"
        "- Incorporates the best evidence from research\n"
        "- Maintains objectivity and balance\n"
        "- Is clear, well-structured, and actionable\n\n"
        "STEP 4: Document all sources that contributed to your answer.\n\n"
        "Your output MUST be a valid JSON object with these exact keys:\n"
        "- 'final_answer': Your comprehensive, well-reasoned answer (string)\n"
        "- 'sources': An array of source objects, each with:\n"
        "    - 'type': one of ['user', 'serper', 'model'] (string)\n"
        "    - 'detail': brief description like domain name or user statement (string)\n"
        "    - 'role': how this source influenced the answer (string)\n\n"
        "Example output format:\n"
        '{\n'
        '  "final_answer": "Based on comprehensive research...",\n'
        '  "sources": [\n'
        '    {"type": "serper", "detail": "openai.com", "role": "Primary source for safety guidelines"},\n'
        '    {"type": "user", "detail": "User clarification on scope", "role": "Defined question scope"},\n'
        '    {"type": "model", "detail": "Analysis and synthesis", "role": "Connected findings"}\n'
        '  ]\n'
        '}'
    ),
    expected_output=(
        "A valid JSON object containing: final_answer (string) and sources (array of objects "
        "with type, detail, and role fields)."
    ),
    agent=reviewer,
)
logger.info("Review task configured")

# ============================================================================
# Crew Configuration
# ============================================================================

crew = Crew(
    agents=[researcher, reviewer],
    tasks=[research_task, review_task],
    process=Process.sequential,
    verbose=True,
)
logger.info("Crew configured with sequential process: researcher -> reviewer")
