from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain.callbacks import get_openai_callback
from app.config import settings
from app.schemas import ReviewComment, SeverityLevel, CategoryType
from app.logger import setup_logger

logger = setup_logger(__name__)


class BaseReviewAgent(ABC):
    """Base class for all review agents"""
    
    def __init__(self, agent_name: str, focus_area: str):
        """
        Initialize base agent with LangChain
        
        Args:
            agent_name: Name of the agent
            focus_area: Primary focus area of this agent
        """
        self.agent_name = agent_name
        self.focus_area = focus_area
        
        # Initialize LLM based on provider (supports OpenAI and Groq)
        if settings.LLM_PROVIDER.lower() == "groq":
            logger.info(f"Initializing {agent_name} with Groq (faster & cheaper!)")
            self.llm = ChatGroq(
                model=settings.DEFAULT_LLM_MODEL,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
                groq_api_key=settings.GROQ_API_KEY
            )
        else:  # Default to OpenAI
            logger.info(f"Initializing {agent_name} with OpenAI")
            self.llm = ChatOpenAI(
                model=settings.DEFAULT_LLM_MODEL,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS,
                openai_api_key=settings.OPENAI_API_KEY
            )
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        pass
    
    @abstractmethod
    def get_analysis_prompt(self, code_context: Dict[str, Any]) -> str:
        """Get the analysis prompt for specific code"""
        pass
    
    async def analyze(
        self, 
        file_path: str, 
        code_diff: str, 
        language: str,
        full_context: Optional[str] = None
    ) -> List[ReviewComment]:
        """
        Analyze code and generate review comments
        
        Args:
            file_path: Path to the file being reviewed
            code_diff: The code diff/patch
            language: Programming language
            full_context: Additional context about the changes
            
        Returns:
            List of review comments
        """
        try:
            code_context = {
                'file_path': file_path,
                'diff': code_diff,
                'language': language,
                'context': full_context or ''
            }
            
            # Create LangChain messages
            messages = [
                SystemMessage(content=self.get_system_prompt()),
                HumanMessage(content=self.get_analysis_prompt(code_context))
            ]
            
            # Call LLM with LangChain (tracks token usage)
            logger.info(f"{self.agent_name} analyzing {file_path} using LangChain")
            
            with get_openai_callback() as cb:
                response = self.llm.invoke(messages)
                logger.info(f"{self.agent_name} - Tokens: {cb.total_tokens}, Cost: ${cb.total_cost:.4f}")
            
            # Parse response
            analysis_text = response.content
            comments = self._parse_analysis(analysis_text, file_path)
            
            logger.info(f"{self.agent_name} found {len(comments)} issues in {file_path}")
            return comments
            
        except Exception as e:
            logger.error(f"Error in {self.agent_name} analysis: {str(e)}")
            return []
    
    def _parse_analysis(self, analysis_text: str, file_path: str) -> List[ReviewComment]:
        """
        Parse LLM analysis into structured comments
        
        Args:
            analysis_text: Raw analysis from LLM
            file_path: File being analyzed
            
        Returns:
            List of ReviewComment objects
        """
        comments = []
        
        # Split by issues (assumes LLM formats with numbered lists or markers)
        issue_blocks = self._split_issues(analysis_text)
        
        for block in issue_blocks:
            comment = self._parse_single_issue(block, file_path)
            if comment:
                comments.append(comment)
        
        return comments
    
    def _split_issues(self, text: str) -> List[str]:
        """Split analysis text into individual issues"""
        # Split by common markers
        import re
        
        # Try numbered list format
        if re.search(r'\d+\.\s+', text):
            parts = re.split(r'\n\d+\.\s+', text)
            return [p.strip() for p in parts if p.strip()]
        
        # Try bullet points
        if '- ' in text or '* ' in text:
            parts = re.split(r'\n[-*]\s+', text)
            return [p.strip() for p in parts if p.strip()]
        
        # Default: treat as single issue
        return [text.strip()] if text.strip() else []
    
    def _parse_single_issue(self, issue_text: str, file_path: str) -> Optional[ReviewComment]:
        """Parse a single issue into a ReviewComment"""
        try:
            # Extract line number if present
            import re
            line_match = re.search(r'[Ll]ine\s+(\d+)', issue_text)
            line_number = int(line_match.group(1)) if line_match else None
            
            # Extract severity
            severity = self._extract_severity(issue_text)
            
            # Extract issue and suggestion
            issue_parts = issue_text.split('\n', 1)
            issue_summary = issue_parts[0].strip()
            suggestion = issue_parts[1].strip() if len(issue_parts) > 1 else "Review and fix the identified issue"
            
            # Calculate confidence based on keywords
            confidence = self._calculate_confidence(issue_text)
            
            return ReviewComment(
                agent=self.agent_name,
                file=file_path,
                line=line_number,
                severity=severity,
                category=self._get_category(),
                issue=issue_summary,
                suggestion=suggestion,
                confidence=confidence
            )
        except Exception as e:
            logger.warning(f"Failed to parse issue: {str(e)}")
            return None
    
    def _extract_severity(self, text: str) -> SeverityLevel:
        """Extract severity from issue text"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['critical', 'severe', 'dangerous', 'vulnerability']):
            return SeverityLevel.CRITICAL
        elif any(word in text_lower for word in ['high', 'important', 'significant']):
            return SeverityLevel.HIGH
        elif any(word in text_lower for word in ['medium', 'moderate']):
            return SeverityLevel.MEDIUM
        elif any(word in text_lower for word in ['low', 'minor']):
            return SeverityLevel.LOW
        else:
            return SeverityLevel.INFO
    
    def _calculate_confidence(self, text: str) -> float:
        """Calculate confidence score based on text analysis"""
        confidence = 0.7  # Base confidence
        
        text_lower = text.lower()
        
        # Increase confidence for definite statements
        if any(word in text_lower for word in ['always', 'never', 'must', 'will', 'definitely']):
            confidence += 0.15
        
        # Decrease confidence for uncertain statements
        if any(word in text_lower for word in ['might', 'could', 'possibly', 'maybe', 'perhaps']):
            confidence -= 0.15
        
        # Increase for specific patterns/examples
        if 'example' in text_lower or 'pattern' in text_lower:
            confidence += 0.1
        
        return max(0.0, min(1.0, confidence))
    
    @abstractmethod
    def _get_category(self) -> CategoryType:
        """Get the category for this agent's reviews"""
        pass


