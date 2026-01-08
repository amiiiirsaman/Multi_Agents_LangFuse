# agents_and_tasks.py
from crewai import Agent, Task, Crew, Process
from tools import search_tool, calculate_circle_area

# Research agent that can browse the web
researcher = Agent(
    role="Technology Researcher",
    goal="Research a given AI topic and provide a concise summary.",
    backstory=(
        "You are an experienced AI researcher who keeps up with the latest "
        "developments in LLMs, multi-agent systems, and tools."
    ),
    tools=[search_tool],
    verbose=True,
)

# Analyst agent that can do reasoning and simple math
analyst = Agent(
    role="Technical Analyst",
    goal="Analyze the research and provide practical recommendations.",
    backstory=(
        "You are a senior AI engineer who focuses on pragmatic, actionable "
        "recommendations for building production systems."
    ),
    tools=[],
    verbose=True,
)

research_task = Task(
    description=(
        "Research the latest best practices for building production-ready "
        "multi-agent systems with CrewAI, including observability and evaluation."
    ),
    expected_output="A concise bullet list (5–8 bullets) of best practices.",
    agent=researcher,
)

analysis_task = Task(
    description=(
        "Given the research summary, propose a concrete next-step plan for a "
        "1-week experiment schedule to adopt these practices in a small project."
    ),
    expected_output="A step-by-step 1-week plan with specific actions each day.",
    agent=analyst,
)

crew = Crew(
    agents=[researcher, analyst],
    tasks=[research_task, analysis_task],
    process=Process.sequential,
    verbose=True,
)
