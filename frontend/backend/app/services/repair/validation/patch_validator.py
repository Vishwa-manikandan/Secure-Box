import subprocess
import logging
import os
from typing import Tuple
from pathlib import Path

logger = logging.getLogger("securebox.repair.validator")

class PatchValidator:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def validate_patch(self, patch_content: str) -> Tuple[bool, str]:
        if not patch_content.strip():
            return False, "Patch content is empty"
        for line in patch_content.splitlines():
            if (line.startswith('--- ') or line.startswith('+++ ')) and (".." in line or line.startswith('/')):
                return False, f"Security violation: Path traversal in patch: {line}"
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write(patch_content)
            tmp_path = tmp.name
        try:
            result = subprocess.run(["git", "apply", "--check", tmp_path], cwd=str(self.repo_path), capture_output=True, text=True, timeout=30)
            if result.returncode == 0: return True, "Patch is valid"
            return False, f"Git apply check failed: {result.stderr.strip()}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
        finally:
            if os.path.exists(tmp_path): os.remove(tmp_path)
