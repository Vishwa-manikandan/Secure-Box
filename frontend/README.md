# 🛡️ Securebox

Securebox is a professional AI-powered code security and skill intelligence platform. It enables developers to scan repositories for vulnerabilities, detect leaked secrets, and manage AI agent skills with high-fidelity security verification.

## ✨ Features

- **Repository-Wide Scanning**: Deep inspection of local, ZIP, and GitHub repositories.
- **Secret Detection**: High-entropy and pattern-based detection for API keys, tokens, and credentials with automatic masking.
- **AI-Powered Code Review**: Semantic analysis of code to identify logic errors, security gaps, and maintainability issues.
- **Controlled Auto-Repair**: Approval-driven remediation pipeline: `Scan` $\rightarrow$ `Explain` $\rightarrow$ `Propose Fix` $\rightarrow$ `Approve` $\rightarrow$ `Apply` $\rightarrow$ `Verify`.
- **Skill Studio & Library**: Create, validate, and manage AI agent skills with a dedicated security inspection layer.
- **Hardened Sandbox**: Isolated Docker-based execution for testing skills without risking host infrastructure.
- **Security Intelligence**: Historical trend analysis, regression detection, and SARIF report generation.

## 🏗️ Architecture

Securebox follows a modular, security-first architecture:
- **Frontend**: Next.js, TypeScript, Tailwind CSS, and shadcn/ui for a professional developer experience.
- **Backend**: FastAPI (Python) with an asynchronous SQLAlchemy layer for high-performance scanning.
- **Orchestration**: LangGraph-driven workflows for complex security analysis and repair cycles.
- **Isolation**: A dedicated Sandbox Broker manages short-lived, hardened Docker containers for skill execution.

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 20+

### Quick Start (Docker)
1. Clone the repository:
   ```bash
   git clone https://github.com/Vishwa-manikandan/Secure-Box.git
   cd Secure-Box
   ```
2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your OPENAI_API_KEY and GITHUB_TOKEN
   ```
3. Launch the platform:
   ```bash
   docker-compose up -d
   ```
4. Access the UI at `http://localhost:3000`.

## 🛠️ Technology Stack
- **Frontend**: Next.js, TypeScript, Tailwind CSS.
- **Backend**: FastAPI, Pydantic, SQLAlchemy (Async).
- **AI/ML**: LangGraph, OpenAI API, NVIDIA SkillSpector.
- **Infrastructure**: Docker, SQLite (Default), PostgreSQL (Ready).
- **Testing**: Pytest, Playwright.

## 🔒 Security Architecture
Securebox is built on the principle of **Zero Trust** for AI-generated content and imported skills:
- **No Execution**: Scanners never execute untrusted repository code.
- **Credential Masking**: Raw secrets are masked at the source and never stored in plaintext in logs or reports.
- **Human-in-the-Loop**: All repairs require explicit user approval of the generated diff.
- **Sandbox Isolation**: Skills run in rootless, network-isolated containers with strict resource limits.

## 📄 Documentation
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Threat Model](docs/THREAT_MODEL.md)
- [Contributing](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)

## 📜 License
Distributed under the Apache License 2.0.
