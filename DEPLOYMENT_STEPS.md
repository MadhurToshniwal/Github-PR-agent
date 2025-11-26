# 🚀 Step-by-Step Deployment Guide

## ✅ Code Successfully Pushed to GitHub!

**Repository:** https://github.com/MadhurToshniwal/Github-PR-agent

---

## 📋 Pre-Deployment Checklist

✅ **All Assignment Requirements Met:**
- ✅ Read PR diffs via GitHub API
- ✅ Read PR diffs via manual input
- ✅ Parse and understand changed lines
- ✅ Multi-agent reasoning with LangChain
- ✅ Identify logic issues
- ✅ Identify readability issues
- ✅ Identify performance issues
- ✅ Identify security issues

✅ **Application Status:**
- ✅ All 4 tests passing (4/4)
- ✅ LangChain integration working
- ✅ Groq AI configured
- ✅ GitHub API integration functional
- ✅ Web interface tested
- ✅ Code pushed to GitHub

---

## 🎯 Recommended Deployment: Railway (Easiest & Free)

### Why Railway?
- ✅ **Easiest** deployment (click & deploy)
- ✅ **Free tier** ($5/month credit)
- ✅ **Auto HTTPS** (free SSL)
- ✅ **Auto redeploy** on GitHub push
- ✅ **Built-in logs** monitoring

---

## 🚂 OPTION 1: Deploy to Railway (RECOMMENDED)

### Step 1: Get Groq API Key (If You Don't Have)

1. Visit: https://console.groq.com/
2. Sign up (free)
3. Go to **API Keys** section
4. Click **Create API Key**
5. Copy the key (starts with `gsk_...`)

### Step 2: Deploy to Railway

1. **Go to Railway:**
   - Visit: https://railway.app/
   - Click **"Login"** → Sign in with GitHub

2. **Create New Project:**
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Choose: **`MadhurToshniwal/Github-PR-agent`**

3. **Add Environment Variables:**
   Click on your deployed service → **Variables** tab → Add these:
   
   ```
   LLM_PROVIDER=groq
   GROQ_API_KEY=gsk_your_actual_groq_key_here
   DEFAULT_LLM_MODEL=llama-3.3-70b-versatile
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   PORT=8000
   ```

   **Optional (for private GitHub repos):**
   ```
   GITHUB_TOKEN=ghp_your_github_token
   ```

4. **Configure Start Command:**
   - Go to **Settings** tab
   - Find **Start Command**
   - Set to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

5. **Deploy:**
   - Railway will automatically deploy
   - Wait 2-3 minutes for build & deployment
   - Your app will be live! 🎉

6. **Get Your URL:**
   - Click **Settings** → **Generate Domain**
   - Your app URL: `https://your-app.railway.app`

### Step 3: Test Your Deployed App

```bash
# Health check
curl https://your-app.railway.app/health

# View agents
curl https://your-app.railway.app/api/v1/agents

# Or open in browser
https://your-app.railway.app
```

---

## 🎨 OPTION 2: Deploy to Render

### Step 1: Get Groq API Key (If You Don't Have)
Same as Railway Step 1 above

### Step 2: Deploy to Render

1. **Go to Render:**
   - Visit: https://render.com/
   - Sign up with GitHub

2. **Create New Web Service:**
   - Click **"New +"** → **"Web Service"**
   - Click **"Build and deploy from a Git repository"**
   - Connect your GitHub: **`MadhurToshniwal/Github-PR-agent`**

3. **Configure Service:**
   - **Name:** `pr-review-agent`
   - **Environment:** `Python 3`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables:**
   Scroll down to **Environment Variables** → Add these:
   
   ```
   LLM_PROVIDER=groq
   GROQ_API_KEY=gsk_your_actual_groq_key_here
   DEFAULT_LLM_MODEL=llama-3.3-70b-versatile
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   ```

5. **Select Plan:**
   - Choose **"Free"** plan ($0/month)
   - Note: Free tier spins down after 15 min inactivity

6. **Deploy:**
   - Click **"Create Web Service"**
   - Wait 3-5 minutes for deployment
   - Your app will be live! 🎉

7. **Get Your URL:**
   - Your app URL: `https://pr-review-agent.onrender.com`

---

## 🐳 OPTION 3: Deploy with Docker (Any Platform)

### Step 1: Build Docker Image

```bash
cd d:\lyzr

# Build image
docker build -t pr-review-agent .

# Test locally
docker run -p 8000:8000 \
  -e GROQ_API_KEY=your_key \
  -e LLM_PROVIDER=groq \
  pr-review-agent
```

### Step 2: Push to Docker Hub (Optional)

```bash
# Tag image
docker tag pr-review-agent madhurtoshniwal/pr-review-agent:latest

# Push to Docker Hub
docker push madhurtoshniwal/pr-review-agent:latest
```

