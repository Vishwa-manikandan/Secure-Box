import asyncio
import logging
from typing import List, Dict, Any
from backend.app.services.scanner.discovery.inventory import DiscoveryService
from backend.app.services.scanner.secrets.detector import SecretDetector
from backend.app.orchestration.skillspector.adapter import SkillSpectorAdapter

logger = logging.getLogger("securebox.scanner")

class RepoScanner:
    def __init__(self, root_path: str, api_key: str = None):
        self.root_path = root_path
        self.api_key = api_key
        self.discovery = DiscoveryService(root_path)
        self.secret_detector = SecretDetector()
        self.skill_spector = SkillSpectorAdapter(api_key=api_key)

    async def run_full_scan(self) -> Dict[str, Any]:
        results = {"inventory": None, "findings": [], "coverage": {}, "engines": []}
        inventory = self.discovery.scan()
        results["inventory"] = inventory
        results["coverage"] = {"files_discovered": len(inventory.files) + len(inventory.skipped_files), "files_analyzed": len(inventory.files), "files_excluded": len(inventory.skipped_files), "coverage_percent": inventory.coverage_percent}
        
        results["engines"].append("SecretDetector")
        for file_info in inventory.files:
            if file_info.is_binary: continue
            try:
                with open(file_info.path, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f, 1):
                        findings = self.secret_detector.analyze_line(line, i, file_info.path)
                        for f_obj in findings:
                            results["findings"].append({"rule_id": f_obj.rule_id, "severity": f_obj.severity, "confidence": f_obj.confidence, "file_path": f_obj.file_path, "line_number": f_obj.line_number, "description": f_obj.description, "evidence_reference": f_obj.evidence, "remediation": f_obj.remediation, "status": "open"})
            except Exception: pass

        results["engines"].append("SkillSpector")
        ss_result = await self.skill_spector.run_scan(self.root_path)
        if ss_result.success: results["findings"].extend(ss_//_s result.findings)
        return results
