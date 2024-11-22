from sqlmodel import SQLModel, Field
from typing import Optional

class FileRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_name: str
    file_url: str
    cloudinary_id: str
