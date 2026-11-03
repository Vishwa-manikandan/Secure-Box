from typing import Dict, Any, List
from backend.app.services.sandbox.manager.sandbox_manager import SandboxManager
from backend.app.services.sandbox.security.permission_validator import PermissionValidator

class SandboxOrchestrator:
    """High-level coordinator for the Skill Sandbox lifecycle."""
    
    def __init__(self):
        self.manager = SandboxManager()
        self.validator = PermissionValidator()

    async def validate_and_run(self, skill_id: str, version: str, content: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Static Inspection
        inspection = self.validator.inspect_skill(content)
        
        # 2. In a real flow, we would now stop and ask for approval of requested_permissions
        # For this foundation, we'll assume the user approved the detected permissions
        approved_permissions = inspection["requested_permissions"]
        
        # 3. Run in Sandbox
        job_id = await self.manager.create_job(skill_id, version, inputs)
        result = await self.manager.execute_skill(job_id, skill_id, approved_permissions, inputs)
        
        return {
            "job_id": job_id,
            "inspection": inspection,
            "result": result
        }
