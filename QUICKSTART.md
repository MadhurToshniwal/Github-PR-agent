# ⚡ Quick Setup Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Prerequisites Check
```bash
# Check Python version (need 3.11+)
python --version

# If not installed, download from python.org
```

### Step 2: Clone & Setup
```bash
# Navigate to project directory
cd d:\lyzr

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
# Copy example environment file
copy .env.example .env

# Edit .env and add your API keys:
# - OPENAI_API_KEY=sk-your-key-here
# - GITHUB_TOKEN=ghp-your-token-here (optional)
```

### Step 4: Run the Application
```bash
# Option 1: Using the quick start script
python start.py

# Option 2: Direct uvicorn command
python -m uvicorn app.main:app --reload --port 8000
```

### Step 5: Test It Out
1. Open browser: http://localhost:8000
2. Try the demo UI
3. Or visit API docs: http://localhost:8000/docs

---

## 🐳 Docker Quick Start

### One-Command Setup
```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Manual Docker
```bash
# Build
docker build -t pr-review-agent .

# Run
docker run -p 8000:8000 --env-file .env pr-review-agent
```

---

## 🧪 Run Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html
```

---

## 🌐 Deploy to Cloud

### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Render
1. Connect GitHub repo to Render
2. Add environment variables in dashboard
3. Deploy automatically

### Docker Hub
```bash
# Login
docker login

# Tag and push
docker tag pr-review-agent yourusername/pr-review-agent
docker push yourusername/pr-review-agent
```

---

## 🔧 Troubleshooting

### Issue: Module not found
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Issue: OpenAI API error
```bash
# Check .env file has valid OPENAI_API_KEY
# Verify API key at platform.openai.com
```

### Issue: GitHub rate limit
```bash
# Add GITHUB_TOKEN to .env for higher limits
# Get token from github.com/settings/tokens
```

### Issue: Port already in use
```bash
# Change port in .env or use different port:
uvicorn app.main:app --port 8001
```

---

## 📝 Environment Variables Quick Reference

### Required
- `OPENAI_API_KEY` - Your OpenAI API key

### Optional but Recommended
- `GITHUB_TOKEN` - For private repos and higher rate limits

### Configuration
- `ENVIRONMENT` - development/production (default: development)
- `DEBUG` - true/false (default: true)
- `LOG_LEVEL` - DEBUG/INFO/WARNING/ERROR (default: INFO)
- `PORT` - Server port (default: 8000)
- `WORKERS` - Number of workers (default: 4)

### Advanced
- `REDIS_URL` - Redis connection (default: redis://localhost:6379/0)
- `REDIS_ENABLED` - Enable Redis caching (default: false)
- `RATE_LIMIT_PER_MINUTE` - API rate limit (default: 60)
- `MAX_PR_SIZE` - Max files in PR (default: 1000)

---

## 🎯 Quick API Test

### Using cURL
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Review a PR
curl -X POST http://localhost:8000/api/v1/review/pr \
  -H "Content-Type: application/json" \
  -d '{
    "repo_owner": "facebook",
    "repo_name": "react",
    "pr_number": 28000
  }'
```

### Using Python
```python
import requests

response = requests.get("http://localhost:8000/api/v1/health")
print(response.json())
```

---

## 📚 Next Steps

1. ✅ Run the application locally
2. ✅ Test with the demo UI
3. ✅ Review the API documentation at /docs
4. ✅ Check out EXAMPLES.md for more usage patterns
5. ✅ Read ARCHITECTURE.md for technical deep dive
6. ✅ Deploy to cloud platform

---

## 💡 Pro Tips

### Speed up reviews
- Use GITHUB_TOKEN for faster API access
- Enable Redis caching for repeated reviews
- Adjust MAX_PR_SIZE based on your needs

### Better results
- Provide context in diff reviews
- Use for PRs with 1-50 files for best results
- Review security-critical code first

### Development
- Use `--reload` flag for auto-restart during development
- Check logs for detailed agent reasoning
- Run tests before deployment

---

## 🆘 Need Help?

- 📖 Full documentation in README.md
- 🏗️ Architecture details in ARCHITECTURE.md  
- 📘 API examples in EXAMPLES.md
- 🚀 Deployment guide in DEPLOYMENT.md
- 💬 Open an issue on GitHub

---

**Happy Reviewing! 🎉**
