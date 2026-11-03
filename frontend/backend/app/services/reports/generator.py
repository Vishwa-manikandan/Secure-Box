import json
import logging
from datetime import datetime
from typing import List, Dict, Any
from backend.app.models.all_models import Scan, Finding

logger = logging.getLogger("securebox.reports")

class ReportGenerator:
    """Generates security reports in various formats (JSON, Markdown, SARIF)."""
    
    def __init__(self, scan: Scan, findings: List[Finding]):
        self.scan = scan
        self.findings = findings

    def to_json(self) -> str:
        """Generate a detailed JSON report."""
        data = {
            "project_id": self.scan.project_id,
            "scan_id": self.scan.id,
            "timestamp": self.scan.completed_at.isoformat() if self.scan.completed_at else None,
            "coverage": self.scan.coverage,
            "summary": self.scan.summary,
            "stats": {
                "total": len(self.findings),
                "critical": len([f for f in self.findings if f.severity == "CRITICAL"]),
                "high": len([f for f in self.findings if f.severity == "HIGH"]),
                "medium": len([f for f in self.findings if f.severity == "MEDIUM"]),
                "low": len([f for f in self.findings if f.severity == "LOW"]),
            },
            "findings": [
                {
                    "id": f.id,
                    "rule_id": f.rule_id,
                    "severity": f.severity,
                    "file": f.file_path,
                    "line": f.line_number,
                    "description": f.description,
                    "remediation": f.remediation,
                    "status": f.status.value if hasattr(f.status, 'value') else f.status
                } for f in self.findings
            ]
        }
        return json.dumps(data, indent=2)

    def to_markdown(self) -> str:
        """Generate a human-readable Markdown report."""
        lines = [
            "# Securebox Security Report",
            f"**Scan ID:** {self.scan.id}",
            f"**Date:** {self.scan.completed_at}",
            f"**Coverage:** {self.scan.coverage * 100:.2f}%",
            "\n## Summary",
            self.scan.summary or "No summary provided.",
            "\n## Severity Distribution",
            f"- Critical: {len([f for f in self.findings if f.severity == 'CRITICAL'])}",
            f"- High: {len([f for f in self.findings if f.severity == 'HIGH'])}",
            f"- Medium: {len([f for f in self.findings if f.severity == 'MEDIUM'])}",
            f"- Low: {len([f for f in self.findings if f.severity == 'LOW'])}",
            "\n## Findings",
            "| Severity | File | Line | Description | Status |",
            "|---|---|---|---|---|"
        ]
        
        for f in self.findings:
            lines.append(f"| {f.severity} | `{f.file_path}` | {f.line_number} | {f.description[:50]}... | {f.status} |")
            
        return "\n".join(lines)

    def to_sarif(self) -> str:
        """Generate a SARIF (Static Analysis Results Interchange Format) report."""
        # Simplified SARIF implementation
        sarif = {
            "version": "2.1.0",
            "runs": [{
                "tool": {"driver": {"name": "Securebox", "version": "1.0.0"}},
                "results": [
                    {
                        "ruleId": f.rule_id,
                        "level": "error" if f.severity in ["CRITICAL", "HIGH"] else "warning",
                        "message": {"text": f.description},
                        "locations": [{
                            "physicalLocation": {
                                "artifactLocation": {"uri": f.file_path},
                                "region": {"startLine": f.line_number}
                            }
                        }]
                    } for f in self.findings
                ]
            }]
        }
        return json.dumps(sarif, indent=2)
