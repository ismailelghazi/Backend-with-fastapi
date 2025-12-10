from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import schemas, models, database, auth
from ..utils import hashing, jwt_handler

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    user_exists = db.query(models.User).filter(models.User.username == user.username).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = models.User(username=user.username, password_hash=hashing.Hash.bcrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(response: Response, user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    if not hashing.Hash.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    access_token = jwt_handler.create_access_token(data={"sub": db_user.username})
    
    # Set HTTP-only cookie
    # For cross-origin requests (frontend on different domain), we need:
    # - secure=True (HTTPS only)
    # - samesite="none" (allow cross-site cookies)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,  # Required for samesite="none"
        samesite="none"  # Required for cross-origin cookies
    )
    
    return {"message": "logged in"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "logged out"}

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
