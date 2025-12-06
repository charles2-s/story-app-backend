from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from auth import SECRET_KEY, ALGORITHM
from database import SessionLocal
from sqlalchemy.orm import Session
from models import User
oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)
def get_db():
 db = SessionLocal()
 try:
   yield db
 finally:
   db.close()
def get_current_user(token: str = Depends(oauth_scheme),
                      db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(401, "Token required")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(401, "Invalid token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(401, "Invalid token")
    return user

def get_current_user_optional(token: str = Depends(oauth_scheme),
                              db: Session = Depends(get_db)):
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except (JWTError, ValueError):
        return None
