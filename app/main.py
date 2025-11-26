from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import time
from typing import Dict
from pathlib import Path

from app.config import settings
from app.schemas import (
    PRReviewRequest,
    DiffReviewRequest,
    PRReviewResponse,
    HealthResponse,
    ErrorResponse,
    ReviewSummary
)
from app.services.review_service import ReviewService
from app.logger import setup_logger

logger = setup_logger(__name__)

# Rate limiting storage (in production, use Redis)
rate_limit_storage: Dict[str, list] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    yield
    
    logger.info("Shutting down application")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Automated GitHub PR Review Agent with Multi-Agent AI System",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
review_service = ReviewService()

# Mount static files
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


# Dependency for rate limiting
async def check_rate_limit(request: Request):
    """Simple rate limiting middleware"""
    if not settings.RATE_LIMIT_ENABLED:
        return
    
    client_ip = request.client.host
    current_time = time.time()
    
    # Clean old entries
    if client_ip in rate_limit_storage:
        rate_limit_storage[client_ip] = [
            req_time for req_time in rate_limit_storage[client_ip]
            if current_time - req_time < 60
        ]
    else:
        rate_limit_storage[client_ip] = []
    
    # Check limit
    if len(rate_limit_storage[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - serves demo UI"""
    static_path = Path(__file__).parent.parent / "static" / "index.html"
    if static_path.exists():
        return FileResponse(static_path)
    return {
        "message": "PR Review Agent API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health"
    }


@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION
    )


@app.post(
    "/api/v1/review/pr",
    response_model=PRReviewResponse,
    tags=["Review"],
    dependencies=[Depends(check_rate_limit)]
)
async def review_pull_request(request: PRReviewRequest):
    """
    Review a GitHub Pull Request
    
    Analyzes code changes in a PR using multiple specialized AI agents:
    - Security Analyst: Identifies security vulnerabilities
    - Performance Reviewer: Detects performance issues
    - Code Quality Inspector: Checks code quality and best practices
    - Logic Analyzer: Finds logic errors and edge cases
    
    Returns comprehensive review with categorized, prioritized issues.
    """
    try:
        logger.info(f"Received PR review request: {request.repo_owner}/{request.repo_name} PR#{request.pr_number}")
        
        # Perform review
        comments, summary, metadata = await review_service.review_pull_request(
            repo_owner=request.repo_owner,
            repo_name=request.repo_name,
            pr_number=request.pr_number,
            github_token=request.github_token
        )
        
        # Build response
        response = PRReviewResponse(
            pr_number=request.pr_number,
            repository=f"{request.repo_owner}/{request.repo_name}",
            review_summary=summary,
            reviews=comments,
            metadata=metadata
        )
        
        logger.info(f"PR review completed: {len(comments)} comments generated")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error reviewing PR: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post(
    "/api/v1/review/diff",
    response_model=PRReviewResponse,
    tags=["Review"],
    dependencies=[Depends(check_rate_limit)]
)
async def review_diff(request: DiffReviewRequest):
    """
    Review a raw Git diff
    
    Analyzes code changes from a raw diff input.
    Useful for reviewing changes before creating a PR or for local development.
    """
    try:
        logger.info("Received diff review request")
        
        # Perform review
        comments, summary = await review_service.review_diff(
            diff_content=request.diff_content,
            language=request.language,
            context=request.context
        )
        
        # Build response
        response = PRReviewResponse(
            pr_number=0,
            repository="diff-review",
            review_summary=summary,
            reviews=comments,
            metadata={
                "language": request.language,
                "context": request.context
            }
        )
        
        logger.info(f"Diff review completed: {len(comments)} comments generated")
        return response
        
    except Exception as e:
        logger.error(f"Error reviewing diff: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/v1/agents", tags=["Info"])
async def list_agents():
    """List all available review agents"""
    return {
        "agents": [
            {
                "name": "Security Analyst",
                "focus": "Security vulnerabilities and risks",
                "categories": ["SQL Injection", "XSS", "Authentication", "Secrets", "CSRF"]
            },
            {
                "name": "Performance Reviewer",
                "focus": "Performance and efficiency",
                "categories": ["Complexity", "Database", "Memory", "Caching", "Loops"]
            },
            {
                "name": "Code Quality Inspector",
                "focus": "Code quality and maintainability",
                "categories": ["SOLID", "DRY", "Readability", "Documentation", "Style"]
            },
            {
                "name": "Logic Analyzer",
                "focus": "Logic correctness and edge cases",
                "categories": ["Bugs", "Edge Cases", "Null Safety", "Validation", "Comparisons"]
            }
        ]
    }


@app.get("/api/v1/stats", tags=["Info"])
async def get_stats():
    """Get API usage statistics"""
    total_requests = sum(len(reqs) for reqs in rate_limit_storage.values())
    
    return {
        "total_requests": total_requests,
        "active_ips": len(rate_limit_storage),
        "rate_limit_per_minute": settings.RATE_LIMIT_PER_MINUTE
    }


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    error_data = ErrorResponse(
        error=exc.detail,
        detail=str(exc)
    ).dict()
    # Convert datetime to string for JSON serialization
    if 'timestamp' in error_data:
        error_data['timestamp'] = error_data['timestamp'].isoformat()
    return JSONResponse(
        status_code=exc.status_code,
        content=error_data
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    error_data = ErrorResponse(
        error="Internal server error",
        detail=str(exc) if settings.DEBUG else None
    ).dict()
    # Convert datetime to string for JSON serialization
    if 'timestamp' in error_data:
        error_data['timestamp'] = error_data['timestamp'].isoformat()
    return JSONResponse(
        status_code=500,
        content=error_data
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
