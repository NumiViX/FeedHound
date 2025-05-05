from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext


SECRET_KEY = "your-secret-key"
ALGORITH = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expides_delta: timedelta | None = None):
    to_encode_date = data.copy()
    expired_time = (datetime.now(datetime.timezone.utc) +
                    (expides_delta or timedelta(minutes=15)))
    to_encode_date.update({"exp": expired_time})
    return jwt.encode(to_encode_date, SECRET_KEY, algorithm=ALGORITH)
