"""
Complete Multi-Agent Example - No User Input Required
Demonstrates the full system with automated responses
"""
import sys
sys.path.insert(0, 'src')

from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from config import LLM_MODEL, LLM_TEMPERATURE, AWS_REGION
import os

print("=" * 70)
print("Complete Multi-Agent System Demo")
print("=" * 70)

# Configure LLM
llm = LLM(
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE,
    max_tokens=1000,
    aws_region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

# Configure tool
search_tool = SerperDevTool()

# Define a simple researcher agent
researcher = Agent(
    role="Research Assistant",
    goal="Provide concise, accurate information about Amazon Bedrock",
    backstory="You are an AI expert specializing in AWS services.",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

# Define a simple task
research_task = Task(
    description="Search for information about Amazon Bedrock Nova Pro and provide a 2-sentence summary.",
    agent=researcher,
    expected_output="A 2-sentence summary about Amazon Bedrock Nova Pro"
)

# Create crew
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True
)

print("\n1. Crew Configuration:")
print(f"   Agents: {len(crew.agents)}")
print(f"   Tasks: {len(crew.tasks)}")
print(f"   LLM: {LLM_MODEL}")

print("\n2. Starting crew execution...")
print("-" * 70)

try:
    result = crew.kickoff()
    
    print("-" * 70)
    print("\n3. Results:")
    print(f"\n{result}")
    
    print("\n" + "=" * 70)
    print("SUCCESS! Multi-agent workflow completed")
    print("=" * 70)
    
except Exception as e:
    print(f"\nError during execution: {e}")
    print("\nNote: If you see a Serper API error, it means the system")
    print("is working but needs the search to be configured.")
