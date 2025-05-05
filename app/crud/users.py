from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.users import User
from app.schemas.users import UserCreate
from app.core.security import get_password_hash


class UserCRUD:
    async def get_by_email(self, email: str, session: AsyncSession):
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

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
        return user


user_crud = UserCRUD()
