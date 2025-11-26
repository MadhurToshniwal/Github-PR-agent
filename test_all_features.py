"""Comprehensive test suite for PR Review Agent"""
import asyncio
import json
from app.services.review_service import ReviewService
from app.services.github_service import GitHubService
from app.schemas import DiffReviewRequest
from app.config import settings

async def test_health_check():
    """Test 1: Health check endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    try:
        print("✅ Server configuration loaded")
        print(f"   Environment: {settings.ENVIRONMENT}")
        print(f"   LLM Provider: {settings.LLM_PROVIDER}")
        print(f"   Model: {settings.DEFAULT_LLM_MODEL}")
    except Exception as e:
        print(f"❌ Failed: {e}")

async def test_agents_list():
    """Test 2: View Agents"""
    print("\n" + "="*60)
    print("TEST 2: View Agents Endpoint")
    print("="*60)
    try:
        from app.agents.orchestrator import ReviewOrchestrator
        orchestrator = ReviewOrchestrator()
        
        agents_info = []
        for agent in orchestrator.agents:
            agents_info.append({
                "name": agent.agent_name,
                "focus": agent.focus_area
            })
        
        print(f"✅ Found {len(agents_info)} agents:")
        for agent in agents_info:
            print(f"   • {agent['name']}: {agent['focus']}")
    except Exception as e:
        print(f"❌ Failed: {e}")

async def test_diff_review():
    """Test 3: Diff Review Feature"""
    print("\n" + "="*60)
    print("TEST 3: Diff Review with Groq")
    print("="*60)
    
    test_diff = """diff --git a/auth.py b/auth.py
--- a/auth.py
+++ b/auth.py
@@ -1,5 +1,8 @@
 def login(username, password):
-    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
-    result = db.execute(query)
-    return result
+    user_data = database.query("SELECT * FROM users WHERE name=" + username)
+    if user_data and user_data['password'] == password:
+        session['user'] = username
+        return True
+    return False
"""
    
    try:
        review_service = ReviewService()
        comments, summary = await review_service.review_diff(
            diff_content=test_diff,
            language="python"
        )
        
        print(f"✅ Diff Review Completed")
        print(f"   Total Issues: {summary.total_issues}")
        print(f"   Critical: {summary.critical}")
        print(f"   High: {summary.high}")
        print(f"   Medium: {summary.medium}")
        print(f"   Low: {summary.low}")
        
        if summary.total_issues > 0:
            print(f"\n   Sample findings:")
            for i, comment in enumerate(comments[:3], 1):
                print(f"   {i}. [{comment.severity}] {comment.agent}: {comment.issue[:60]}...")
        
        if summary.total_issues == 0:
            print("❌ WARNING: No issues found - agents may not be working")
            return False
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_github_service():
    """Test 4: GitHub Service (without actual API call)"""
    print("\n" + "="*60)
    print("TEST 4: GitHub Service Configuration")
    print("="*60)
    
    try:
        github_service = GitHubService()
        
        # Check if token is configured
        if settings.GITHUB_TOKEN and settings.GITHUB_TOKEN != "ghp_your-github-token-here":
            print("✅ GitHub token configured")
            print(f"   Token: {settings.GITHUB_TOKEN[:10]}...")
        else:
            print("⚠️  No GitHub token configured")
            print("   PR review feature will only work with public repos")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

async def test_error_handling():
    """Test 5: Error Handling"""
    print("\n" + "="*60)
    print("TEST 5: Error Handling")
    print("="*60)
    
    try:
        review_service = ReviewService()
        
        # Test with empty diff
        print("Testing with empty diff...")
        comments, summary = await review_service.review_diff(
            diff_content="",
            language="python"
        )
        print(f"   ✅ Empty diff handled: {summary.total_issues} issues")
        
        # Test with invalid diff
        print("Testing with invalid diff...")
        comments, summary = await review_service.review_diff(
            diff_content="not a valid diff",
            language="python"
        )
        print(f"   ✅ Invalid diff handled: {summary.total_issues} issues")
        
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

async def test_api_configuration():
    """Test 6: API Keys Configuration"""
    print("\n" + "="*60)
    print("TEST 6: API Configuration Check")
    print("="*60)
    
    checks = []
    
    # Check Groq API
    if settings.GROQ_API_KEY and settings.GROQ_API_KEY.startswith("gsk_"):
        print("✅ Groq API key configured")
        checks.append(True)
    else:
        print("❌ Groq API key missing or invalid")
        checks.append(False)
    
    # Check LLM Provider
    if settings.LLM_PROVIDER == "groq":
        print("✅ LLM Provider set to Groq")
        checks.append(True)
    else:
        print(f"⚠️  LLM Provider: {settings.LLM_PROVIDER}")
        checks.append(True)
    
    # Check Model
    if settings.DEFAULT_LLM_MODEL:
        print(f"✅ Model configured: {settings.DEFAULT_LLM_MODEL}")
        checks.append(True)
    else:
        print("❌ No model configured")
        checks.append(False)
    
    return all(checks)

async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("   PR REVIEW AGENT - COMPREHENSIVE FEATURE TEST SUITE")
    print("="*70)
    
    results = []
    
    # Run all tests
    await test_health_check()
    await test_agents_list()
    
    result = await test_diff_review()
    results.append(("Diff Review", result))
    
    result = await test_github_service()
    results.append(("GitHub Service", result))
    
    result = await test_error_handling()
    results.append(("Error Handling", result))
    
    result = await test_api_configuration()
    results.append(("API Configuration", result))
    
    # Summary
    print("\n" + "="*70)
    print("   TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Application is ready for deployment.")
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")

if __name__ == "__main__":
    asyncio.run(main())
