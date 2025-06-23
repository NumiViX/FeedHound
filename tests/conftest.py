import sys
import json
from types import ModuleType, SimpleNamespace

# Provide a lightweight stub for `jose.jwt` if the real library is unavailable.
if 'jose' not in sys.modules:
    jose_module = ModuleType('jose')
    def _encode(data, key, algorithm=None):
        processed = {
            k: (int(v.timestamp()) if hasattr(v, "timestamp") else v)
            for k, v in data.items()
        }
        return json.dumps(processed)

    def _decode(token, key, algorithms=None):
        return json.loads(token)

    jwt_ns = SimpleNamespace(encode=_encode, decode=_decode)
    jose_module.jwt = jwt_ns
    sys.modules['jose'] = jose_module
    sys.modules['jose.jwt'] = jwt_ns

# Minimal stub for `passlib.context.CryptContext` if `passlib` isn't available.
if 'passlib.context' not in sys.modules:
    passlib_context_module = ModuleType('passlib.context')

    class DummyCryptContext:
        def __init__(self, schemes=None, deprecated='auto'):
            pass

        def hash(self, password: str) -> str:
            return 'hashed-' + password

        def verify(self, plain_password: str, hashed_password: str) -> bool:
            return self.hash(plain_password) == hashed_password

    passlib_context_module.CryptContext = DummyCryptContext

    # Ensure "passlib" package exists and exposes the context module
    passlib_pkg = sys.modules.setdefault('passlib', ModuleType('passlib'))
    passlib_pkg.context = passlib_context_module
    sys.modules['passlib.context'] = passlib_context_module

import pytest

try:
    from sqlalchemy.ext.asyncio import (
        create_async_engine,
        async_sessionmaker,
        AsyncSession,
    )
    from app.db.base import Base
except Exception:  # pragma: no cover - SQLAlchemy may be missing
    create_async_engine = async_sessionmaker = AsyncSession = None
    Base = None


@pytest.fixture()
async def async_session():
    """Create an in-memory SQLite session for testing."""
    if create_async_engine is None:
        pytest.skip("SQLAlchemy is not available")
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    async_session_maker = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session_maker() as session:
        yield session
    await engine.dispose()
