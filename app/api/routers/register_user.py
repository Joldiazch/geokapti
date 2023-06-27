from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api.schemas import User
from app.api.dependecies import (
    get_session,
    get_user,
    get_password_hash
)

def register_user(data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_session)):
    username = data.username
    password = data.password

    if get_user(db, username):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = get_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}