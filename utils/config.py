import os

from dotenv import load_dotenv

# Load environment variables from .env file into os.environ
load_dotenv()

# API keys for different LLM providers
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Dictionary of available model providers and their respective models
MODEL_OPTIONS = { 
  "Gemini": {
    "playground": "https://ai.google.dev",
    "models": ["gemini-2.0-flash", "gemini-2.5-flash"]
  }
}
