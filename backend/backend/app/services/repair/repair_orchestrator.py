import logging
from typing import Dict, Any, Tuple
from backend.app.services.repair.validation.patch_validator import PatchValidator
from backend.app.services.repair.application.patch_applier import PatchApplier
from backend.app.services.repair.rollback.rollback_manager import RollbackManager

logger = logging.getLogger("securebox.repair.orchestrator")

class RepairOrchestrator:
    """Orchestrates the repair lifecycle: Propose -> Validate -> Apply -> Verify."""
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.validator = PatchValidator(repo_path)
        self.applier = PatchApplier(repo_path)
        self.rollback = RollbackManager(repo_path)

    async def process_repair(self, patch_content: str) -> Tuple[bool, str]:
        """
        Full repair pipeline. 
        Note: In a real app, 'Approval' is a separate API call.
        This method handles the technical application.
        """
        # 1. Validate
        is_valid, msg = self.validator.validate_patch(patch_content)
        if not is_valid:
            logger.warning(f"Invalid patch: {msg}")
            return False, msg
            
        # 2. Apply
        success, apply_msg = self.applier.apply_patch(patch_content)
        if not success:
            logger.error(f"Application failed: {apply_msg}")
            return False, apply_msg
            
        # 3. Post-apply verification would go here (running tests, rescanning)
        # For this foundation, we return success.
        
        return True, "Patch applied successfully"

    async def rollback_repair(self, patch_content: str) -> Tuple[bool, str]:
        """Initiates rollback of a specific patch."""
        return self.rollback.rollback_patch(patch_content)
