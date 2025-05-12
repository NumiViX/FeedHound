from typing import Annotated

from fastapi import APIRouter, Depends

from app.schemas.users import UserRead
from app.dependencies.auth import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
):
    return current_user