### Step 3: Deploy to Any Cloud Provider

Now you can deploy this Docker image to:
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Instances**
- **DigitalOcean App Platform**
- **Heroku**

---

## 🔧 Post-Deployment Configuration

### Update GitHub Webhook (Optional - For Auto PR Reviews)

1. Go to your GitHub repository
2. Settings → Webhooks → Add webhook
3. Payload URL: `https://your-app.railway.app/api/v1/webhook`
4. Content type: `application/json`
5. Events: Select "Pull requests"
6. Active: ✅

---

## ✅ Verify Deployment

### Test 1: Health Check
```bash
curl https://your-deployed-url/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production",
  "llm_provider": "groq"
}
```

### Test 2: View Agents
```bash
curl https://your-deployed-url/api/v1/agents
```

**Expected:** List of 4 agents

### Test 3: Review Diff (Full Test)
```bash
curl -X POST https://your-deployed-url/api/v1/review/diff \
  -H "Content-Type: application/json" \
  -d '{
    "diff": "- query = \"SELECT * FROM users WHERE id=\" + user_id\n+ query = \"SELECT * FROM users WHERE id=%s\"",
    "language": "python",
    "context": "Security fix"
  }'
```

**Expected:** JSON response with security issues found

### Test 4: Web Interface

Open in browser:
```
https://your-deployed-url
```

Should see the PR Review Agent web interface with 3 tabs.

---

## 📊 Monitoring & Logs

### Railway Logs
- Go to your Railway project
- Click on your service
- View **Deployments** tab
- Click on latest deployment
- See real-time logs

### Render Logs
- Go to your Render dashboard
- Click on your web service
- Click **"Logs"** tab
- See real-time logs

---

## 🐛 Troubleshooting

### Issue 1: "Build Failed"

**Solution:** Check your `requirements.txt` has all dependencies:
```bash
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Issue 2: "Application Error" / "Service Unavailable"

**Solution:** Check environment variables are set correctly:
- `GROQ_API_KEY` is set
- `LLM_PROVIDER=groq`
- `DEFAULT_LLM_MODEL=llama-3.3-70b-versatile`

### Issue 3: "Invalid API Key"

**Solution:** 
1. Verify Groq API key is correct
2. Check for extra spaces in environment variable
3. Generate new key at https://console.groq.com/

### Issue 4: Port Binding Error

**Solution:** Use `$PORT` environment variable:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Railway/Render automatically set `$PORT`.

---

## 💰 Cost Estimation

### Railway (Free Tier)
- **Free:** $5 credit/month
- **Your app:** ~$0-2/month (depending on usage)
- **Groq API:** Free tier (100K tokens/day)
- **Total:** $0/month (within free tier)

### Render (Free Tier)
- **Free:** $0/month
- **Limitation:** Spins down after 15 min inactivity
- **Cold start:** ~30 seconds
- **Groq API:** Free tier
- **Total:** $0/month

### Docker on Cloud Run (Google)
- **Free tier:** 2 million requests/month
- **Your app:** ~$0-5/month
- **Groq API:** Free tier
- **Total:** $0-5/month

---

## 🎯 Recommended for Lyzr AI Demo

**Use Railway** because:
1. ✅ Always on (no cold starts)
2. ✅ Fast response times
3. ✅ Professional domain
4. ✅ Easy to demo
5. ✅ Auto-deploys on GitHub push

---

## 📝 Next Steps After Deployment

### 1. Update README with Live Demo Link

Add this to your GitHub README.md:

```markdown
## 🌐 Live Demo

**Try it now:** https://your-app.railway.app

No installation needed! Test the PR Review Agent in your browser.
```

### 2. Create Demo Video

Use your deployed app to record demo video showing:
- Web interface
- Reviewing code diffs
- Analyzing GitHub PRs
- All 4 agents working

### 3. Share with Lyzr AI

Email them:
- **GitHub Repo:** https://github.com/MadhurToshniwal/Github-PR-agent
- **Live Demo:** https://your-app.railway.app
- **Demo Video:** [Your YouTube/Loom link]

---

## 🎉 You're Done!

Your AI-Powered PR Review Agent is now:
- ✅ Deployed to production
- ✅ Accessible via public URL
- ✅ Auto-deploys on GitHub push
- ✅ Ready for Lyzr AI demo

---

## 📞 Support

If you need help:
1. Check Railway/Render logs
2. Test locally first: `python -m uvicorn app.main:app --reload`
3. Verify all environment variables
4. Check Groq API key is valid

---

**Made with ❤️ for Lyzr AI Backend Engineering Internship**

**Developer:** Madhur Toshniwal | madhurtoshniwal03@gmail.com
