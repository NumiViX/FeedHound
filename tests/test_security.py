import pytest
from datetime import timedelta, datetime, timezone

from jose import jwt

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)


def test_get_password_hash_and_verify_password():
    password = "mysecret"
    hashed = get_password_hash(password)

    assert hashed != password  # ensure hashing occurred
    assert verify_password(password, hashed)
    assert not verify_password("wrong" + password, hashed)


def test_create_access_token_contains_claims():
    data = {"sub": "tester"}
    token = create_access_token(data=data, expides_delta=timedelta(minutes=5))

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded["sub"] == data["sub"]
    assert "exp" in decoded
    # expiration should be in the future
    exp_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    assert exp_time > datetime.now(timezone.utc)
