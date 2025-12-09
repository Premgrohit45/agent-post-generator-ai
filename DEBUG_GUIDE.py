"""
Debugging Guide for Generation Failed Error

If you're seeing "Generation failed: Unknown error", follow these steps:
"""

# STEP 1: Check if API Key is Valid
print("1️⃣  CHECKING API KEY...")
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("❌ API Key not found in .env file!")
    print("   Add: GOOGLE_API_KEY=your_key_here")
    exit(1)
else:
    print(f"✅ API Key found: {api_key[:30]}...")

# STEP 2: Test LLM Connection
print("\n2️⃣  TESTING LLM CONNECTION...")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.9
    )
    response = llm.invoke("Say hello")
    print("✅ LLM Connection OK")
    print(f"   Response: {str(response)[:100]}...")
except Exception as e:
    print(f"❌ LLM Connection Failed: {e}")
    print("\n💡 SOLUTIONS:")
    print("   1. Check if API key is valid (go to Google AI Studio)")
    print("   2. Check internet connection")
    print("   3. Check if gemini-2.5-flash model is available in your region")
    exit(1)

# STEP 3: Test Agent Tools
print("\n3️⃣  TESTING AGENT TOOLS...")
try:
    from src.agent_tools import create_langchain_tools
    tools = create_langchain_tools()
    print(f"✅ Agent Tools OK: {len(tools)} tools available")
    for tool in tools:
        print(f"   - {tool.name}")
except Exception as e:
    print(f"❌ Agent Tools Failed: {e}")
    exit(1)

# STEP 4: Test LangGraph Agent
print("\n4️⃣  TESTING LANGGRAPH AGENT...")
try:
    from langgraph.prebuilt import create_react_agent
    agent = create_react_agent(
        model=llm,
        tools=tools
    )
    print("✅ LangGraph Agent OK")
except Exception as e:
    print(f"❌ LangGraph Agent Failed: {e}")
    exit(1)

# STEP 5: Test Complete Pipeline
print("\n5️⃣  TESTING COMPLETE PIPELINE...")
try:
    from src.langchain_post_agent import LangChainPostAgent
    agent = LangChainPostAgent()
    result = agent.generate_post_with_langchain(
        topic="Machine Learning",
        tone="professional",
        length=1,
        target_audience="professionals"
    )
    
    if result and isinstance(result, dict):
        print("✅ Post Generation OK")
        print(f"   Title: {result.get('title', 'N/A')[:50]}")
        print(f"   Content: {len(result.get('content', ''))} characters")
    else:
        print("❌ Invalid result structure")
        
except Exception as e:
    print(f"❌ Pipeline Failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - READY TO USE!")
print("=" * 60)

# COMMON ISSUES & SOLUTIONS

print("\n📋 COMMON ISSUES & SOLUTIONS:\n")

issues = {
    "Generation failed: Unknown error": [
        "1. Check if .env file exists with GOOGLE_API_KEY",
        "2. Verify API key is valid (test at https://aistudio.google.com)",
        "3. Make sure you have internet connection",
        "4. Check if gemini-2.5-flash is available",
        "5. Try restarting Streamlit app: Ctrl+C then streamlit run app.py"
    ],
    "Module not found error": [
        "1. Run: pip install -r requirements.txt",
        "2. Make sure you're in the correct directory",
        "3. Check Python version is 3.8+"
    ],
    "API Key error": [
        "1. Go to https://aistudio.google.com",
        "2. Create new API key",
        "3. Copy-paste in .env file",
        "4. Restart Streamlit"
    ],
    "Connection timeout": [
        "1. Check internet connection",
        "2. Try using VPN if Google is blocked",
        "3. Check firewall settings"
    ]
}

for issue, solutions in issues.items():
    print(f"🔴 {issue}")
    for solution in solutions:
        print(f"   {solution}")
    print()
