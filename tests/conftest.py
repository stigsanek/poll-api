from typing import Generator

import pytest
from fastapi.testclient import TestClient

from poll_api.db import SessionLocal
from poll_api.main import app
from poll_api.models.user import User
from tests import FAKE_PASSWORD, urls
from tests.utils import read_json_fixture


@pytest.fixture(scope='session', autouse=True)
def load_fixtures() -> Generator:
    """Load fixtures to database

    Yields:
        Generator: Test case
    """
    db = SessionLocal()
    users = read_json_fixture('users.json')

    for user in users:
        db.add(User(**user))
        db.commit()
    yield
    db.close()


@pytest.fixture(scope='module')
def client() -> Generator:
    """Test client fixture

    Yields:
        Generator: Test client fixture
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope='module')
def auth_admin(client: TestClient) -> dict:
    """Auth headers fixture for superuser

    Args:
        client (TestClient): Test client fixture

    Returns:
        dict: Auth headers
    """
    resp = client.post(
        url=urls.login,
        data={'username': 'admin', 'password': FAKE_PASSWORD}
    )
    access_token = resp.json()['access_token']
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture(scope='module')
def auth_user(client: TestClient) -> dict:
    """Auth headers fixture for user

    Args:
        client (TestClient): Test client fixture

    Returns:
        dict: Auth headers
    """
    resp = client.post(
        url=urls.login,
        data={'username': 'user', 'password': FAKE_PASSWORD}
    )
    access_token = resp.json()['access_token']
    return {'Authorization': f'Bearer {access_token}'}
