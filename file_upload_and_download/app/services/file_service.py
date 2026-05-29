import os
import uuid
import aiofiles
from fastapi import UploadFile



UPLOAD_DIR = "storage/uploads"

async def save_file(file : UploadFile):

    unique_name = f"{uuid.uuid4()}_{file.filename}"

    file_path = os.path.join(UPLOAD_DIR,unique_name)

    async with aiofiles.open(file_path,"wb") as out_file:
        while chunk := await file.read(1024 * 1024):
            await out_file.write(chunk)


    return {
        "original_name":file.filename,
        "stored_name":unique_name
    }