from jose import jwt, JWTError

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import SECRET_KEY, ALGORITH
from app.db.session import get_async_session
from app.models.users import User

oauth2_csheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
        token: str = Depends(oauth2_csheme),
        session: AsyncSession = Depends(get_async_session)
):
    credentials_eception = HTTPException(
        status_code=401,
        detail="Invalid credential"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITH])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_eception
    except JWTError:
        raise credentials_eception

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_eception
    return user
