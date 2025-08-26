import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API key for Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN")

# Validate required environment variables
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is not set")
