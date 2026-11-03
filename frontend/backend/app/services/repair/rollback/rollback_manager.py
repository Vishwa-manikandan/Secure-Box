import subprocess
import logging
from pathlib import Path
from typing import Tuple

logger = logging.getLogger("securebox.repair.rollback")

class RollbackManager:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def rollback_patch(self, patch_content: str) -> Tuple[bool, str]:
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write(patch_content)
            tmp_path = tmp.name
        try:
            result = subprocess.run(["git", "apply", "-R", tmp_path], cwd=str(self.repo_path), capture_output=True, text=True, timeout=30)
            if result.returncode == 0: return True, "Rollback successful"
            return False, f"Rollback failed: {result.stderr.strip()}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
        finally:
            if os.path.exists(tmp_path): os.remove(tmp_path)
