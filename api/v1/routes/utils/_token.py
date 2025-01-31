import jwt
from datetime import datetime, timedelta
from config.config import settings

SECRET_KEY = settings.secret_key

def generate_token(email:str, token_type:str, expires_in: int) -> str:
    """Generates a token for email verification"""
    payload = {
        "email": email,
        "type": token_type,
        "exp": datetime.utcnow() + timedelta(minutes=expires_in),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def confirm_token(token: str, expected_type: str) -> str:
    """Confirms token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("email")
        token_type = payload.get("type")
        if email is None or token_type != expected_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type or payload"
            )
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )
