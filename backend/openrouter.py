"""OpenRouter API client for making LLM requests."""

import httpx
from typing import List, Dict, Any, Optional
from .config import OPENROUTER_API_KEY, OPENROUTER_API_URL, MODEL_CONFIGS


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via OpenRouter API.

    Args:
        model: OpenRouter model identifier (e.g., "openai/gpt-4o")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds

    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    # Determine which API configuration to use
    api_key = OPENROUTER_API_KEY
    api_url = OPENROUTER_API_URL
    model_id = model

    # Check if this model has a specific configuration
    if model in MODEL_CONFIGS:
        specific_config = MODEL_CONFIGS[model]
        # Only attempt specific config if API key is present
        if specific_config.get("api_key"):
            try:
                # Use specific configuration
                specific_api_key = specific_config["api_key"]
                specific_api_url = specific_config["api_url"]
                # Use provider specific model ID if available, otherwise use default
                specific_model_id = specific_config.get("provider_model_id", model)
                
                headers = {
                    "Authorization": f"Bearer {specific_api_key}",
                    "Content-Type": "application/json",
                }

                payload = {
                    "model": specific_model_id,
                    "messages": messages,
                }

                async with httpx.AsyncClient(timeout=timeout) as client:
                    response = await client.post(
                        specific_api_url,
                        headers=headers,
                        json=payload
                    )
                    response.raise_for_status()

                    data = response.json()
                    message = data['choices'][0]['message']

                    return {
                        'content': message.get('content'),
                        'reasoning_details': message.get('reasoning_details')
                    }
            except Exception as e:
                print(f"Error querying model {model} via direct API: {e}. Falling back to OpenRouter.")
                # Fallback to OpenRouter (continue below)
        else:
            # Config exists but no key provided, just use OpenRouter
            pass

    # Default / Fallback to OpenRouter
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173", # Optional OpenRouter headers
        "X-Title": "LLM Council",
    }

    payload = {
        "model": model, 
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                api_url,
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            data = response.json()
            message = data['choices'][0]['message']

            return {
                'content': message.get('content'),
                'reasoning_details': message.get('reasoning_details')
            }

    except Exception as e:
        print(f"Error querying model {model} via OpenRouter: {e}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.

    Args:
        models: List of OpenRouter model identifiers
        messages: List of message dicts to send to each model

    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio

    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model: response for model, response in zip(models, responses)}
