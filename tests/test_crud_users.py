import pytest

from app.crud.users import UserCRUD
from app.schemas.users import UserCreate


@pytest.mark.asyncio
async def test_user_crud(async_session):
    crud = UserCRUD()
    create_data = UserCreate(
        email="user@example.com",
        username="user",
        password="secret",
    )
    user = await crud.create(create_data, async_session)
    assert user.id is not None

    by_username = await crud.get_by_username("user", async_session)
    assert by_username is not None
    assert by_username.email == "user@example.com"

    by_email = await crud.get_by_email("user@example.com", async_session)
    assert by_email is not None
    assert by_email.username == "user"
