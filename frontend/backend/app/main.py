from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.app.api.v1 import projects, scans, reports, github
from backend.app.core.config import settings
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("securebox")

app = FastAPI(
    title="Securebox API",
    version="1.0.0",
    description="AI-powered code security and skill intelligence platform"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred. Please contact support."}
    )

app.include_router(projects.router, prefix=settings.API_V1_STR)
app.include_router(scans.router, prefix=settings.API_V1_STR)
app.include_router(reports.router, prefix=settings.API_V1_STR)
app.include_router(github.router, prefix=settings.API_V1_STR)

@app.get("/", tags=["health"])
async def root():
    return {"message": "Welcome to Securebox API", "version": "1.0.0"}

@app.get("/health", tags=["health"])
async def health():
    return {"status": "healthy"}
