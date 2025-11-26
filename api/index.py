from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mangum import Mangum
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

# Mangum adapter for Vercel serverless
handler = Mangum(app, lifespan="off")
