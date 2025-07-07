from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode_data = data.copy()
    expired_time = (datetime.now(timezone.utc) +
                    (expires_delta or timedelta(minutes=15)))
    to_encode_data.update({"exp": expired_time})
    return jwt.encode(to_encode_data, SECRET_KEY, algorithm=ALGORITHM)
