import re
from typing import List, Dict, Any, Optional, Tuple
from github import Github, GithubException
from app.config import settings
from app.schemas import FileChange, PRInfo
from app.logger import setup_logger

logger = setup_logger(__name__)


class GitHubService:
    """Service for interacting with GitHub API"""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub service
        
        Args:
            token: GitHub personal access token
        """
        self.token = token or settings.GITHUB_TOKEN
        self.client = Github(self.token) if self.token else None
    
    async def get_pr_info(self, repo_owner: str, repo_name: str, pr_number: int) -> PRInfo:
        """
        Fetch PR information from GitHub
        
        Args:
            repo_owner: Repository owner
            repo_name: Repository name
            pr_number: Pull request number
            
        Returns:
            PRInfo object with PR details
            
        Raises:
            Exception: If PR cannot be fetched
        """
        try:
            if not self.client:
                raise ValueError("GitHub token not configured")
            
            # Get repository
            repo = self.client.get_repo(f"{repo_owner}/{repo_name}")
            logger.info(f"Fetching PR #{pr_number} from {repo_owner}/{repo_name}")
            
            # Get pull request
            pr = repo.get_pull(pr_number)
            
            # Get file changes
            files_changed = []
            for file in pr.get_files():
                file_change = FileChange(
                    filename=file.filename,
                    status=file.status,
                    additions=file.additions,
                    deletions=file.deletions,
                    changes=file.changes,
                    patch=file.patch,
                    language=self._detect_language(file.filename)
                )
                files_changed.append(file_change)
            
            # Create PRInfo object
            pr_info = PRInfo(
                number=pr.number,
                title=pr.title,
                description=pr.body,
                author=pr.user.login,
                base_branch=pr.base.ref,
                head_branch=pr.head.ref,
                state=pr.state,
                files_changed=files_changed,
                created_at=pr.created_at,
                updated_at=pr.updated_at
            )
            
            logger.info(f"Successfully fetched PR #{pr_number}: {len(files_changed)} files changed")
            return pr_info
            
        except GithubException as e:
            logger.error(f"GitHub API error: {e.status} - {e.data}")
            raise Exception(f"Failed to fetch PR: {e.data.get('message', str(e))}")
        except Exception as e:
            logger.error(f"Error fetching PR: {str(e)}")
            raise
    
    def _detect_language(self, filename: str) -> Optional[str]:
        """
        Detect programming language from filename
        
        Args:
            filename: File name/path
            
        Returns:
            Detected language or None
        """
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.r': 'r',
            '.sql': 'sql',
            '.sh': 'bash',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.json': 'json',
            '.xml': 'xml',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sass': 'sass',
        }
        
        for ext, lang in extension_map.items():
            if filename.endswith(ext):
                return lang
        
        return None


class DiffParser:
    """Parser for Git diffs"""
    
    @staticmethod
    def parse_diff(diff_content: str) -> List[Dict[str, Any]]:
        """
        Parse git diff into structured format
        
        Args:
            diff_content: Raw diff content
            
        Returns:
            List of parsed file changes
        """
        changes = []
        current_file = None
        current_hunk = []
        
        lines = diff_content.split('\n')
        
        for line in lines:
            # New file marker
            if line.startswith('diff --git'):
                if current_file:
                    changes.append(current_file)
                current_file = {
                    'hunks': [],
                    'added_lines': [],
                    'removed_lines': [],
                    'context_lines': []
                }
                current_hunk = []
            
            # File path
            elif line.startswith('+++'):
                if current_file is not None:
                    filename = line[6:].strip()  # Remove '+++ b/'
                    current_file['filename'] = filename
                    current_file['language'] = DiffParser._detect_language(filename)
            
            # Hunk header
            elif line.startswith('@@'):
                if current_hunk and current_file:
                    current_file['hunks'].append(current_hunk)
                current_hunk = [line]
                # Parse line numbers
                match = re.search(r'@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@', line)
                if match and current_file:
                    current_file['old_start'] = int(match.group(1))
                    current_file['new_start'] = int(match.group(3))
            
            # Added line
            elif line.startswith('+') and not line.startswith('+++'):
                if current_file is not None:
                    current_file['added_lines'].append(line[1:])
                    if current_hunk is not None:
                        current_hunk.append(line)
            
            # Removed line
            elif line.startswith('-') and not line.startswith('---'):
                if current_file is not None:
                    current_file['removed_lines'].append(line[1:])
                    if current_hunk is not None:
                        current_hunk.append(line)
            
            # Context line
            elif line.startswith(' ') and current_file is not None:
                current_file['context_lines'].append(line[1:])
                if current_hunk is not None:
                    current_hunk.append(line)
        
        # Add last file
        if current_file:
            if current_hunk:
                current_file['hunks'].append(current_hunk)
            changes.append(current_file)
        
        return changes
    
    @staticmethod
    def _detect_language(filename: str) -> Optional[str]:
        """Detect language from filename"""
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
            '.cpp': 'cpp',
            '.c': 'c',
        }
        
        for ext, lang in extension_map.items():
            if filename.endswith(ext):
                return lang
        
        return None
    
    @staticmethod
    def extract_changed_lines_with_context(
        patch: str, 
        context_lines: int = 3
    ) -> List[Tuple[int, str, str]]:
        """
        Extract changed lines with surrounding context
        
        Args:
            patch: Git patch content
            context_lines: Number of context lines to include
            
        Returns:
            List of tuples (line_number, change_type, content)
            change_type: 'added', 'removed', 'context'
        """
        result = []
        if not patch:
            return result
        
        lines = patch.split('\n')
        current_line = 0
        
        for line in lines:
            if line.startswith('@@'):
                # Parse hunk header for line number
                match = re.search(r'\+(\d+)', line)
                if match:
                    current_line = int(match.group(1))
            elif line.startswith('+') and not line.startswith('+++'):
                result.append((current_line, 'added', line[1:]))
                current_line += 1
            elif line.startswith('-') and not line.startswith('---'):
                result.append((current_line, 'removed', line[1:]))
            elif line.startswith(' '):
                result.append((current_line, 'context', line[1:]))
                current_line += 1
        
        return result
