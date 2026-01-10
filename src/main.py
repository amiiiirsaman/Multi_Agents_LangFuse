"""Main entry point for the Multi-Agent LangFuse system.

Provides the orchestration of the CrewAI workflow with full LangFuse observability.
"""
from langfuse import get_client
from agents_and_tasks import crew
from config import (
    validate_config,
    TRACE_NAME,
    TRACE_USER_ID,
    TRACE_SESSION_ID,
    TRACE_PROJECT_NAME,
    TRACE_TAGS,
    PROJECT_NAME,
    VERSION,
)
from logger import setup_logging, get_logger
import sys
import json

# Initialize logging
setup_logging()
logger = get_logger(__name__)


def init_langfuse():
    """Initialize Langfuse client with configuration validation.
    
    Returns:
        Langfuse: Configured Langfuse client instance
        
    Raises:
        ValueError: If required configuration is missing
        Exception: If Langfuse client initialization fails
    """
    try:
        logger.info("Initializing Langfuse client...")
        validate_config()
        client = get_client()
        logger.info("Langfuse client initialized successfully")
        return client
    except ValueError as e:
        logger.error(f"Configuration validation failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to initialize Langfuse client: {e}")
        raise


def run():
    """Execute the multi-agent workflow with full observability.
    
    This function:
    1. Validates configuration
    2. Initializes Langfuse tracing
    3. Executes the CrewAI workflow
    4. Captures and logs results
    5. Handles errors gracefully
    
    Returns:
        dict or str: The final crew result
    """
    logger.info(f"Starting {PROJECT_NAME} v{VERSION}")
    
    try:
        # Initialize Langfuse
        langfuse = init_langfuse()

        # Create root span for the entire workflow
        with langfuse.start_as_current_observation(
            as_type="span",
            name=TRACE_NAME,
            input={"project": TRACE_PROJECT_NAME, "version": VERSION},
        ) as root_span:
            # Set trace-level metadata
            root_span.update_trace(
                user_id=TRACE_USER_ID,
                session_id=TRACE_SESSION_ID,
                metadata={
                    "project": TRACE_PROJECT_NAME,
                    "version": VERSION,
                },
                tags=TRACE_TAGS,
            )

            logger.info(f"Created Langfuse root span: {root_span.id}")
            print(f"\n{'='*60}")
            print(f"Starting {PROJECT_NAME}")
            print(f"Langfuse Trace ID: {root_span.id}")
            print(f"{'='*60}\n")

            # Create a span for the crew execution
            with langfuse.start_as_current_observation(
                as_type="span",
                name="crew-execution",
                input={"agents": ["researcher", "reviewer"]},
            ) as crew_span:
                try:
                    logger.info("Starting CrewAI workflow...")
                    result = crew.kickoff()
                    logger.info("CrewAI workflow completed successfully")
                    
                    # Update crew span with output
                    crew_span.update(output=str(result))
                    
                except Exception as e:
                    logger.error(f"CrewAI workflow failed: {e}", exc_info=True)
                    crew_span.update(
                        level="ERROR",
                        status_message=str(e),
                    )
                    raise

            # Update root span with final output
            root_span.update(output=str(result))
            logger.info("Workflow completed, updating root span")

        # Display results
        print(f"\n{'='*60}")
        print("FINAL RESULT")
        print(f"{'='*60}")
        
        # Try to parse and pretty-print JSON if possible
        try:
            if isinstance(result, str):
                result_dict = json.loads(result)
                print(json.dumps(result_dict, indent=2))
            else:
                print(result)
        except (json.JSONDecodeError, AttributeError):
            print(result)
        
        print(f"{'='*60}\n")
        
        logger.info("Workflow completed successfully")
        return result

    except KeyboardInterrupt:
        logger.warning("Workflow interrupted by user")
        print("\n\nWorkflow interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error in workflow: {e}", exc_info=True)
        print(f"\n\nERROR: {e}")
        print("Check logs/app.log for detailed error information.")
        sys.exit(1)


if __name__ == "__main__":
    run()
