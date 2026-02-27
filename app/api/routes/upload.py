from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/")
async def upload_chat(universe: str = Form(...), file: UploadFile = File(...)):
    content = await file.read()

    return {"filename": file.filename, "universe": universe, "size_bytes": len(content)}
