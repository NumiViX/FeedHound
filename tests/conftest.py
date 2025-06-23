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

# Provide a lightweight stub for the `httpx` library if it's unavailable.
if 'httpx' not in sys.modules:
    httpx_module = ModuleType('httpx')

    class ByteStream:
        def __init__(self, content: bytes):
            self._content = content

        def read(self) -> bytes:
            return self._content

    class Request:
        def __init__(self, method: str, url: str, headers=None, stream=None):
            self.method = method
            self.url = SimpleNamespace(
                scheme=url.split('://')[0],
                netloc=url.split('://')[1].split('/')[0].encode(),
                path='/' + '/'.join(url.split('://')[1].split('/')[1:]),
                raw_path=('/' + '/'.join(url.split('://')[1].split('/')[1:])).encode(),
                query=b"",
            )
            self.headers = headers or {}
            self._stream = stream or ByteStream(b"")

        def read(self):
            return self._stream.read()

    class Response:
        def __init__(self, status_code: int, headers=None, stream=None, request=None):
            self.status_code = status_code
            self.headers = headers or []
            self._stream = stream or ByteStream(b"")
            self.request = request

        def json(self):
            import json as _json
            return _json.loads(self._stream.read().decode())

    class BaseTransport:
        def handle_request(self, request: Request) -> Response:  # pragma: no cover - stub
            raise NotImplementedError

    class Client:
        def __init__(self, *, app=None, base_url: str = "", headers=None, transport=None, follow_redirects=True, cookies=None):
            self.app = app
            self.base_url = base_url
            self.headers = headers or {}
            self.transport = transport

        def request(self, method: str, url: str, **kwargs) -> Response:
            url = self.base_url.rstrip('/') + '/' + url.lstrip('/')
            headers = kwargs.get('headers', {})
            stream = ByteStream(kwargs.get('content', b""))
            req = Request(method, url, headers=headers, stream=stream)
            return self.transport.handle_request(req)

        def get(self, url: str, **kwargs) -> Response:
            return self.request('GET', url, **kwargs)

        def post(self, url: str, **kwargs) -> Response:
            return self.request('POST', url, **kwargs)

    _client_module = ModuleType('httpx._client')
    _client_module.USE_CLIENT_DEFAULT = object()
    sys.modules['httpx._client'] = _client_module

    httpx_module.Client = Client
    httpx_module.BaseTransport = BaseTransport
    httpx_module.Request = Request
    httpx_module.Response = Response
    httpx_module.ByteStream = ByteStream
    sys.modules['httpx'] = httpx_module

# Provide a minimal stub for SQLAlchemy so imports succeed when the real
# package isn't installed. This allows tests to skip gracefully.
if 'sqlalchemy' not in sys.modules:
    sa_module = ModuleType('sqlalchemy')
    sa_module.ext = ModuleType('sqlalchemy.ext')
    sa_asyncio = ModuleType('sqlalchemy.ext.asyncio')
    sa_asyncio.create_async_engine = None
    sa_asyncio.async_sessionmaker = None
    sa_asyncio.AsyncSession = type('AsyncSession', (), {})
    sa_module.ext.asyncio = sa_asyncio
    sys.modules['sqlalchemy.ext'] = sa_module.ext
    sys.modules['sqlalchemy.ext.asyncio'] = sa_asyncio

    sa_future = ModuleType('sqlalchemy.future')
    sa_future.select = lambda *a, **k: None
    sa_module.future = sa_future
    sys.modules['sqlalchemy.future'] = sa_future

    sa_orm = ModuleType('sqlalchemy.orm')
    sa_orm.DeclarativeBase = type('DeclarativeBase', (), {})
    sa_orm.relationship = lambda *a, **k: None
    sa_module.orm = sa_orm
    sys.modules['sqlalchemy.orm'] = sa_orm

    def _column(*args, **kwargs):
        return None

    sa_module.Column = _column
    for name in ['Integer', 'String', 'DateTime', 'Boolean', 'ForeignKey']:
        setattr(sa_module, name, type(name, (), {}))

    sys.modules['sqlalchemy'] = sa_module

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
