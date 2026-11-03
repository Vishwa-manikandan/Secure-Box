import logging
from typing import Tuple
from backend.app.services.repair.validation.patch_validator import PatchValidator
from backend.app.services.repair.application/patch_applier import PatchApplier
from backend.app.services.repair.rollback.rollback_manager import RollbackManager

logger = logging.getLogger("securebox.repair.orchestrator")

class RepairOrchestrator:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.validator = PatchValidator(repo_path)
        self.applier = PatchApplier(repo_path)
        self.rollback = RollbackManager(repo_path)

    async def process_repair(self, patch_content: str) -> Tuple[bool, str]:
        is_valid, msg = self.validator.validate_patch(patch_content)
        if not is_valid: return False, msg
        success, apply_msg = self.applier.apply_patch(patch_content)
        if not success: return False, apply_msg
        return True, "Patch applied successfully"

    async def rollback_repair(self, patch_content: str) -> Tuple[bool, str]:
        return self.rollback.rollback_patch(patch_content)
