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

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
GROK_API_URL = "https://api.x.ai/v1/chat/completions"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# Model presets use OpenRouter identifiers. The "latest" preset keeps cost and
# latency reasonable while representing each already-listed provider once.
MODEL_PRESETS = {
    "latest": [
        "openai/gpt-5.4-pro",
        "google/gemini-3.1-pro-preview",
        "anthropic/claude-opus-4.8",
        "x-ai/grok-4.3",
    ],
    "expanded": [
        "openai/gpt-5.4-pro",
        "openai/gpt-chat-latest",
        "openai/gpt-5.4-mini",
        "google/gemini-3.1-pro-preview",
        "google/gemini-3.5-flash",
        "google/gemini-3.1-flash-lite",
        "anthropic/claude-opus-4.8",
        "anthropic/claude-sonnet-4.6",
        "anthropic/claude-haiku-4.5",
        "x-ai/grok-4.3",
        "x-ai/grok-4.20",
        "x-ai/grok-build-0.1",
    ],
}


def _csv_env(name: str) -> list[str]:
    """Read a comma-separated env var into a clean list."""
    value = os.getenv(name, "")
    return [item.strip() for item in value.split(",") if item.strip()]


def _configured_models() -> list[str]:
    """Resolve council models from explicit env override or a named preset."""
    env_models = _csv_env("COUNCIL_MODELS")
    if env_models:
        return env_models

    preset_name = os.getenv("COUNCIL_PRESET", "latest").strip().lower()
    return MODEL_PRESETS.get(preset_name, MODEL_PRESETS["latest"])


# Council members - list of OpenRouter model identifiers
COUNCIL_MODELS = _configured_models()

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = os.getenv("CHAIRMAN_MODEL", COUNCIL_MODELS[0])

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
        "provider_model_id": "gpt-5.2" 
    }
}

# Data directory for conversation storage
DATA_DIR = "data/conversations"
