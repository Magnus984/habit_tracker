import bcrypt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound
from config.db import session
from schemas.schema import User
from .utils._token import generate_token, confirm_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
router = APIRouter()

def _hash_password(password: str) -> bytes:
    """Hashes input password.
    """
    password_to_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_to_bytes, salt)
    return hashed_password

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """generates access token for login"""
    try:
        user = session.query(User).filter(User.username == form_data.username).one()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"Incorrect username or password"}
        )
    password_to_byte = form_data.password.encode('utf-8')
    if not bcrypt.checkpw(password_to_byte, user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    access_token = generate_token(user.email, token_type="access", expires_in=30)
    return {
        "access_token": access_token,
        "token_type": "bearer"
        }

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Gets current user
    """
    try:
        email = confirm_token(token=token, expected_type="access")
        try:
            user = session.query(User).filter(User.email == email).one()
            return user
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or token invalid"
            )
    except HTTPException as e:
        raise e