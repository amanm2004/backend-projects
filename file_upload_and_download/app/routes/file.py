from fastapi import APIRouter ,UploadFile ,File
from services.file_service import save_file

router = APIRouter()

@router.post("/upload")
async def upload_file(file:UploadFile = File(...)):
    result = await save_file(file)
    return result