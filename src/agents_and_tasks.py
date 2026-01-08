from crewai import Agent, Task, Crew, Process, LLM
from tools import search_tool, calculate_circle_area, ask_user
from dotenv import load_dotenv

load_dotenv()

nova_pro_llm = LLM(
    model="bedrock/amazon.nova-pro-v1:0",
    temperature=0.2,
    max_tokens=4000,
)

researcher = Agent(
    role="Researcher",
    goal="Gather evidence from the web and the user, then summarize it.",
    backstory="You use Serper and ask_user to collect high-quality evidence.",
    tools=[ask_user, search_tool],
    llm=nova_pro_llm,
    verbose=True,
)


reviewer = Agent(
    role="Reviewer",
    goal="Review all evidence and write the best, balanced answer with sources.",
    backstory="You critically read the research output and synthesize a final answer.",
    tools=[],  # reasoning only
    llm=nova_pro_llm,
    verbose=True,
)

research_task = Task(
    description=(
        "1) Use the ask_user tool to fully understand the user's question.\n"
        "2) Use the Serper web search tool at least once with the clarified question.\n"
        "3) Return a JSON object with:\n"
        "   - 'user_question': the final clarified question.\n"
        "   - 'serper_query': the exact search query you used.\n"
        "   - 'serper_results': a short bullet list of key points from the top 3 results, "
        "including site names or domains.\n"
        "   - 'provisional_answer': your best answer based on this evidence.\n"
    ),
    expected_output=(
        "A JSON object with keys: user_question, serper_query, serper_results, "
        "provisional_answer."
    ),
    agent=researcher,
)


review_task = Task(
    description=(
        "Read the JSON from the research_task. Using only that JSON and your own reasoning, "
        "produce the final answer.\n"
        "Your output must be a JSON object with:\n"
        "  - 'final_answer': your best combined answer.\n"
        "  - 'sources': an array of objects with fields:\n"
        "      - 'type': one of ['user', 'serper', 'model'].\n"
        "      - 'detail': short description, e.g. which domain or which user statement.\n"
        "      - 'role': how this source impacted the final answer.\n"
    ),
    expected_output="A JSON object with keys: final_answer, sources.",
    agent=reviewer,
)

crew = Crew(
    agents=[researcher, reviewer],
    tasks=[research_task, review_task],
    process=Process.sequential,
    verbose=True,
)