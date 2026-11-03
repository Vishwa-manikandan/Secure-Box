from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.app.api.v1 import projects, scans, reports, github
from backend.app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("securebox")

app = FastAPI(title="Securebox API", version="1.0.0")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

app.include_router(projects.router, prefix=settings.API_V1_STR)
app.include_router(scans.router, prefix=settings.API_V1_STR)
app.include_router(reports.router, prefix=settings.API_V1_STR)
app.include_router(github.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root(): return {"message": "Securebox API Active"}

@app.get("/health")
async def health(): return {"status": "healthy"}
