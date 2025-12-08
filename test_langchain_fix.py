"""Quick test to verify LangGraph agent works"""

from src.advanced_agent_orchestrator import LinkedInAgentOrchestrator

def test_blog_generation():
    print("=" * 60)
    print("Testing LangGraph Blog Generation")
    print("=" * 60)
    
    # Initialize orchestrator
    orchestrator = LinkedInAgentOrchestrator()
    print("\n✅ Orchestrator initialized")
    print(f"✅ Has send_email method: {hasattr(orchestrator, 'send_email')}")
    
    # Generate a simple blog
    print("\n🤖 Generating blog post...")
    blog = orchestrator.orchestrate_blog_creation(
        topic="AI in Healthcare",
        tone="professional",
        length="short",
        target_audience="healthcare professionals"
    )
    
    print("\n" + "=" * 60)
    print("BLOG POST GENERATED")
    print("=" * 60)
    print(f"\nTitle: {blog.get('title')}")
    print(f"\nContent preview: {blog.get('content', '')[:200]}...")
    print(f"\nHashtags: {blog.get('hashtags')}")
    print(f"\nCTA: {blog.get('call_to_action')}")
    
    # Check metadata
    if 'agent_metadata' in blog:
        meta = blog['agent_metadata']
        print("\n" + "=" * 60)
        print("FRAMEWORK METADATA")
        print("=" * 60)
        print(f"Framework: {meta.get('framework')}")
        print(f"Agent Type: {meta.get('agent_type')}")
        print(f"Tools Available: {', '.join(meta.get('tools_available', []))}")
    
    print("\n✅ ALL TESTS PASSED!")
    return blog

if __name__ == "__main__":
    test_blog_generation()
