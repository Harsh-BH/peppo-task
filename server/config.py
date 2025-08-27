import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API key for Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN")

# API key for Runway
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")

# Validate required environment variables
if not HF_TOKEN:
    print("Warning: HF_TOKEN environment variable is not set")

if not RUNWAY_API_KEY:
    print("Warning: RUNWAY_API_KEY environment variable is not set")
