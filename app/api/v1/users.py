from typing import Annotated

from fastapi import APIRouter, Depends
import logging

from app.schemas.users import UserRead
from app.dependencies.auth import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])

logger = logging.getLogger(__name__)


@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[UserRead, Depends(get_current_active_user)],
):
    logger.debug("Current user %s", current_user.username)
    return current_user

