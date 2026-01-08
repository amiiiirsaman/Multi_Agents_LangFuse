# main.py
from dotenv import load_dotenv
from langfuse import get_client
from agents_and_tasks import crew

def init_langfuse():
    load_dotenv()
    client = get_client()
    # Optional: this will raise if keys/host are wrong in many setups
    return client

def run():
    langfuse = init_langfuse()

    # Root span / trace for the whole run
    with langfuse.start_as_current_observation(
        as_type="span",
        name="day12-crewai-run",
        input={"project": "multi_agent"},
    ) as span:
        # Set trace-level metadata
        span.update_trace(
            user_id="local-dev-user",
            session_id="dev-session-1",
            metadata={"project": "day12_multi_agent"},
            tags=["crewai", "nova-pro", "multi-agent"],
        )

        print("Starting CrewAI workflow (Langfuse root span id):", span.id)
        result = crew.kickoff()
        span.update(output=str(result))

    print("\n=== Final Crew Result ===")
    print(result)

if __name__ == "__main__":
    run()
