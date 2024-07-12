from jwt import InvalidTokenError
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from sqlalchemy.orm import Session
from app.db import user as user_db
from app.auth.auth_handler import decode_jwt
from app.routers.api.auth.auth import oauth2_scheme

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/signup", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_db.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Email already registered.")
    created_user = user_db.create_user(db, user)
    return {"detail": f"User {created_user.email} created successfully."}


@router.get("", response_model=UserResponse, status_code=200)
def read_user(user_token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Check if user_token is valid or revoked
    try:
        payload = decode_jwt(user_token)
        username = payload.get("username")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = user_db.get_user_by_email(db, username)
    if user is None:
        raise credentials_exception
    return user


# @router.put("/{user_id}", response_model=int,  tags=["user"], status_code=200)
# def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
#     user = user_db.get_user(db, user_id)
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found.")
#     return user_db.update_user(db, user_id, user)
