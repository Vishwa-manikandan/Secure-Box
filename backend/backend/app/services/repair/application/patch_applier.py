import subprocess
import logging
import os
from pathlib import Path
from typing import Tuple

logger = logging.getLogger("securebox.repair.applier")

class PatchApplier:
    """Safely applies validated patches to the repository."""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def apply_patch(self, patch_content: str) -> Tuple[bool, str]:
        """
        Applies a patch using 'git apply'.
        Assumes the patch has already been validated by PatchValidator.
        """
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write(patch_content)
            tmp_path = tmp.name

        try:
            # Apply the patch
            result = subprocess.run(
                ["git", "apply", tmp_path],
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                logger.info("Patch applied successfully")
                return True, "Patch applied successfully"
            else:
                logger.error(f"Patch application failed: {result.stderr}")
                return False, f"Git apply failed: {result.stderr.strip()}"
        except subprocess.TimeoutExpired:
            return False, "Patch application timed out"
        except Exception as e:
            return False, f"Unexpected error during application: {str(e)}"
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
