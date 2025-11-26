"""Test GitHub PR Review Feature"""
import asyncio
from app.services.review_service import ReviewService
from app.config import settings

async def test_github_pr():
    """Test GitHub PR review with a small real PR"""
    print("\n" + "="*60)
    print("TESTING GITHUB PR REVIEW")
    print("="*60)
    
    # Use a small, simple PR from a public repo
    repo_owner = "octocat"  # GitHub's test account
    repo_name = "Hello-World"
    pr_number = 1
    
    print(f"\nTesting with: {repo_owner}/{repo_name} PR#{pr_number}")
    print(f"GitHub Token: {'✅ Configured' if settings.GITHUB_TOKEN and settings.GITHUB_TOKEN != 'ghp_your-github-token-here' else '❌ Not configured'}")
    
    if not settings.GITHUB_TOKEN or settings.GITHUB_TOKEN == "ghp_your-github-token-here":
        print("\n⚠️  WARNING: No valid GitHub token configured!")
        print("   GitHub PR review will fail without a token.")
        print("   To test this feature:")
        print("   1. Go to https://github.com/settings/tokens")
        print("   2. Generate a new token with 'repo' scope")
        print("   3. Add it to .env as GITHUB_TOKEN=your_token")
        return False
    
    try:
        review_service = ReviewService()
        
        print("\n📡 Fetching PR from GitHub...")
        comments, summary, metadata = await review_service.review_pull_request(
            repo_owner=repo_owner,
            repo_name=repo_name,
            pr_number=pr_number,
            github_token=settings.GITHUB_TOKEN
        )
        
        print(f"\n✅ GitHub PR Review Completed!")
        print(f"\n📊 Results:")
        print(f"   PR Title: {metadata.get('pr_title', 'N/A')}")
        print(f"   Files Changed: {metadata.get('files_changed', 0)}")
        print(f"   Total Issues Found: {summary.total_issues}")
        print(f"   Critical: {summary.critical}")
        print(f"   High: {summary.high}")
        print(f"   Medium: {summary.medium}")
        print(f"   Low: {summary.low}")
        
        if len(comments) > 0:
            print(f"\n   Sample Review Comments:")
            for i, comment in enumerate(comments[:3], 1):
                print(f"   {i}. [{comment.severity}] {comment.file}: {comment.issue[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ GitHub PR Review Failed!")
        print(f"   Error: {str(e)}")
        
        if "Bad credentials" in str(e):
            print("\n   Issue: Invalid GitHub token")
            print("   Solution: Update GITHUB_TOKEN in .env with a valid token")
        elif "Not Found" in str(e):
            print("\n   Issue: PR or repository not found")
            print("   Solution: Check repo_owner, repo_name, and pr_number")
        elif "rate limit" in str(e).lower():
            print("\n   Issue: GitHub API rate limit exceeded")
            print("   Solution: Wait or use authenticated requests")
        
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_github_pr())
