from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel, EmailStr
from config.db import session
from schemas.schema import User
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from .utils import _mail, _token
from .auth import _hash_password


router = APIRouter()
#User Management Routes
class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str

#Registration
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: RegisterUser):
    """Register a new user"""
    try:
        existing_user = session.query(User).filter(User.email == user.email).one()
        if existing_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
                )
        else:
            token = _token.generate_token(user.email, "email_verification", 10)
            verification_url = f"http://localhost:8000/api/v1/user/verify?token={token}"
            try:
                _mail.send_verification_email(user.email, verification_url)
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to send email"
                )
            return {"message": "User already exists but not verified. Email verification sent."}
    except NoResultFound:
        new_user = User(
            username=user.username,
            email=user.email,
            password_hash=_hash_password(user.password)
        )
        session.add(new_user)
        session.commit()
        token = _token.generate_token(user.email, "email_verification", 10)
        verification_url = f"http://localhost:8000/api/v1/user/verify?token={token}"
        try:
            _mail.send_verification_email(user.email, token)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email"
            )
        return {"message": "User created successfully. Email verification sent."}
    except MultipleResultsFound:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Multiple users found"
            )

@router.get("/verify")
def verify_email(token: str):
    """Verifies email upon registration"""
    print("confirming token")
    email = _token.confirm_token(token, "email_verification")
    print("token confirmed")
    if email:
        try:
            new_user = session.query(User).filter(User.email == email).one()
            new_user.is_verified = True
            session.commit()
            return {"message": "Email verified successfully"}
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "User not found"}
            )