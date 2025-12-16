"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Grok API key
GROK_API_KEY = os.getenv("GROK_API_KEY")

# Council members - list of OpenRouter model identifiers
COUNCIL_MODELS = [
    "openai/gpt-5.2",
    "google/gemini-3-pro-preview",
    "anthropic/claude-opus-4.5",
    "grok-4-1-fast-reasoning", # xAI model ID
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = "grok-4-1-fast-reasoning"

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
GROK_API_URL = "https://api.x.ai/v1/chat/completions"

# Model specific configurations
# Maps model ID to (api_key, api_base_url)
MODEL_CONFIGS = {
    "grok-4-1-fast-reasoning": {
        "api_key": GROK_API_KEY,
        "api_url": GROK_API_URL,
    }
}

# Data directory for conversation storage
DATA_DIR = "data/conversations"
