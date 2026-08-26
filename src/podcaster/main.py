#!/usr/bin/env python
import sys
import time
import warnings
import os

from datetime import datetime

# Configure LiteLLM retry behavior BEFORE any CrewAI imports.
# CrewAI uses LiteLLM to call the Gemini API, and free-tier keys
# hit rate limits quickly. This makes all 3 agents retry automatically.
import litellm
litellm.num_retries = 5                       # Retry up to 5 times on transient errors
litellm.request_timeout = 120                 # Allow 2 minutes per request
litellm.retry_after = 30                      # Wait 30 seconds between retries
litellm.retry_on_status_codes = [429, 503]    # Retry on both rate-limit AND high-demand

from podcaster.crew import Podcaster

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

TOPIC = 'Latest gaming'  # <-- Change the topic here (one place only)

MAX_CREW_RETRIES = 3
CREW_RETRY_WAIT = 60  # seconds

def run():
    """
    Run the crew with automatic retry on transient API errors.
    """
    inputs = {
        'topic': TOPIC,
        'current_month': str(datetime.now().month),
        'current_year': str(datetime.now().year)
    }
    
    for attempt in range(1, MAX_CREW_RETRIES + 1):
        try:
            print(f"🚀 Starting crew (attempt {attempt}/{MAX_CREW_RETRIES})...")
            Podcaster().crew().kickoff(inputs=inputs)
            print("✅ Crew completed successfully!")
            return
        except Exception as e:
            err = str(e).lower()
            is_transient = (
                "429" in err or "503" in err
                or "rate" in err or "quota" in err
                or "resource_exhausted" in err
                or "high demand" in err
                or "unavailable" in err
            )
            if is_transient and attempt < MAX_CREW_RETRIES:
                print(
                    f"\n⏳ Transient API error (attempt {attempt}/{MAX_CREW_RETRIES}). "
                    f"Waiting {CREW_RETRY_WAIT}s before retry...\n"
                )
                time.sleep(CREW_RETRY_WAIT)
            else:
                raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": TOPIC,
        'current_month': str(datetime.now().month),
        'current_year': str(datetime.now().year)
    }
    try:
        Podcaster().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Podcaster().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": TOPIC,
        "current_year": str(datetime.now().year)
    }
    
    try:
        Podcaster().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
