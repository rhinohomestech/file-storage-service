from fastapi import FastAPI, UploadFile, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import engine, get_session
from models import FileRecord, User
from cloudinary_utils import upload_file_to_cloudinary
from dependencies import authenticate_user
import cloudinary.uploader
from uuid import uuid4

app = FastAPI()


# Initialize database
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.post("/register/")
async def register_user(email: str, session: Session = Depends(get_session)):
    private_id = str(uuid4())
    new_user = User(email=email, private_id=private_id)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"email": new_user.email, "private_id": new_user.private_id}

@app.post("/upload/")
async def upload_file(
        file: UploadFile,
        user: User = Depends(authenticate_user),
        session: Session = Depends(get_session)
):
    try:
        upload_response = upload_file_to_cloudinary(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary upload failed: {str(e)}")

    new_file = FileRecord(
        file_name=file.filename,
        file_url=upload_response["url"],
        cloudinary_id=upload_response["cloudinary_id"],
    )
    session.add(new_file)
    session.commit()
    session.refresh(new_file)

    return {
        "id": new_file.id,
        "file_name": new_file.file_name,
        "file_url": new_file.file_url,
    }


@app.get("/files/")
async def get_files(
        user: User = Depends(authenticate_user),
        session: Session = Depends(get_session)
):
    files = session.exec(select(FileRecord)).all()
    return files


@app.put("/files/{file_id}")
async def update_file(
        file_id: int,
        new_file: UploadFile,
        user: User = Depends(authenticate_user),
        session: Session = Depends(get_session)
):
    file_record = session.get(FileRecord, file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        cloudinary.uploader.destroy(file_record.cloudinary_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete old file from Cloudinary: {str(e)}")

    try:
        upload_response = upload_file_to_cloudinary(new_file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload new file to Cloudinary: {str(e)}")

    file_record.file_name = new_file.filename
    file_record.file_url = upload_response["url"]
    file_record.cloudinary_id = upload_response["cloudinary_id"]
    session.add(file_record)
    session.commit()
    session.refresh(file_record)

    return {
        "id": file_record.id,
        "file_name": file_record.file_name,
        "file_url": file_record.file_url,
    }
