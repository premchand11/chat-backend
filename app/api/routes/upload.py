from fastapi import APIRouter, UploadFile, File, Form, Request
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/")
@limiter.limit("3/minute")
async def upload_chat(
    request: Request, universe: str = Form(...), file: UploadFile = File(...)
):
    content = await file.read()
    return {"filename": file.filename, "universe": universe, "size_bytes": len(content)}
