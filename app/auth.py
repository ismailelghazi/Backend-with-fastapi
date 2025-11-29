from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .utils import jwt_handler
from .database import get_db
from . import models

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
        
    payload = jwt_handler.verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    username = payload.get("sub")
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
    return user
