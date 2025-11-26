import pytest
import asyncio
from app.agents.orchestrator import ReviewOrchestrator
from app.schemas import SeverityLevel, CategoryType


@pytest.fixture
def orchestrator():
    """Create orchestrator instance"""
    return ReviewOrchestrator()


def test_orchestrator_initialization(orchestrator):
    """Test orchestrator initialization"""
    assert orchestrator is not None
    assert len(orchestrator.agents) == 4


def test_calculate_similarity(orchestrator):
    """Test similarity calculation"""
    text1 = "This is a security vulnerability in the code"
    text2 = "This is a security issue in the code"
    
    similarity = orchestrator._calculate_similarity(text1, text2)
    assert 0.0 <= similarity <= 1.0
    assert similarity > 0.5  # Should be similar


def test_calculate_similarity_different(orchestrator):
    """Test similarity with different texts"""
    text1 = "Security vulnerability detected"
    text2 = "Performance issue found"
    
    similarity = orchestrator._calculate_similarity(text1, text2)
    assert similarity < 0.5  # Should be different


def test_sort_comments(orchestrator):
    """Test comment sorting by severity"""
    from app.schemas import ReviewComment
    
    comments = [
        ReviewComment(
            agent="Test",
            file="test.py",
            severity=SeverityLevel.LOW,
            category=CategoryType.QUALITY,
            issue="Low issue",
            suggestion="Fix it",
            confidence=0.8
        ),
        ReviewComment(
            agent="Test",
            file="test.py",
            severity=SeverityLevel.CRITICAL,
            category=CategoryType.SECURITY,
            issue="Critical issue",
            suggestion="Fix it",
            confidence=0.9
        ),
        ReviewComment(
            agent="Test",
            file="test.py",
            severity=SeverityLevel.MEDIUM,
            category=CategoryType.PERFORMANCE,
            issue="Medium issue",
            suggestion="Fix it",
            confidence=0.7
        )
    ]
    
    sorted_comments = orchestrator._sort_comments(comments)
    
    # Critical should be first
    assert sorted_comments[0].severity == SeverityLevel.CRITICAL
    # Low should be last
    assert sorted_comments[-1].severity == SeverityLevel.LOW


def test_generate_summary(orchestrator):
    """Test summary generation"""
    from app.schemas import ReviewComment
    
    comments = [
        ReviewComment(
            agent="Test",
            file="test.py",
            severity=SeverityLevel.CRITICAL,
            category=CategoryType.SECURITY,
            issue="Critical",
            suggestion="Fix",
            confidence=0.9
        ),
        ReviewComment(
            agent="Test",
            file="test.py",
            severity=SeverityLevel.HIGH,
            category=CategoryType.PERFORMANCE,
            issue="High",
            suggestion="Fix",
            confidence=0.8
        ),
        ReviewComment(
            agent="Test",
            file="test.py",
            severity=SeverityLevel.MEDIUM,
            category=CategoryType.QUALITY,
            issue="Medium",
            suggestion="Fix",
            confidence=0.7
        )
    ]
    
    summary = orchestrator._generate_summary(comments, files_reviewed=5, lines_analyzed=100)
    
    assert summary.total_issues == 3
    assert summary.critical == 1
    assert summary.high == 1
    assert summary.medium == 1
    assert summary.files_reviewed == 5
    assert summary.lines_analyzed == 100
