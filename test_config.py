"""
Simple test script to verify configuration and API connectivity
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config import get_secret
from src.langchain_post_agent import LangChainPostAgent

print("=" * 60)
print("🧪 TESTING CONFIGURATION")
print("=" * 60)

# Test 1: API Key
api_key = get_secret('GOOGLE_API_KEY')
if api_key:
    print("✅ API Key found:", api_key[:20] + "..." if len(api_key) > 20 else api_key)
else:
    print("❌ API Key NOT found!")
    sys.exit(1)

# Test 2: Initialize Agent
print("\n🤖 Initializing LangChain Agent...")
try:
    agent = LangChainPostAgent()
    print("✅ Agent initialized successfully")
except Exception as e:
    print(f"❌ Agent initialization failed: {e}")
    sys.exit(1)

# Test 3: Generate Sample Post
print("\n📝 Testing post generation...")
try:
    result = agent.generate_post_with_langchain(
        topic="Artificial Intelligence",
        tone="professional",
        length=1,
        target_audience="professionals"
    )
    
    if result:
        print("✅ Post generated successfully!")
        print(f"   Title: {result.get('title', 'N/A')[:50]}...")
        print(f"   Content length: {len(result.get('content', ''))} chars")
        print(f"   Metadata: {result.get('agent_metadata', {}).get('framework', 'N/A')}")
    else:
        print("❌ No result returned")
        
except Exception as e:
    print(f"❌ Generation failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!" if result else "❌ TESTS FAILED!")
print("=" * 60)
