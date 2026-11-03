import re
import math
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class SecretFinding:
    rule_id: str
    severity: str
    confidence: float
    file_path: str
    line_number: int
    description: str
    evidence: str
    remediation: str

class SecretDetector:
    PATTERNS = {
        "AWS_ACCESS_KEY": r"AKIA[0-9A-Z]{16}",
        "AWS_SECRET_KEY": r"([^A-Za-z0-9/+=])([A-zA-Z0-9/+=]{40})([^A-Za-z0-9/+=])",
        "GENERIC_API_KEY": r"(?i)(api[_-]?key|secret|token|password|auth)[_:]\s*['\"]([a-zA-Z0-9_\-]{16,})['\"]",
        "GITHUB_TOKEN": r"gh[p|n|o]_[a-zA-Z0-9]{36}",
        "DATABASE_URL": r"(postgres|mysql|mongodb):\/\/([^:]+):([^@]+)@([^\s/]+)",
        "JWT": r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
    }
    def calculate_entropy(self, text: str) -> float:
        if not text: return 0
        probabilities = [float(text.count(c)) / len(text) for c in set(text)]
        return -sum(p * math.log2(p) for p in probabilities)

    def analyze_line(self, line: str, line_num: int, file_path: str) -> List[SecretFinding]:
        findings = []
        for rule_id, pattern in self.PATTERNS.items():
            matches = re.finditer(pattern, line)
            for match in matches:
                val = match.group(0)
                masked = val[:4] + "*" * (len(val)-8) + val[-4:] if len(val) > 8 else "****"
                findings.append(SecretFinding(rule_id=rule_id, severity="CRITICAL", confidence=0.9, file_path=file_path, line_number=line_num, description=f"Detected {rule_id}", evidence=masked, remediation="Revoke and rotate."))
        if "=" in line:
            parts = line.split("=", 1)
            val = parts[1].strip().strip("'\"")
            if len(val) > 16 and self.calculate_entropy(val) > 4.5:
                masked = val[:4] + "*" * (len(val)-8) + val[-4:] if len(val) > 8 else "****"
                findings.append(SecretFinding(rule_id="HIGH_ENTROPY_SECRET", severity="HIGH", confidence=0.6, file_path=file_path, line_number=line_num, description="High entropy string detected", evidence=masked, remediation="Verify if this is a secret."))
        return findings
