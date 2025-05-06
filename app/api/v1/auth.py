from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.core.security import (create_access_token,
                               verify_password,
                               ACCESS_TOKEN_EXPIRE_MINUTES)
from app.crud.users import user_crud
from app.schemas.users import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registr", response_model=UserRead)
async def refister(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    existing = await user_crud.get_by_email(user.email, session)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user_crud.create(user, session)


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    user = await user_crud.get_by_email(form_data.username, session)
    if not user or verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(
        data={"sub": user.id},
        expides_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                                       )
    return {"access_token": access_token, "token_type": "bearer"}