class SecurityAnalystAgent(BaseReviewAgent):
    """Agent specialized in security analysis"""
    
    def __init__(self):
        super().__init__("Security Analyst", "Security vulnerabilities and risks")
    
    def get_system_prompt(self) -> str:
        return """You are an expert security analyst reviewing code changes for security vulnerabilities.

Focus on identifying:
- SQL injection vulnerabilities
- Cross-site scripting (XSS) risks
- Authentication and authorization issues
- Insecure data handling
- Hardcoded credentials or secrets
- Unsafe deserialization
- Command injection risks
- Cryptographic weaknesses
- CSRF vulnerabilities
- Path traversal issues
- Insecure API endpoints
- Missing input validation

For each issue found, provide:
1. Line number (if identifiable)
2. Clear description of the security risk
3. Potential impact and exploit scenario
4. Specific recommendation to fix

Be thorough but avoid false positives. Only report genuine security concerns."""
    
    def get_analysis_prompt(self, code_context: Dict[str, Any]) -> str:
        return f"""Analyze this code change for security vulnerabilities:

File: {code_context['file_path']}
Language: {code_context['language']}

Code Changes:
{code_context['diff']}

Additional Context:
{code_context.get('context', 'None')}

Identify all security issues, rank by severity (CRITICAL, HIGH, MEDIUM, LOW), and provide specific fixes.
Format each issue as:
Line X: [Issue description]
Impact: [Security impact]
Fix: [Specific recommendation]"""
    
    def _get_category(self) -> CategoryType:
        return CategoryType.SECURITY


