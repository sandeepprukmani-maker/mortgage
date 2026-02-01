import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from unittest.mock import Mock
import redis

from database import Base, get_db
from main import app
from models.user import User
from models.tenant import Tenant
from models.role import Role
from services.password_service import PasswordService

# Test database setup - use aiosqlite for async SQLite
SQLALCHEMY_TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Create a fresh database session for each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database dependency override."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def mock_redis():
    """Create a mock Redis client."""
    redis_mock = Mock(spec=redis.Redis)
    redis_mock.get.return_value = None
    redis_mock.set.return_value = True
    redis_mock.delete.return_value = True
    redis_mock.incr.return_value = 1
    redis_mock.expire.return_value = True
    return redis_mock


@pytest_asyncio.fixture(scope="function")
async def test_tenant(db_session):
    """Create a test tenant."""
    tenant = Tenant(
        company_name="Test Company",
        plan="basic",
        is_active=True
    )
    db_session.add(tenant)
    await db_session.commit()
    await db_session.refresh(tenant)
    return tenant


@pytest_asyncio.fixture(scope="function")
async def test_role(db_session):
    """Create a test role."""
    role = Role(
        name="loan_officer",
        description="Loan Officer Role"
    )
    db_session.add(role)
    await db_session.commit()
    await db_session.refresh(role)
    return role


@pytest_asyncio.fixture(scope="function")
async def test_user(db_session, test_tenant, test_role):
    """Create a test user with local authentication."""
    password_service = PasswordService()
    user = User(
        email="test@example.com",
        password_hash=password_service.hash_password("Test1234"),
        first_name="Test",
        last_name="User",
        auth_provider="local",
        is_email_verified=False,
        tenant_id=test_tenant.id,
        role_id=test_role.id
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def test_google_user(db_session, test_tenant, test_role):
    """Create a test user with Google authentication."""
    user = User(
        email="google@example.com",
        password_hash=None,
        first_name="Google",
        last_name="User",
        auth_provider="google",
        google_id="google123",
        is_email_verified=True,
        tenant_id=test_tenant.id,
        role_id=test_role.id
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture(scope="function")
async def test_admin_role(db_session):
    """Create an admin role."""
    role = Role(
        name="admin",
        description="Administrator Role"
    )
    db_session.add(role)
    await db_session.commit()
    await db_session.refresh(role)
    return role


@pytest_asyncio.fixture(scope="function")
async def test_admin_user(db_session, test_tenant, test_admin_role):
    """Create a test admin user."""
    password_service = PasswordService()
    user = User(
        email="admin@example.com",
        password_hash=password_service.hash_password("Admin1234"),
        first_name="Admin",
        last_name="User",
        auth_provider="local",
        is_email_verified=True,
        tenant_id=test_tenant.id,
        role_id=test_admin_role.id
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_access_token(test_user):
    """Generate a test access token."""
    from services.token_service import TokenService
    token_service = TokenService()
    return token_service.create_access_token(test_user.id, test_user.email)


@pytest_asyncio.fixture(scope="function")
async def test_refresh_token(db_session, test_user):
    """Create a test refresh token."""
    from services.token_service import TokenService
    token_service = TokenService()
    return await token_service.create_refresh_token(test_user.id, db_session)


@pytest.fixture(scope="function")
def authenticated_client(client, test_access_token):
    """Create a test client with authentication headers."""
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {test_access_token}"
    }
    return client
