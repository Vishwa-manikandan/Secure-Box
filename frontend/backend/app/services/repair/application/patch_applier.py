import subprocess
import logging
import os
from typing import Tuple
from pathlib import Path

logger = logging.getLogger("securebox.repair.applier")

class PatchApplier:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def apply_patch(self, patch_content: str) -> Tuple[bool, str]:
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write(patch_content)
            tmp_path = tmp.name
        try:
            result = subprocess.run(["git", "apply", tmp_path], cwd=str(self.repo_path), capture_output=True, text=True, timeout=60)
            if result.returncode == 0: return True, "Patch applied successfully"
            return False, f"Git apply failed: {result.stderr.strip()}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
        finally:
            if os.path.exists(tmp_path): os.remove(tmp_path)
