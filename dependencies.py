from fastapi import Header, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from models import User

def authenticate_user(private_id: str = Header(...), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.private_id == private_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or missing authentication header")
    return user
