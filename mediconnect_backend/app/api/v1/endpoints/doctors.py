import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1 import deps
from app import crud
from app.schemas.response import StandardResponse
from app.schemas.doctor import DoctorVerificationDocument

router = APIRouter()

UPLOAD_DIRECTORY = "./verification_documents"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@router.post("/upload-verification-document", response_model=StandardResponse[DoctorVerificationDocument])
async def upload_verification_document(
    db: AsyncSession = Depends(deps.get_db),
    doctor_id: int = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Upload a verification document for a doctor.
    """
    doctor = await crud.crud_doctor.get(db, id=doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    document_data = {
        "doctor_id": doctor_id,
        "document_type": document_type,
        "document_url": file_path,
        "is_verified": False
    }
    
    new_document = await crud.crud_doctor_verification_document.create(db, obj_in=document_data)

    return StandardResponse(data=new_document, message="Document uploaded successfully.")
