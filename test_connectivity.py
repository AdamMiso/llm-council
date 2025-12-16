
import asyncio
import os
import sys

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from backend.openrouter import query_model
import backend.config as config

async def test_connectivity():
    print("Testing real API connectivity...\n")
    
    # Test 1: OpenRouter (using gemini-2.5-flash as it's cheap/fast)
    print("1. Testing OpenRouter (google/gemini-2.5-flash)...")
    try:
        response = await query_model("google/gemini-2.5-flash", [{"role": "user", "content": "Say 'OpenRouter OK'"}], timeout=30.0)
        if response and response.get('content'):
            print(f"✅ OpenRouter Success: {response['content'][:50]}...")
        else:
            print(f"❌ OpenRouter Failed: No response")
            print(f"Response object: {response}")
    except Exception as e:
        print(f"❌ OpenRouter Error: {e}")

    # Test 2: x.ai (using the configured Grok model)
    grok_model = "grok-4-1-fast-reasoning"
    print(f"\n2. Testing x.ai ({grok_model})...")
    
    try:
        response = await query_model(grok_model, [{"role": "user", "content": "Say 'Grok OK'"}], timeout=30.0)
        if response and response.get('content'):
            print(f"✅ x.ai Success: {response['content'][:50]}...")
        else:
            print(f"❌ x.ai Failed: No response")
            print(f"Response object: {response}")
    except Exception as e:
        print(f"❌ x.ai Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_connectivity())
