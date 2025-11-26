# Deployment Guide

## Railway Deployment

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login to Railway:
```bash
railway login
```

3. Initialize project:
```bash
railway init
```

4. Add environment variables in Railway dashboard:
- `OPENAI_API_KEY`
- `GITHUB_TOKEN`
- Other variables from `.env.example`

5. Deploy:
```bash
railway up
```

## Render Deployment

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: pr-review-agent
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: GITHUB_TOKEN
        sync: false
```

2. Connect GitHub repo to Render
3. Add environment variables in Render dashboard
4. Deploy automatically on push

## Docker Deployment

1. Build image:
```bash
docker build -t pr-review-agent .
```

2. Run container:
```bash
docker run -p 8000:8000 --env-file .env pr-review-agent
```

3. Or use docker-compose:
```bash
docker-compose up -d
```

## Vercel Deployment

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "app/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/main.py"
    }
  ]
}
```

3. Deploy:
```bash
vercel
```

## Environment Variables Required

- `OPENAI_API_KEY`: OpenAI API key (required)
- `GITHUB_TOKEN`: GitHub personal access token (optional but recommended)
- `ENVIRONMENT`: production/development
- `LOG_LEVEL`: INFO/DEBUG/WARNING/ERROR

## Post-Deployment

1. Test health endpoint: `https://your-domain.com/api/v1/health`
2. Access API docs: `https://your-domain.com/docs`
3. Test demo UI: `https://your-domain.com/`

## Performance Optimization

- Enable Redis for caching (set `REDIS_ENABLED=true`)
- Increase `WORKERS` for production
- Set appropriate `RATE_LIMIT_PER_MINUTE`
- Configure `MAX_PR_SIZE` based on your needs
