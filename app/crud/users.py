from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from app.core.security import get_password_hash
from app.models.users import User
from app.schemas.users import UserCreate

logger = logging.getLogger(__name__)


class UserCRUD:
    async def get_by_username(self, username: str, session: AsyncSession):
        result = await session.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()
        logger.debug("Fetched user by username %s: %s", username, bool(user))
        return user

    async def get_by_email(self, email: str, session: AsyncSession):
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        logger.debug("Fetched user by email %s: %s", email, bool(user))
        return user

    async def create(self, user_data: UserCreate, session: AsyncSession):
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        logger.debug("Created user %s", user.id)
        return user


user_crud = UserCRUD()

