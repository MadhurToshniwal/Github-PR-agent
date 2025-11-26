"""Test script to debug diff review"""
import asyncio
from app.services.review_service import ReviewService
from app.schemas import DiffReviewRequest

async def test_diff_review():
    # Sample vulnerable code diff
    test_diff = """diff --git a/auth.py b/auth.py
--- a/auth.py
+++ b/auth.py
@@ -1,5 +1,8 @@
 def login(username, password):
-    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
-    result = db.execute(query)
-    return result
+    # Using string concatenation for SQL query
+    user_data = database.query("SELECT * FROM users WHERE name=" + username)
+    if user_data and user_data['password'] == password:
+        session['user'] = username
+        return True
+    return False
"""
    
    request = DiffReviewRequest(
        diff_content=test_diff,
        language="python"
    )
    
    review_service = ReviewService()
    
    print("🔍 Starting diff review...")
    print("=" * 60)
    
    comments, summary = await review_service.review_diff(
        diff_content=request.diff_content,
        language=request.language
    )
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total Issues: {summary.total_issues}")
    print(f"   Critical: {summary.critical}")
    print(f"   High: {summary.high}")
    print(f"   Medium: {summary.medium}")
    print(f"   Low: {summary.low}")
    print(f"   Info: {summary.info}")
    
    print(f"\n💬 COMMENTS FOUND: {len(comments)}")
    print("=" * 60)
    
    for i, comment in enumerate(comments, 1):
        print(f"\n{i}. [{comment.severity}] {comment.category}")
        print(f"   Agent: {comment.agent}")
        print(f"   File: {comment.file}:{comment.line}")
        print(f"   Issue: {comment.comment}")
        if comment.suggestion:
            print(f"   Fix: {comment.suggestion}")
    
    if len(comments) == 0:
        print("\n⚠️ NO COMMENTS GENERATED!")
        print("This means the agents are not finding issues.")

if __name__ == "__main__":
    asyncio.run(test_diff_review())