class PerformanceReviewerAgent(BaseReviewAgent):
    """Agent specialized in performance analysis"""
    
    def __init__(self):
        super().__init__("Performance Reviewer", "Performance and efficiency")
    
    def get_system_prompt(self) -> str:
        return """You are an expert performance engineer reviewing code changes for efficiency issues.

Focus on identifying:
- Algorithmic complexity issues (O(n²) where O(n) possible)
- Inefficient database queries (N+1 queries, missing indexes)
- Memory leaks and excessive memory usage
- Redundant computations
- Inefficient data structures
- Missing caching opportunities
- Unnecessary synchronous operations
- Resource leaks (file handles, connections)
- Inefficient loops and iterations
- Premature optimization vs real issues

For each issue, provide:
1. Line number
2. Performance problem description
3. Expected impact on performance
4. Optimized alternative implementation

Focus on real, measurable performance impacts, not micro-optimizations."""
    
    def get_analysis_prompt(self, code_context: Dict[str, Any]) -> str:
        return f"""Analyze this code change for performance issues:

File: {code_context['file_path']}
Language: {code_context['language']}

Code Changes:
{code_context['diff']}

Identify performance bottlenecks, inefficiencies, and optimization opportunities.
Format each issue as:
Line X: [Performance issue]
Impact: [Performance impact - time/memory/resources]
Optimization: [Better approach with complexity analysis]"""
    
    def _get_category(self) -> CategoryType:
        return CategoryType.PERFORMANCE


class CodeQualityInspectorAgent(BaseReviewAgent):
    """Agent specialized in code quality and best practices"""
    
    def __init__(self):
        super().__init__("Code Quality Inspector", "Code quality and maintainability")
    
    def get_system_prompt(self) -> str:
        return """You are an expert code reviewer focused on code quality, readability, and best practices.

Focus on identifying:
- Violations of SOLID principles
- Poor naming conventions
- Code duplication (DRY violations)
- Complex, hard-to-read code
- Missing or poor documentation
- Inconsistent code style
- Magic numbers and strings
- Long functions/methods (>50 lines)
- Deep nesting (>3 levels)
- Tight coupling
- Missing error handling
- Poor separation of concerns

For each issue:
1. Line number
2. Quality issue description
3. Impact on maintainability
4. Refactoring suggestion

Focus on issues that genuinely impact code quality and maintainability."""
    
    def get_analysis_prompt(self, code_context: Dict[str, Any]) -> str:
        return f"""Analyze this code change for quality and maintainability:

File: {code_context['file_path']}
Language: {code_context['language']}

Code Changes:
{code_context['diff']}

Identify code quality issues, best practice violations, and maintainability concerns.
Format each issue as:
Line X: [Quality issue]
Impact: [Effect on maintainability/readability]
Improvement: [How to refactor/improve]"""
    
    def _get_category(self) -> CategoryType:
        return CategoryType.QUALITY


class LogicAnalyzerAgent(BaseReviewAgent):
    """Agent specialized in logic and correctness analysis"""
    
    def __init__(self):
        super().__init__("Logic Analyzer", "Logic correctness and edge cases")
    
    def get_system_prompt(self) -> str:
        return """You are an expert software engineer reviewing code logic and correctness.

Focus on identifying:
- Logic errors and bugs
- Edge case handling (null, empty, boundary values)
- Off-by-one errors
- Race conditions in concurrent code
- Incorrect error handling
- Missing validation
- Incorrect assumptions
- Type mismatches
- Incorrect comparisons (== vs ===, is vs ==)
- Missing null/undefined checks
- Array/list bounds issues
- Incorrect loop conditions

For each issue:
1. Line number
2. Logic problem description
3. Problematic scenario/input
4. Correct implementation

Focus on actual logic bugs, not style preferences."""
    
    def get_analysis_prompt(self, code_context: Dict[str, Any]) -> str:
        return f"""Analyze this code change for logic errors and correctness:

File: {code_context['file_path']}
Language: {code_context['language']}

Code Changes:
{code_context['diff']}

Identify logic bugs, edge case issues, and correctness problems.
Format each issue as:
Line X: [Logic issue]
Scenario: [When this would fail/cause problems]
Fix: [Correct implementation]"""
    
    def _get_category(self) -> CategoryType:
        return CategoryType.LOGIC
