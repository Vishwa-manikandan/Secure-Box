import re
import logging
from typing import List, Dict, Any, Set

logger = logging.getLogger("securebox.sandbox.security")

class PermissionValidator:
    """Inspects skill instructions for risky requests."""
    
    RISKY_PATTERNS = {
        "FILESYSTEM_ESCAPE": r"(\.\./|\/etc\/|\/root\/|\/home\/)",
        "SENSITIVE_ENV": r"(AWS_SECRET|GITHUB_TOKEN|PASSWORD|SECRET_KEY)",
        "PRIVILEGED_CMD": r"(sudo|chmod|chown|mkfs|rm\s+-rf\s+/)",
        "NETWORK_SENSITIVE": r"(curl|wget|socket|requests|http)\s+([0-9]{1,3}\.){3}[0-9]{1,3}"
    }

    def inspect_skill(self, content: str) -> Dict[str, Any]:
        """Static analysis of skill content to identify requested permissions."""
        findings = []
        requested_permissions = set()
        
        # Simple heuristic: look for keywords in instructions/scripts
        if "network" in content.lower(): requested_permissions.add("NETWORK_ACCESS")
        if "write" in content.lower(): requested_permissions.add("FILESYSTEM_WRITE")
        if "exec" in content.lower(): requested_permissions.add("PROCESS_EXECUTION")
        
        for category, pattern in self.RISKY_PATTERNS.items():
            if re.search(pattern, content, re.IGNORECASE):
                findings.append({
                    "category": category,
                    "severity": "HIGH",
                    "description": f"Detected potential {category} attempt in skill instructions.",
                    "confidence": 0.8
                })
        
        return {
            "is_safe": len(findings) == 0,
            "requested_permissions": list(requested_permissions),
            "security_findings": findings
        }
