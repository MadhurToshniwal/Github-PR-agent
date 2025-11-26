from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class SeverityLevel(str, Enum):
    """Issue severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class CategoryType(str, Enum):
    """Review category types"""
    SECURITY = "security"
    PERFORMANCE = "performance"
    QUALITY = "quality"
    LOGIC = "logic"
    STYLE = "style"
    DOCUMENTATION = "documentation"


class PRReviewRequest(BaseModel):
    """Request model for PR review"""
    repo_owner: str = Field(..., description="Repository owner")
    repo_name: str = Field(..., description="Repository name")
    pr_number: int = Field(..., gt=0, description="Pull request number")
    github_token: Optional[str] = Field(None, description="GitHub personal access token")
    
    @validator('repo_owner', 'repo_name')
    def validate_non_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class DiffReviewRequest(BaseModel):
    """Request model for direct diff review"""
    diff_content: str = Field(..., description="Git diff content")
    language: Optional[str] = Field("python", description="Programming language")
    context: Optional[str] = Field(None, description="Additional context about the changes")


class ReviewComment(BaseModel):
    """Individual review comment from an agent"""
    agent: str = Field(..., description="Name of the agent that generated this comment")
    file: str = Field(..., description="File path")
    line: Optional[int] = Field(None, description="Line number in the file")
    severity: SeverityLevel = Field(..., description="Issue severity")
    category: CategoryType = Field(..., description="Issue category")
    issue: str = Field(..., description="Description of the issue")
    suggestion: str = Field(..., description="Suggested fix or improvement")
    code_snippet: Optional[str] = Field(None, description="Relevant code snippet")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")


class ReviewSummary(BaseModel):
    """Summary statistics of the review"""
    total_issues: int = Field(0, description="Total number of issues found")
    critical: int = Field(0, description="Number of critical issues")
    high: int = Field(0, description="Number of high severity issues")
    medium: int = Field(0, description="Number of medium severity issues")
    low: int = Field(0, description="Number of low severity issues")
    info: int = Field(0, description="Number of informational items")
    files_reviewed: int = Field(0, description="Number of files reviewed")
    lines_analyzed: int = Field(0, description="Number of lines analyzed")


class PRReviewResponse(BaseModel):
    """Response model for PR review"""
    pr_number: int
    repository: str
    review_summary: ReviewSummary
    reviews: List[ReviewComment]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    reviewed_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class FileChange(BaseModel):
    """Model for a file change in a PR"""
    filename: str
    status: str  # added, modified, removed
    additions: int
    deletions: int
    changes: int
    patch: Optional[str] = None
    language: Optional[str] = None


class PRInfo(BaseModel):
    """Pull Request information"""
    number: int
    title: str
    description: Optional[str] = None
    author: str
    base_branch: str
    head_branch: str
    state: str
    files_changed: List[FileChange]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
