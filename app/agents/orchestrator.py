from typing import List, Dict, Any
import asyncio
from collections import defaultdict
from app.agents.base_agent import (
    SecurityAnalystAgent,
    PerformanceReviewerAgent,
    CodeQualityInspectorAgent,
    LogicAnalyzerAgent
)
from app.schemas import ReviewComment, ReviewSummary, SeverityLevel
from app.logger import setup_logger

logger = setup_logger(__name__)


class ReviewOrchestrator:
    """Orchestrates multiple agents for comprehensive code review"""
    
    def __init__(self):
        """Initialize orchestrator with all review agents"""
        self.agents = [
            SecurityAnalystAgent(),
            PerformanceReviewerAgent(),
            CodeQualityInspectorAgent(),
            LogicAnalyzerAgent()
        ]
        logger.info(f"Initialized orchestrator with {len(self.agents)} agents")
    
    async def review_changes(
        self,
        files_changed: List[Dict[str, Any]],
        pr_context: Dict[str, Any] = None
    ) -> tuple[List[ReviewComment], ReviewSummary]:
        """
        Orchestrate multi-agent review of code changes
        
        Args:
            files_changed: List of file changes from PR
            pr_context: Additional PR context (title, description, etc.)
            
        Returns:
            Tuple of (review comments, review summary)
        """
        all_comments = []
        files_reviewed = 0
        lines_analyzed = 0
        
        logger.info(f"Starting review of {len(files_changed)} files")
        
        # Review each file
        for file_change in files_changed:
            filename = file_change.get('filename', 'unknown')
            patch = file_change.get('patch', '')
            language = file_change.get('language', 'unknown')
            
            if not patch:
                logger.warning(f"Skipping {filename}: no patch content")
                continue
            
            logger.info(f"Reviewing file: {filename}")
            files_reviewed += 1
            lines_analyzed += len(patch.split('\n'))
            
            # Run all agents in parallel for this file
            agent_tasks = [
                agent.analyze(
                    file_path=filename,
                    code_diff=patch,
                    language=language,
                    full_context=self._build_context(file_change, pr_context)
                )
                for agent in self.agents
            ]
            
            # Gather results from all agents
            agent_results = await asyncio.gather(*agent_tasks, return_exceptions=True)
            
            # Collect comments, filtering out exceptions
            for result in agent_results:
                if isinstance(result, list):
                    all_comments.extend(result)
                elif isinstance(result, Exception):
                    logger.error(f"Agent error: {str(result)}")
        
        # Deduplicate and prioritize comments
        deduplicated_comments = self._deduplicate_comments(all_comments)
        
        # Sort by severity and confidence
        sorted_comments = self._sort_comments(deduplicated_comments)
        
        # Generate summary
        summary = self._generate_summary(sorted_comments, files_reviewed, lines_analyzed)
        
        logger.info(f"Review complete: {summary.total_issues} issues found")
        return sorted_comments, summary
    
    def _build_context(
        self,
        file_change: Dict[str, Any],
        pr_context: Dict[str, Any] = None
    ) -> str:
        """Build context string for agents"""
        context_parts = []
        
        if pr_context:
            if 'title' in pr_context:
                context_parts.append(f"PR Title: {pr_context['title']}")
            if 'description' in pr_context:
                context_parts.append(f"PR Description: {pr_context['description']}")
        
        status = file_change.get('status', 'modified')
        context_parts.append(f"File Status: {status}")
        
        additions = file_change.get('additions', 0)
        deletions = file_change.get('deletions', 0)
        context_parts.append(f"Changes: +{additions}/-{deletions}")
        
        return '\n'.join(context_parts)
    
    def _deduplicate_comments(self, comments: List[ReviewComment]) -> List[ReviewComment]:
        """
        Remove duplicate comments from multiple agents
        
        Uses similarity matching on file, line, and issue content
        """
        if not comments:
            return []
        
        # Group by file and line
        grouped = defaultdict(list)
        for comment in comments:
            key = (comment.file, comment.line)
            grouped[key].append(comment)
        
        deduplicated = []
        
        for (file, line), group in grouped.items():
            if len(group) == 1:
                deduplicated.extend(group)
                continue
            
            # Find unique issues based on similarity
            unique_comments = []
            for comment in group:
                is_duplicate = False
                
                for existing in unique_comments:
                    similarity = self._calculate_similarity(
                        comment.issue,
                        existing.issue
                    )
                    if similarity > 0.7:  # 70% similarity threshold
                        # Keep the one with higher confidence
                        if comment.confidence > existing.confidence:
                            unique_comments.remove(existing)
                            unique_comments.append(comment)
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    unique_comments.append(comment)
            
            deduplicated.extend(unique_comments)
        
        logger.info(f"Deduplicated {len(comments)} -> {len(deduplicated)} comments")
        return deduplicated
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple similarity between two texts"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _sort_comments(self, comments: List[ReviewComment]) -> List[ReviewComment]:
        """Sort comments by severity and confidence"""
        severity_order = {
            SeverityLevel.CRITICAL: 0,
            SeverityLevel.HIGH: 1,
            SeverityLevel.MEDIUM: 2,
            SeverityLevel.LOW: 3,
            SeverityLevel.INFO: 4
        }
        
        return sorted(
            comments,
            key=lambda c: (severity_order.get(c.severity, 999), -c.confidence)
        )
    
    def _generate_summary(
        self,
        comments: List[ReviewComment],
        files_reviewed: int,
        lines_analyzed: int
    ) -> ReviewSummary:
        """Generate review summary statistics"""
        summary = ReviewSummary(
            total_issues=len(comments),
            files_reviewed=files_reviewed,
            lines_analyzed=lines_analyzed
        )
        
        # Count by severity
        for comment in comments:
            if comment.severity == SeverityLevel.CRITICAL:
                summary.critical += 1
            elif comment.severity == SeverityLevel.HIGH:
                summary.high += 1
            elif comment.severity == SeverityLevel.MEDIUM:
                summary.medium += 1
            elif comment.severity == SeverityLevel.LOW:
                summary.low += 1
            elif comment.severity == SeverityLevel.INFO:
                summary.info += 1
        
        return summary
    
    async def review_file(
        self,
        filename: str,
        patch: str,
        language: str,
        context: str = None
    ) -> List[ReviewComment]:
        """
        Review a single file with all agents
        
        Args:
            filename: File path
            patch: Git patch/diff
            language: Programming language
            context: Additional context
            
        Returns:
            List of review comments
        """
        comments = []
        
        # Run all agents in parallel
        agent_tasks = [
            agent.analyze(
                file_path=filename,
                code_diff=patch,
                language=language,
                full_context=context
            )
            for agent in self.agents
        ]
        
        results = await asyncio.gather(*agent_tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, list):
                comments.extend(result)
        
        return comments
