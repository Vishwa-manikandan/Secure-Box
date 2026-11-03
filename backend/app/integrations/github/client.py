class GitHubClient:
    def __init__(self, token: str): self.token = token
    async def list_repositories(self, org=None): return []
    async def get_repository_content(self, o, r, b="main"): return ""
    async def post_pr_comment(self, o, r, p, b): return True
