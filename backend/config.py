"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
CHAIRMAN_MODEL = "openai/gpt-5.2"

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
GROK_API_URL = "https://api.x.ai/v1/chat/completions"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Model specific configurations
# Maps model ID to (api_key, api_base_url)
MODEL_CONFIGS = {
    "grok-4-1-fast-reasoning": {
        "api_key": GROK_API_KEY,
        "api_url": GROK_API_URL,
    },
    "openai/gpt-5.2": {
        "api_key": OPENAI_API_KEY,
        "api_url": OPENAI_API_URL,
        # Map OpenRouter ID to OpenAI ID if different, but usually they are close.
        # OpenRouter: openai/gpt-5.2 -> OpenAI: gpt-5.2 (assuming)
        # If the OpenAI model ID is different, we might need a mapping here.
        # For now assuming "gpt-5.2" is the ID on OpenAI side.
        "provider_model_id": "gpt-5.2" 
    }
}

# Data directory for conversation storage
DATA_DIR = "data/conversations"

