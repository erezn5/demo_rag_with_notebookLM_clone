import os
from pathlib import Path

from dotenv import load_dotenv


def init():
    # Move the logic inside this function
    Path(__file__).resolve()
    
    load_dotenv()

    # Optional feedback
    if os.environ.get("OPENAI_API_KEY"):
        print("✅ API Key loaded.")