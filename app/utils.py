"""
Utility functions for PR Review Agent
"""

from typing import List, Dict, Any
import re
from datetime import datetime


def calculate_code_complexity(code: str) -> int:
    """
    Calculate cyclomatic complexity of code
    
    Args:
        code: Source code string
        
    Returns:
        Complexity score
    """
    complexity = 1  # Base complexity
    
    # Count decision points
    decision_keywords = [
        r'\bif\b', r'\belif\b', r'\belse\b',
        r'\bfor\b', r'\bwhile\b',
        r'\band\b', r'\bor\b',
        r'\btry\b', r'\bexcept\b', r'\bcatch\b',
        r'\bcase\b', r'\bswitch\b'
    ]
    
    for keyword in decision_keywords:
        complexity += len(re.findall(keyword, code))
    
    return complexity


def extract_function_names(code: str, language: str = "python") -> List[str]:
    """
    Extract function names from code
    
    Args:
        code: Source code string
        language: Programming language
        
    Returns:
        List of function names
    """
    functions = []
    
    if language == "python":
        pattern = r'def\s+(\w+)\s*\('
    elif language in ["javascript", "typescript"]:
        pattern = r'function\s+(\w+)\s*\('
    elif language == "java":
        pattern = r'(?:public|private|protected)?\s*\w+\s+(\w+)\s*\('
    else:
        return functions
    
    matches = re.findall(pattern, code)
    functions.extend(matches)
    
    return functions


def format_review_as_markdown(reviews: List[Dict[str, Any]]) -> str:
    """
    Format review comments as Markdown
    
    Args:
        reviews: List of review comment dictionaries
        
    Returns:
        Formatted Markdown string
    """
    markdown = "# Code Review\n\n"
    
    # Group by file
    by_file = {}
    for review in reviews:
        file = review.get('file', 'unknown')
        if file not in by_file:
            by_file[file] = []
        by_file[file].append(review)
    
    for file, file_reviews in by_file.items():
        markdown += f"## 📄 {file}\n\n"
        
        for review in file_reviews:
            severity = review.get('severity', 'info').upper()
            emoji = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢',
                'INFO': 'ℹ️'
            }.get(severity, 'ℹ️')
            
            markdown += f"### {emoji} {severity}\n\n"
            markdown += f"**Agent:** {review.get('agent', 'Unknown')}\n\n"
            
            if review.get('line'):
                markdown += f"**Line:** {review['line']}\n\n"
            
            markdown += f"**Issue:** {review.get('issue', 'No description')}\n\n"
            markdown += f"**Category:** {review.get('category', 'general')}\n\n"
            markdown += f"**Suggestion:**\n{review.get('suggestion', 'No suggestion')}\n\n"
            
            if review.get('code_snippet'):
                markdown += f"```\n{review['code_snippet']}\n```\n\n"
            
            markdown += "---\n\n"
    
    return markdown


def format_review_as_github_comment(reviews: List[Dict[str, Any]]) -> str:
    """
    Format reviews as GitHub-compatible comment
    
    Args:
        reviews: List of review comments
        
    Returns:
        GitHub-compatible markdown string
    """
    comment = "## 🤖 AI Code Review\n\n"
    
    # Summary
    severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0}
    for review in reviews:
        severity = review.get('severity', 'info')
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    comment += "### Summary\n\n"
    comment += f"- 🔴 Critical: {severity_counts.get('critical', 0)}\n"
    comment += f"- 🟠 High: {severity_counts.get('high', 0)}\n"
    comment += f"- 🟡 Medium: {severity_counts.get('medium', 0)}\n"
    comment += f"- 🟢 Low: {severity_counts.get('low', 0)}\n\n"
    
    comment += "### Detailed Findings\n\n"
    
    for idx, review in enumerate(reviews, 1):
        severity_emoji = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢',
            'info': 'ℹ️'
        }.get(review.get('severity', 'info'), 'ℹ️')
        
        comment += f"#### {idx}. {severity_emoji} {review.get('issue', 'Issue')}\n\n"
        comment += f"**File:** `{review.get('file', 'unknown')}`"
        
        if review.get('line'):
            comment += f" (Line {review['line']})"
        
        comment += f"\n\n**Category:** {review.get('category', 'general')}\n\n"
        comment += f"**Agent:** {review.get('agent', 'Unknown')}\n\n"
        comment += f"💡 **Suggestion:** {review.get('suggestion', 'No suggestion')}\n\n"
        comment += "---\n\n"
    
    comment += f"\n*Review generated at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}*\n"
    
    return comment


def sanitize_code_snippet(code: str, max_lines: int = 10) -> str:
    """
    Sanitize and truncate code snippet
    
    Args:
        code: Code snippet
        max_lines: Maximum number of lines
        
    Returns:
        Sanitized code snippet
    """
    lines = code.split('\n')
    
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines.append('... (truncated)')
    
    return '\n'.join(lines)


def detect_sensitive_data(code: str) -> List[str]:
    """
    Detect potential sensitive data in code
    
    Args:
        code: Source code
        
    Returns:
        List of potential issues
    """
    issues = []
    
    # API keys
    if re.search(r'api[_-]?key\s*=\s*["\'][^"\']+["\']', code, re.IGNORECASE):
        issues.append("Potential API key hardcoded")
    
    # Passwords
    if re.search(r'password\s*=\s*["\'][^"\']+["\']', code, re.IGNORECASE):
        issues.append("Potential password hardcoded")
    
    # Tokens
    if re.search(r'token\s*=\s*["\'][^"\']+["\']', code, re.IGNORECASE):
        issues.append("Potential token hardcoded")
    
    # AWS keys
    if re.search(r'AKIA[0-9A-Z]{16}', code):
        issues.append("Potential AWS access key")
    
    # Private keys
    if 'BEGIN PRIVATE KEY' in code or 'BEGIN RSA PRIVATE KEY' in code:
        issues.append("Private key detected")
    
    return issues


def calculate_review_score(reviews: List[Dict[str, Any]]) -> float:
    """
    Calculate overall code quality score based on reviews
    
    Args:
        reviews: List of review comments
        
    Returns:
        Score from 0-100
    """
    if not reviews:
        return 100.0
    
    # Severity weights
    weights = {
        'critical': 20,
        'high': 10,
        'medium': 5,
        'low': 2,
        'info': 0
    }
    
    total_penalty = sum(weights.get(r.get('severity', 'info'), 0) for r in reviews)
    
    # Base score is 100, subtract penalties
    score = max(0, 100 - total_penalty)
    
    return score
