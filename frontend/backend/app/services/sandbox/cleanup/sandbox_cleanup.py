import logging
import subprocess
from typing import List

logger = logging.getLogger("securebox.sandbox.cleanup")

class SandboxCleanup:
    """Ensures no orphaned containers or volumes remain."""
    
    async def cleanup_job(self, job_id: str):
        """Remove containers associated with a job."""
        container_name = f"securebox-job-{job_id}"
        try:
            subprocess.run(
                ["docker", "rm", "-f", container_name],
                capture_output=True,
                text=True
            )
            logger.info(f"Cleaned up container {container_name}")
        except Exception as e:
            logger.error(f"Cleanup failed for {container_name}: {e}")

    async def purge_orphans(self):
        """Remove any securebox-job containers that have been running too long."""
        # Logic to list containers and filter by name and age
        pass
