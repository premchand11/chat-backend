from fastapi import FastAPI, Request
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.api.routes import upload
from app.core.rate_limiter import limiter

app = FastAPI(title="Chat Universe Analyzer API")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(upload.router)


@app.get("/")
@limiter.limit("10/minute")
async def root(request: Request):
    return {"status": "Backend Running"}
