from fastapi import FastAPI

app = FastAPI(title="Securebox API")

@app.get("/")
async def root():
    return {"message": "Welcome to Securebox AI-powered code security platform"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
