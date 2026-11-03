import asyncio
import logging
import os
from typing import List, Dict, Any
from dataclasses import dataclass

from backend.app.models.all_models import ScanStatus, FindingStatus
from backend.app.schemas.finding import FindingResponse

# We import skillspector inside the function to avoid eager loading issues 
# and to keep the adapter decoupled from the exact install location.
# The adapter will assume skillspector is installed in the environment.

logger = logging.getLogger("securebox.skillspector")

@dataclass
class SkillSpectorResult:
    findings: List[Dict[str, Any]]
    summary: str
    coverage: float
    success: bool

class SkillSpectorAdapter:
    """Adapter for NVIDIA SkillSpector to integrate its scanning logic into Securebox."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    async def run_scan(self, repository_path: str) -> SkillSpectorResult:
        """
        Executes a SkillSpector scan on the given path.
        This wraps the LangGraph workflow of SkillSpector.
        """
        try:
            # Lazy import of skillspector
            import skillspector
            from skillspector.graph import graph
            
            logger.info(f"Starting SkillSpector scan for: {repository_path}")
            
            # We prepare the state for SkillSpector. 
            # Based on our inspection, SkillSpector expects a state dictionary.
            initial_state = {
                "input_path": repository_path,
                "findings": [],
                "filtered_findings": [],
                "structured_summaries": [],
                "api_key": self.api_key
            }
            
            # Invoke the LangGraph workflow
            # SkillSpector's graph is a compiled LangGraph object.
            result = await graph.ainvoke(initial_state)
            
            # Normalize the findings
            # SkillSpector Finding model: (rule_id, message, severity, confidence, file, start_line, ...)
            # Securebox Finding model: (rule_id, category, severity, confidence, file_path, line_number, ...)
            
            raw_findings = result.get("findings", [])
            normalized_findings = []
            
            for f in raw_findings:
                normalized_findings.append({
                    "rule_id": getattr(f, "rule_id", "unknown"),
                    "category": getattr(f, "category", "General"),
                    "severity": getattr(f, "severity", "LOW").upper(),
                    "confidence": getattr(f, "confidence", 0.5),
                    "file_path": getattr(f, "file", "unknown"),
                    "line_number": getattr(f, "start_line", 1),
                    "description": getattr(f, "message", "No description provided"),
                    "evidence_reference": getattr(f, "finding", ""),
                    "remediation": getattr(f, "remediation", ""),
                    "status": "open"
                })
            
            # Extract summary from structured summaries or result
            summary = " ".join([s.get("summary", "") for s in result.get("structured_summaries", [])])
            if not summary:
                summary = "Scan completed. No high-level summary generated."
            
            # Coverage is often a derived metric in the report node
            coverage = result.get("coverage", 1.0)
            
            return SkillSpectorResult(
                findings=normalized_findings,
                summary=summary,
                coverage=coverage,
                success=True
            )
            
        except Exception as e:
            logger.error(f"SkillSpector scan failed: {str(e)}", exc_info=True)
            return SkillSpectorResult(
                findings=[],
                summary=f"Error during scan: {str(e)}",
                coverage=0.0,
                success=False
            )
