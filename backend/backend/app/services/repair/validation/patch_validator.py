import subprocess
import logging
import os
from typing import Tuple, List
from pathlib import Path

logger = logging.getLogger("securebox.repair.validator")

class PatchValidator:
    """Validates unified diffs before application."""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def validate_patch(self, patch_content: str) -> Tuple[bool, str]:
        """
        Check if the patch is syntactically correct and can be applied 
        without conflicts using 'git apply --check'.
        """
        if not patch_content.strip():
            return False, "Patch content is empty"

        # Security check: ensure no path traversal in the patch
        # We check for '..' in the file paths of the diff
        for line in patch_content.splitlines():
            if line.startswith('--- ') or line.startswith('+++ '):
                path = line[4:].strip()
                if ".." in path or path.startswith('/'):
                    return False, f"Security violation: Path traversal detected in patch: {path}"

        # Use a temporary file to run git apply --check
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write(patch_content)
            tmp_path = tmp.name

        try:
            # Run git apply --check in the repository directory
            # We use a list for arguments to avoid shell interpolation
            result = subprocess.run(
                ["git", "apply", "--check", tmp_path],
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "Patch is valid"
            else:
                return False, f"Git apply check failed: {result.stderr.strip()}"
        except subprocess.TimeoutExpired:
            return False, "Patch validation timed out"
        except Exception as e:
            return False, f"Unexpected error during validation: {str(e)}"
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
