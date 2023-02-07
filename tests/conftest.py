from typing import Generator

import pytest
from fastapi.testclient import TestClient

from poll_api.db import SessionLocal, engine
from poll_api.main import app
from poll_api.models import Base, Choice, Question, User
from tests import FAKE_PASSWORD, urls
from tests.utils import read_json_fixture


@pytest.fixture(scope='module', autouse=True)
def load_fixtures() -> Generator:
    """Load fixtures to database

    Yields:
        Generator: Test case
    """
    Base.metadata.create_all(engine)
    db = SessionLocal()

    users = read_json_fixture('users.json')
    [db.add(User(**user)) for user in users]
    questions = read_json_fixture('questions.json')
    [db.add(Question(**question)) for question in questions]
    choices = read_json_fixture('choices.json')
    [db.add(Choice(**choice)) for choice in choices]

    db.commit()
    yield
    db.close()
    Base.metadata.drop_all(engine)


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
