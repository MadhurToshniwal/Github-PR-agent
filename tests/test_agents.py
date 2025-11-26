import pytest
from app.agents.base_agent import (
    SecurityAnalystAgent,
    PerformanceReviewerAgent,
    CodeQualityInspectorAgent,
    LogicAnalyzerAgent
)


@pytest.mark.asyncio
async def test_security_analyst_initialization():
    """Test Security Analyst agent initialization"""
    agent = SecurityAnalystAgent()
    assert agent.agent_name == "Security Analyst"
    assert agent.focus_area == "Security vulnerabilities and risks"


@pytest.mark.asyncio
async def test_performance_reviewer_initialization():
    """Test Performance Reviewer agent initialization"""
    agent = PerformanceReviewerAgent()
    assert agent.agent_name == "Performance Reviewer"
    assert agent.focus_area == "Performance and efficiency"


@pytest.mark.asyncio
async def test_code_quality_inspector_initialization():
    """Test Code Quality Inspector agent initialization"""
    agent = CodeQualityInspectorAgent()
    assert agent.agent_name == "Code Quality Inspector"
    assert agent.focus_area == "Code quality and maintainability"


@pytest.mark.asyncio
async def test_logic_analyzer_initialization():
    """Test Logic Analyzer agent initialization"""
    agent = LogicAnalyzerAgent()
    assert agent.agent_name == "Logic Analyzer"
    assert agent.focus_area == "Logic correctness and edge cases"


def test_security_analyst_system_prompt():
    """Test Security Analyst system prompt generation"""
    agent = SecurityAnalystAgent()
    prompt = agent.get_system_prompt()
    
    assert "security" in prompt.lower()
    assert "vulnerabilities" in prompt.lower()
    assert len(prompt) > 100


def test_performance_reviewer_system_prompt():
    """Test Performance Reviewer system prompt generation"""
    agent = PerformanceReviewerAgent()
    prompt = agent.get_system_prompt()
    
    assert "performance" in prompt.lower()
    assert "efficiency" in prompt.lower()
    assert len(prompt) > 100


def test_code_quality_inspector_system_prompt():
    """Test Code Quality Inspector system prompt generation"""
    agent = CodeQualityInspectorAgent()
    prompt = agent.get_system_prompt()
    
    assert "quality" in prompt.lower()
    assert "maintainability" in prompt.lower()
    assert len(prompt) > 100


def test_logic_analyzer_system_prompt():
    """Test Logic Analyzer system prompt generation"""
    agent = LogicAnalyzerAgent()
    prompt = agent.get_system_prompt()
    
    assert "logic" in prompt.lower()
    assert "correctness" in prompt.lower()
    assert len(prompt) > 100
