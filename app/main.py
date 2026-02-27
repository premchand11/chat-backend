from fastapi import FastAPI
from app.api.routes import upload

app = FastAPI(title="Chat Universe Analyzer API")

app.include_router(upload.router)


@app.get("/")
async def root():
    return {"status": "Backend Running"}
