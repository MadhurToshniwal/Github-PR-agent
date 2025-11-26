# PR Review Agent - Complete Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ What's Working:
- ✅ **Review Diff Feature**: Analyzes code diffs with Groq AI (llama-3.3-70b-versatile)
- ✅ **GitHub PR Review**: Fetches and reviews PRs from GitHub
- ✅ **4 AI Agents**: Security, Performance, Quality, Logic analyzers
- ✅ **Web Interface**: User-friendly UI at http://localhost:8000
- ✅ **API Endpoints**: `/api/v1/review/diff`, `/api/v1/review/pr`, `/api/v1/agents`, `/health`
- ✅ **Error Handling**: Graceful handling of invalid inputs
- ✅ **LangChain Integration**: Token tracking and cost monitoring

### 🔧 Current Configuration:
- **Framework**: LangChain 0.1.20
- **LLM Provider**: Groq (faster & cheaper than OpenAI)
- **Model**: llama-3.3-70b-versatile
- **Backend**: FastAPI 0.109.0
- **Python**: 3.10+

---

## 🚀 DEPLOYMENT OPTIONS

### Option 1: Local Development Deployment (Recommended for Demo)

#### Step 1: Verify Environment
```powershell
# Check Python version
python --version  # Should be 3.10+

# Verify all dependencies installed
pip list | findstr "fastapi langchain groq uvicorn"
```

#### Step 2: Configure Environment Variables
```powershell
# Edit .env file - ensure these are set:
GROQ_API_KEY=gsk_your_actual_groq_key_here
GITHUB_TOKEN=ghp_your_github_token_here
LLM_PROVIDER=groq
DEFAULT_LLM_MODEL=llama-3.3-70b-versatile
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

#### Step 3: Start Production Server
```powershell
# Production mode with Uvicorn
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# OR for demo with auto-reload
python -m uvicorn app.main:app --reload --port 8000
```

#### Step 4: Verify Deployment
```powershell
# Test health endpoint
curl http://localhost:8000/health

# Test agents endpoint
curl http://localhost:8000/api/v1/agents

# Open web interface
start http://localhost:8000
```

**✅ Ready for Demo Video!**

---

### Option 2: Docker Deployment (Production-Ready)

#### Step 1: Create Dockerfile
```dockerfile
# Create D:\lyzr\Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### Step 2: Create docker-compose.yml
```yaml
# Create D:\lyzr\docker-compose.yml

version: '3.8'

services:
  pr-review-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - LLM_PROVIDER=groq
      - DEFAULT_LLM_MODEL=llama-3.3-70b-versatile
      - ENVIRONMENT=production
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

#### Step 3: Deploy with Docker
```powershell
# Build image
docker build -t pr-review-agent .

# Run container
docker-compose up -d

# Check logs
docker-compose logs -f

# Access at http://localhost:8000
```

---

### Option 3: Cloud Deployment (Render/Railway/Heroku)

#### For Render.com:

1. **Create `render.yaml`:**
```yaml
services:
  - type: web
    name: pr-review-agent
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GROQ_API_KEY
        sync: false
      - key: GITHUB_TOKEN
        sync: false
      - key: LLM_PROVIDER
        value: groq
      - key: DEFAULT_LLM_MODEL
        value: llama-3.3-70b-versatile
      - key: ENVIRONMENT
        value: production
```

2. **Deploy:**
   - Push code to GitHub
   - Connect Render to your GitHub repo
   - Add environment variables in Render dashboard
   - Deploy!

#### For Railway.app:

1. **Push to GitHub**
2. **Connect Railway to GitHub repo**
3. **Add environment variables:**
   - `GROQ_API_KEY`
   - `GITHUB_TOKEN`
   - `LLM_PROVIDER=groq`
   - `DEFAULT_LLM_MODEL=llama-3.3-70b-versatile`
4. **Deploy automatically**

---

### Option 4: Azure/AWS/GCP Deployment

#### Azure App Service:
```powershell
# Install Azure CLI
az login

# Create resource group
az group create --name PRReviewAgent --location eastus

# Create App Service plan
az appservice plan create --name PRReviewPlan --resource-group PRReviewAgent --sku B1 --is-linux

# Create web app
az webapp create --resource-group PRReviewAgent --plan PRReviewPlan --name pr-review-agent --runtime "PYTHON:3.10"

# Configure app settings
az webapp config appsettings set --resource-group PRReviewAgent --name pr-review-agent --settings GROQ_API_KEY="your_key" GITHUB_TOKEN="your_token"

# Deploy
az webapp up --name pr-review-agent --resource-group PRReviewAgent
```

---

## 🔐 Security Checklist for Production

- [ ] **Environment Variables**: Never commit `.env` to Git
- [ ] **API Keys**: Use secrets management (Azure Key Vault, AWS Secrets Manager)
- [ ] **HTTPS**: Enable SSL/TLS certificates
- [ ] **Rate Limiting**: Already enabled in code (60 requests/minute)
- [ ] **CORS**: Configure allowed origins in `app/main.py`
- [ ] **Logging**: Set `LOG_LEVEL=WARNING` in production
- [ ] **Debug Mode**: Set `DEBUG=false` in production

---

## 📊 Monitoring & Maintenance

### Health Check
```bash
curl http://your-domain.com/health
```

### View Logs
```powershell
# Local
tail -f logs/app.log

# Docker
docker-compose logs -f

# Cloud
Check provider's logging dashboard
```

### Performance Monitoring
- Monitor Groq API usage at https://console.groq.com
- Track response times in FastAPI docs: `http://your-domain.com/docs`
- Check token usage in application logs

---

## 🎯 Post-Deployment Verification

### Test All Features:

1. **Health Check:**
   ```bash
   curl http://your-domain.com/health
   ```

2. **View Agents:**
   ```bash
   curl http://your-domain.com/api/v1/agents
   ```

3. **Review Diff (Web UI):**
   - Open browser to `http://your-domain.com`
   - Click "Review Diff"
   - Paste sample code diff
   - Verify results show Critical/High/Medium/Low counts

4. **GitHub PR Review (Web UI):**
   - Click "Review GitHub PR"
   - Enter: `octocat/Hello-World` PR #1
   - Verify review completes successfully

---

## 🆘 Troubleshooting

### Issue: "Model decommissioned" error
**Solution:** Update `.env` to use `llama-3.3-70b-versatile`

### Issue: "Bad credentials" for GitHub
**Solution:** Generate new GitHub token at https://github.com/settings/tokens

### Issue: No issues found in reviews
**Solution:** Check GROQ_API_KEY is valid and has credits

### Issue: Server won't start
**Solution:** 
```powershell
# Kill any process on port 8000
Get-Process -Name python | Stop-Process -Force

# Restart server
python -m uvicorn app.main:app --reload --port 8000
```

---

## 📈 Scaling Recommendations

For high-traffic production:

1. **Use Redis** for rate limiting:
   ```env
   REDIS_ENABLED=true
   REDIS_URL=redis://localhost:6379/0
   ```

2. **Increase Workers:**
   ```bash
   uvicorn app.main:app --workers 8
   ```

3. **Add Load Balancer** (nginx/AWS ALB)

4. **Enable Caching** for repeated PR reviews

5. **Use Async Database** for storing review history

---

## ✅ Deployment Complete!

Your PR Review Agent is now production-ready and deployed!

**Next Steps:**
1. ✅ Test all features
2. 📹 Record demo video (see DEMO_VIDEO_SCRIPT.md)
3. 📝 Document any custom configurations
4. 🎉 Share with users!
