import logging
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from backend.app.services.sandbox.security.permission_validator import PermissionValidator
from backend.app.services.sandbox.execution.skill_executor import SkillExecutor
from backend.app.services.sandbox.cleanup.sandbox_cleanup import SandboxCleanup

logger = logging.getLogger("securebox.sandbox.manager")

class SandboxManager:
    """Orchestrates the creation, execution, and cleanup of skill sandboxes."""
    
    def __init__(self, docker_client=None):
        # In a real app, we'd pass a configured Docker SDK client
        self.docker_client = docker_client 
        self.validator = PermissionValidator()
        self.cleanup = SandboxCleanup()

    async def create_job(self, skill_id: str, version: str, inputs: Dict[str, Any]) -> str:
        """Initialize a new sandbox job and return the job_id."""
        job_id = str(uuid.uuid4())
        logger.info(f"Creating sandbox job {job_id} for skill {skill_id} v{version}")
        # Here we would record the job in the DB as 'QUEUED'
        return job_id

    async def validate_skill(self, skill_content: str) -> Dict[str, Any]:
        """Perform static inspection of the skill before execution."""
        return self.validator.inspect_skill(skill_content)

    async def execute_skill(self, job_id: str, skill_id: str, approved_permissions: List[str], inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the skill in a hardened container."""
        executor = SkillExecutor(job_id)
        try:
            result = await executor.run(skill_id, approved_permissions, inputs)
            return result
        finally:
            await self.cleanup.cleanup_job(job_id)
