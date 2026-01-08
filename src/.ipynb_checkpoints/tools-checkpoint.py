from crewai_tools import SerperDevTool
from crewai.tools import tool
from dotenv import load_dotenv
import os
import math

load_dotenv()

# Web search tool using Serper (hard-coded key)
search_tool = SerperDevTool(
    api_key="0826551de68ea059fa47d086a51e02b4e257a511d5b188898f79f21127e88a0f"
)

def calculate_circle_area(radius: float) -> float:
    return math.pi * radius * radius

@tool("Ask User")
def ask_user(question: str) -> str:
    """Ask the human user a question in the console and return their exact answer."""
    print("\n[ENGINE QUESTION]", question)
    answer = input("[YOUR ANSWER] ")
    return answer