# Securebox Architecture

## System Overview
Securebox is a distributed system designed to bridge the gap between static security analysis and active AI remediation.

### Components
1. **Frontend (Next.js)**: A professional dashboard for managing projects, viewing findings, and approving repairs.
2. **API Gateway (FastAPI)**: Manages authentication, project synchronization, and orchestrates the scanning pipeline.
3. **Scanning Engine**:
    - **Discovery**: Maps the repository structure and identifies languages.
    - **Secret Detector**: Uses entropy and regex to find credentials.
    - **SkillSpector Integration**: Applies NVIDIA's semantic analysis to AI skills.
4. **Repair Engine**: Generates unified diffs and manages the `git apply` lifecycle.
5. **Sandbox Broker**: A high-security layer that spawns isolated Docker containers for skill validation.

## Data Flow
`User Request` $\rightarrow$ `FastAPI` $\rightarrow$ `LangGraph Workflow` $\rightarrow$ `Scanner/Repair Engine` $\rightarrow$ `Database` $\rightarrow$ `Frontend UI`.
