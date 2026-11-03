import httpx
import logging
from typing import List, Dict, Any, Optional
from backend.app.core.config import settings

logger = logging.getLogger("securebox.github")

class GitHubClient:
    """Secure wrapper for GitHub API interactions."""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Securebox-Security-Platform"
        }

    async def list_repositories(self, organization: Optional[str] = None) -> List[Dict[str, Any]]:
        """List repositories authorized for the given token."""
        endpoint = f"{self.base_url}/user/repos" if not organization else f"{self.base_url}/orgs/{organization}/repos"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint, headers=self.headers)
            if response.status_code != 200:
                logger.error(f"GitHub API Error: {response.status_code} - {response.text}")
                return []
            return response.json()

    async def get_repository_content(self, owner: str, repo: str, branch: str = "main") -> str:
        """
        Fetch the repository content as a tarball for scanning.
        In a production environment, this would download to a secure temp directory.
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/tarball/{branch}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, follow_redirects=True)
            if response.status_code != 200:
                logger.error(f"GitHub API Error: {response.status_code}")
                raise Exception("Failed to fetch repository content")
            return response.content.decode('utf-8', errors='ignore')

    async def post_pr_comment(self, owner: str, repo: str, pr_number: int, body: str):
        """Post a security review comment to a pull request."""
        endpoint = f"{self.base_url}/repos/{owner}/{repo}/issues/{pr_number}/comments"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(endpoint, headers=self.headers, json={"body": body})
            if response.status_code != 200:
                logger.error(f"GitHub PR Comment Error: {response.status_code}")
                return False
            return True

    async def upload_sarif(self, owner: str, repo: str, sarif_content: str):
        """Upload SARIF findings to GitHub Code Scanning (requires GHAS)."""
        # This is a simplified representation of the SARIF upload API
        endpoint = f"{self.base_url}/repos/{owner}/{repo}/code-scanning/sarif-files"
        
        async with httpx.AsyncClient() as client:
            # In reality, this requires a specific multipart request
            response = await client.post(endpoint, headers=self.headers, content=sarif_content)
            return response.status_code == 201
