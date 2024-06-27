from typing_extensions import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.auth_handler import sign_jwt
from app.db.database import get_db
from app.db.user import user as user_db
from app.utils.hashing import Hasher


router = APIRouter(prefix="/token", tags=["Authentication"])


# OAuth2PasswordBearer makes FastAPI know that it is a security scheme. So it is added that way to OpenAPI.
# When we create an instance of the OAuth2PasswordBearer class we pass in the tokenUrl parameter. This parameter contains the URL that the client (the frontend running in the user's browser) will use to send the username and password in order to get a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Blacklist for revoked tokens
# Store in redis
token_blacklist = set()


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    access_token = sign_jwt(user.email)
    # To include the JWT token in the Authorization header in the response itself isn't a typical practice because the Authorization header is used for requests, not responses.
    return Token(access_token=access_token, token_type="bearer")

# Route to revoke a token and add it to the blacklist


@router.post("/revoke")
def revoke_token(token: Annotated[str, Depends(oauth2_scheme)]):
    print("token to revoke", token)
    token_blacklist.add(token)
    return {"detail": "Token revoked successfully"}


# Generates a new access token if the current user is authenticated.
# Generate a refresh token along with access token. the refresh token has longer expiry than access token
# When access token expires, refresh token is used to get a new access token without user getting logged out and having to log in.
# @router.post("/token/refresh")


def is_token_revoked(token: str = Depends(oauth2_scheme)):
    if token in token_blacklist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked"
        )
    return token


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    db_user = user_db.get_user_by_email(db, username)
    if not db_user or not Hasher.verify_password(password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db_user
