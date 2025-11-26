from typing import List, Dict, Any
from app.schemas import PRInfo, ReviewComment, ReviewSummary
from app.services.github_service import GitHubService, DiffParser
from app.agents.orchestrator import ReviewOrchestrator
from app.logger import setup_logger

logger = setup_logger(__name__)


class ReviewService:
    """Main service for coordinating PR reviews"""
    
    def __init__(self):
        """Initialize review service"""
        self.orchestrator = ReviewOrchestrator()
    
    async def review_pull_request(
        self,
        repo_owner: str,
        repo_name: str,
        pr_number: int,
        github_token: str = None
    ) -> tuple[List[ReviewComment], ReviewSummary, Dict[str, Any]]:
        """
        Review a GitHub Pull Request
        
        Args:
            repo_owner: Repository owner
            repo_name: Repository name
            pr_number: PR number
            github_token: GitHub access token
            
        Returns:
            Tuple of (comments, summary, metadata)
        """
        logger.info(f"Starting review for PR #{pr_number} in {repo_owner}/{repo_name}")
        
        # Fetch PR information
        github_service = GitHubService(token=github_token)
        pr_info = await github_service.get_pr_info(repo_owner, repo_name, pr_number)
        
        # Prepare files for review
        files_to_review = []
        for file_change in pr_info.files_changed:
            files_to_review.append({
                'filename': file_change.filename,
                'status': file_change.status,
                'additions': file_change.additions,
                'deletions': file_change.deletions,
                'patch': file_change.patch,
                'language': file_change.language
            })
        
        # Build PR context
        pr_context = {
            'title': pr_info.title,
            'description': pr_info.description,
            'author': pr_info.author,
            'base_branch': pr_info.base_branch,
            'head_branch': pr_info.head_branch
        }
        
        # Run review
        comments, summary = await self.orchestrator.review_changes(
            files_changed=files_to_review,
            pr_context=pr_context
        )
        
        # Build metadata
        metadata = {
            'pr_title': pr_info.title,
            'pr_author': pr_info.author,
            'base_branch': pr_info.base_branch,
            'head_branch': pr_info.head_branch,
            'files_changed': len(pr_info.files_changed),
            'total_additions': sum(f.additions for f in pr_info.files_changed),
            'total_deletions': sum(f.deletions for f in pr_info.files_changed)
        }
        
        logger.info(f"Review completed for PR #{pr_number}: {summary.total_issues} issues")
        return comments, summary, metadata
    
    async def review_diff(
        self,
        diff_content: str,
        language: str = "python",
        context: str = None
    ) -> tuple[List[ReviewComment], ReviewSummary]:
        """
        Review a raw diff
        
        Args:
            diff_content: Git diff content
            language: Programming language
            context: Additional context
            
        Returns:
            Tuple of (comments, summary)
        """
        logger.info("Starting review of raw diff")
        
        # Parse diff
        parser = DiffParser()
        parsed_changes = parser.parse_diff(diff_content)
        
        # Prepare for review
        files_to_review = []
        for change in parsed_changes:
            filename = change.get('filename', 'unknown')
            
            # Reconstruct patch from hunks
            patch_lines = []
            for hunk in change.get('hunks', []):
                patch_lines.extend(hunk)
            patch = '\n'.join(patch_lines)
            
            files_to_review.append({
                'filename': filename,
                'status': 'modified',
                'additions': len(change.get('added_lines', [])),
                'deletions': len(change.get('removed_lines', [])),
                'patch': patch,
                'language': change.get('language', language)
            })
        
        # Run review
        comments, summary = await self.orchestrator.review_changes(
            files_changed=files_to_review,
            pr_context={'context': context} if context else None
        )
        
        logger.info(f"Diff review completed: {summary.total_issues} issues")
        return comments, summary
