from typing import Annotated

from fastapi import APIRouter, Depends

from app.schemas.users import UserRead
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[UserRead, Depends(get_current_user)],
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[UserRead, Depends(get_current_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]