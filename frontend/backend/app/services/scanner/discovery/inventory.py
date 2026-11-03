import os
from dataclasses import dataclass, field
from typing import List, Set, Dict
from pathlib import Path

@dataclass
class FileInfo:
    path: str
    extension: str
    size: int
    is_binary: bool
    is_config: bool = False
    is_dependency: bool = False

@dataclass
class RepoInventory:
    root_path: str
    files: List[FileInfo] = field(default_factory=list)
    languages: Set[str] = field(default_factory=set)
    package_managers: Set[str] = field(default_factory=set)
    skipped_files: List[str] = field(default_factory=list)
    coverage_percent: float = 0.0

class DiscoveryService:
    """Stage 1: Repository Discovery"""
    
    CONFIG_FILES = {".env", "settings.json", "config.yaml", "config.json", "web.config", "appsettings.json"}
    PKG_MANAGERS = {
        "package.json": "npm/yarn",
        "requirements.txt": "pip",
        "pyproject.toml": "poetry/pip",
        "pom.xml": "maven",
        "go.mod": "go",
        "Cargo.toml": "cargo"
    }
    
    EXCLUSIONS = {
        ".git", ".svn", ".hg", "node_modules", "venv", ".venv", "__pycache__", 
        "dist", "build", ".next", ".idea", ".vscode", "target"
    }

    def __init__(self, root_path: str, custom_exclusions: List[str] = None):
        self.root_path = Path(root_path)
        self.exclusions = self.EXCLUSIONS.union(set(custom_exclusions or []))

    def is_binary(self, path: Path) -> bool:
        """Check if a file is binary."""
        try:
            with open(path, 'rb') as f:
                chunk = f.read(1024)
                return b'\x00' in chunk
        except:
            return True

    def scan(self) -> RepoInventory:
        inventory = RepoInventory(root_path=str(self.root_path))
        total_files = 0
        
        for root, dirs, files in os.walk(self.root_path):
            # In-place modification of dirs to respect exclusions
            dirs[:] = [d for d in dirs if d not in self.exclusions]
            
            for file in files:
                total_files += 1
                file_path = Path(root) / file
                
                if any(part in self.exclusions for part in file_path.relative_to(self.root_path).parts):
                    inventory.skipped_files.append(str(file_path))
                    continue
                
                ext = file_path.suffix.lower()
                is_bin = self.is_binary(file_path)
                
                # Identify languages
                if not is_bin:
                    if ext == '.py': inventory.languages.add('python')
                    elif ext == '.ts' or ext == '.tsx' or ext == '.js': inventory.languages.add('typescript/javascript')
                    elif ext == '.go': inventory.languages.add('go')
                    elif ext == '.rs': inventory.languages.add('rust')
                    elif ext == '.java': inventory.languages.add('java')

                # Identify package managers
                if file in self.PKG_MANAGERS:
                    inventory.package_managers.add(self.PKG_MANAGERS[file])

                inventory.files.append(FileInfo(
                    path=str(file_path.relative_to(self.root_path)),
                    extension=ext,
                    size=file_path.stat().st_size,
                    is_binary=is_bin,
                    is_config=file in self.CONFIG_FILES,
                    is_dependency=False # Simplified for now
                ))

        inventory.coverage_percent = (len(inventory.files) / total_files * 100) if total_files > 0 else 0
        return inventory
