from fastapi import FastAPI, UploadFile, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import engine, get_session
from models import FileRecord
from cloudinary_utils import upload_file_to_cloudinary

app = FastAPI()

# Initialize database
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/upload/")
async def upload_file(file: UploadFile, session: Session = Depends(get_session)):
    # Upload file to Cloudinary
    try:
        upload_response = upload_file_to_cloudinary(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary upload failed: {str(e)}")

    # Save metadata to the database
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
async def get_files(session: Session = Depends(get_session)):
    files = session.exec(select(FileRecord)).all()
    return files

@app.get("/files/{file_id}")
async def get_file(file_id: int, session: Session = Depends(get_session)):
    file_record = session.get(FileRecord, file_id)
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")
    return file_record
