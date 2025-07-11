from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.core.security import (create_access_token,
                               verify_password
                               )
from app.crud.users import user_crud
from app.schemas.auth import Token
from app.schemas.users import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    logger.debug("Read items token %s", token)
    return {"token": token}


@router.post("/register", response_model=UserRead)
async def register(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    logger.info("Registering user %s", user.username)
    existing_email = await user_crud.get_by_email(user.email, session)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_username = await user_crud.get_by_username(user.username, session)
    if existing_username:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    created = await user_crud.create(user, session)
    logger.debug("Registered user %s", created.id)
    return created


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
) -> Token:
    logger.debug("Login attempt for %s", form_data.username)
    user = await user_crud.get_by_username(form_data.username, session)
    if not user or not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    logger.info("User %s logged in", user.username)
    return Token(access_token=access_token, token_type="bearer")

