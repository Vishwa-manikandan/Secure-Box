# Securebox

Securebox is an AI-powered code security and skill intelligence platform.

## Product Vision
Build a professional platform that enables developers to:
- Scan entire software repositories for security risks.
- Detect exposed API keys, credentials, tokens, passwords and confidential information.
- Identify vulnerabilities and insecure code.
- Review code using AI.
- Generate and apply controlled code fixes.
- Verify fixes through tests and subsequent scans.
- Create, manage, inspect and validate AI agent skills.

## Architecture
- **Frontend**: Next.js, TypeScript, Tailwind CSS, shadcn/ui.
- **Backend**: Python, FastAPI, Pydantic, LangGraph.
- **Database**: SQLite (initial), PostgreSQL (abstraction ready).
- **Testing**: Pytest, Playwright.
- **Deployment**: Docker.

## Getting Started

### Backend Setup
1. `cd backend`
2. `python -m venv .venv`
3. `source .venv/bin/activate` (or `.venv\Scripts\activate` on Windows)
4. `pip install -r requirements.txt`
5. `uvicorn app.main:app --reload`

### Frontend Setup
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Security
See [SECURITY.md](SECURITY.md) for details.
