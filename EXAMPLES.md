# API Usage Examples

## Python Client Example

```python
import requests
import json

# Base URL
API_URL = "http://localhost:8000"

# Example 1: Review a GitHub PR
def review_github_pr():
    url = f"{API_URL}/api/v1/review/pr"
    
    payload = {
        "repo_owner": "facebook",
        "repo_name": "react",
        "pr_number": 28000,
        "github_token": "ghp_your_token_here"  # Optional
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        
        # Print summary
        summary = result["review_summary"]
        print(f"Total Issues: {summary['total_issues']}")
        print(f"Critical: {summary['critical']}")
        print(f"High: {summary['high']}")
        print(f"Medium: {summary['medium']}")
        print(f"Low: {summary['low']}")
        
        # Print detailed reviews
        for review in result["reviews"]:
            print(f"\n{review['severity'].upper()}: {review['issue']}")
            print(f"File: {review['file']}, Line: {review['line']}")
            print(f"Suggestion: {review['suggestion']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())


# Example 2: Review a diff
def review_diff():
    url = f"{API_URL}/api/v1/review/diff"
    
    diff_content = """
diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -10,7 +10,7 @@
 def login(username, password):
-    query = "SELECT * FROM users WHERE username = '" + username + "'"
+    query = f"SELECT * FROM users WHERE username = '{username}'"
     result = db.execute(query)
     return result
"""
    
    payload = {
        "diff_content": diff_content,
        "language": "python",
        "context": "User authentication module"
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(json.dumps(result, indent=2))
    else:
        print(f"Error: {response.status_code}")


# Example 3: Get agent information
def get_agents():
    url = f"{API_URL}/api/v1/agents"
    response = requests.get(url)
    
    if response.status_code == 200:
        agents = response.json()["agents"]
        for agent in agents:
            print(f"\n{agent['name']}")
            print(f"Focus: {agent['focus']}")
            print(f"Categories: {', '.join(agent['categories'])}")


if __name__ == "__main__":
    # Review GitHub PR
    review_github_pr()
    
    # Review diff
    # review_diff()
    
    # Get agents info
    # get_agents()
```

## cURL Examples

### Review GitHub PR
```bash
curl -X POST "http://localhost:8000/api/v1/review/pr" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "facebook",
    "repo_name": "react",
    "pr_number": 28000,
    "github_token": "ghp_your_token"
  }'
```

### Review Diff
```bash
curl -X POST "http://localhost:8000/api/v1/review/diff" \
  -H "Content-Type: application/json" \
  -d '{
    "diff_content": "diff --git a/test.py b/test.py\n...",
    "language": "python"
  }'
```

### Health Check
```bash
curl "http://localhost:8000/api/v1/health"
```

### List Agents
```bash
curl "http://localhost:8000/api/v1/agents"
```

## JavaScript/Node.js Example

```javascript
const axios = require('axios');

const API_URL = 'http://localhost:8000';

async function reviewPR(owner, repo, prNumber, token) {
  try {
    const response = await axios.post(`${API_URL}/api/v1/review/pr`, {
      repo_owner: owner,
      repo_name: repo,
      pr_number: prNumber,
      github_token: token
    });
    
    const result = response.data;
    console.log('Summary:', result.review_summary);
    console.log('Total Issues:', result.reviews.length);
    
    // Filter critical issues
    const critical = result.reviews.filter(r => r.severity === 'critical');
    console.log('Critical Issues:', critical.length);
    
    return result;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

// Usage
reviewPR('facebook', 'react', 28000, 'ghp_your_token');
```

## Webhook Integration

### GitHub Webhook Setup

1. Go to your repository settings → Webhooks → Add webhook
2. Set Payload URL: `https://your-domain.com/api/v1/webhook/github`
3. Set Content type: `application/json`
4. Set Secret: Your webhook secret from `.env`
5. Select events: Pull requests
6. Save webhook

### Webhook Handler (Future Enhancement)

```python
@app.post("/api/v1/webhook/github")
async def github_webhook(request: Request):
    """Handle GitHub webhook events"""
    payload = await request.json()
    
    if payload.get("action") in ["opened", "synchronize"]:
        pr = payload["pull_request"]
        
        # Trigger async review
        await review_service.review_pull_request(
            repo_owner=payload["repository"]["owner"]["login"],
            repo_name=payload["repository"]["name"],
            pr_number=pr["number"]
        )
    
    return {"status": "processed"}
```

## Response Format

### Success Response
```json
{
  "pr_number": 123,
  "repository": "owner/repo",
  "review_summary": {
    "total_issues": 15,
    "critical": 2,
    "high": 5,
    "medium": 6,
    "low": 2,
    "info": 0,
    "files_reviewed": 8,
    "lines_analyzed": 450
  },
  "reviews": [
    {
      "agent": "Security Analyst",
      "file": "app/auth.py",
      "line": 45,
      "severity": "critical",
      "category": "security",
      "issue": "SQL Injection vulnerability detected",
      "suggestion": "Use parameterized queries or an ORM",
      "code_snippet": null,
      "confidence": 0.95
    }
  ],
  "metadata": {
    "pr_title": "Add user authentication",
    "pr_author": "developer",
    "base_branch": "main",
    "head_branch": "feature/auth"
  },
  "reviewed_at": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
  "error": "Failed to fetch PR",
  "detail": "API rate limit exceeded",
  "timestamp": "2024-01-15T10:30:00Z"
}
```
