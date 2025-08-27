import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

if not HF_TOKEN:
    print("Warning: HF_TOKEN environment variable is not set")

if not RUNWAY_API_KEY:
    print("Warning: RUNWAY_API_KEY environment variable is not set")

if not STABILITY_API_KEY:
    print("Warning: STABILITY_API_KEY environment variable is not set")
