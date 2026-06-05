import asyncio

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from backend.openrouter import query_model
import backend.config as config

async def test_connectivity():
    print("Testing real API connectivity...\n")
    
    # Test 1: OpenRouter (using a fast configured model when possible)
    fast_model = next(
        (
            model for model in config.COUNCIL_MODELS
            if any(token in model for token in ("flash", "mini", "nano", "haiku", "fast"))
        ),
        config.COUNCIL_MODELS[0],
    )
    print(f"1. Testing OpenRouter ({fast_model})...")
    try:
        response = await query_model(fast_model, [{"role": "user", "content": "Say 'OpenRouter OK'"}], timeout=30.0)
        if response and response.get('content'):
            print(f"✅ OpenRouter Success: {response['content'][:50]}...")
        else:
            print(f"❌ OpenRouter Failed: No response")
            print(f"Response object: {response}")
    except Exception as e:
        print(f"❌ OpenRouter Error: {e}")

    # Test 2: Current configured council slate
    print("\n2. Configured council models:")
    for model in config.COUNCIL_MODELS:
        print(f"   - {model}")
    print(f"\nChairman: {config.CHAIRMAN_MODEL}")

if __name__ == "__main__":
    asyncio.run(test_connectivity())
