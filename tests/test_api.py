import pytest
import asyncio
from httpx import AsyncClient
from app.main import app


@pytest.fixture
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    """Create async test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint"""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test root endpoint"""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_list_agents(client):
    """Test agents listing endpoint"""
    response = await client.get("/api/v1/agents")
    assert response.status_code == 200
    data = response.json()
    assert "agents" in data
    assert len(data["agents"]) == 4  # 4 specialized agents


@pytest.mark.asyncio
async def test_review_pr_missing_fields(client):
    """Test PR review with missing required fields"""
    response = await client.post("/api/v1/review/pr", json={})
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_review_diff_basic(client):
    """Test basic diff review"""
    diff = """diff --git a/test.py b/test.py
--- a/test.py
+++ b/test.py
@@ -1,3 +1,3 @@
 def hello():
-    print("Hello")
+    print("Hello World")
"""
    
    response = await client.post(
        "/api/v1/review/diff",
        json={
            "diff_content": diff,
            "language": "python"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "review_summary" in data
    assert "reviews" in data


@pytest.mark.asyncio
async def test_stats_endpoint(client):
    """Test stats endpoint"""
    response = await client.get("/api/v1/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_requests" in data
