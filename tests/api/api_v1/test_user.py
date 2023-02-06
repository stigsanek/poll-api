from fastapi.testclient import TestClient

from tests import FAKE_PASSWORD, urls


def test_no_auth(client: TestClient) -> None:
    """Test return user list no auth

    Args:
        client (TestClient): Test client fixture
    """
    resp = client.get(url=urls.users)
    assert resp.status_code == 401

    resp = client.get(url=f'{urls.users}/1')
    assert resp.status_code == 401

    resp = client.patch(url=f'{urls.users}/1')
    assert resp.status_code == 401

    resp = client.delete(url=f'{urls.users}/1')
    assert resp.status_code == 401


def test_get_list_for_admin(client: TestClient, auth_admin: dict) -> None:
    """Test return user list for superuser

    Args:
        client (TestClient): Test client fixture
        auth_admin (dict): Auth headers fixture
    """
    resp = client.get(url=urls.users, headers=auth_admin)
    resp_data = resp.json()

    assert resp.status_code == 200
    assert len(resp_data) == 3


def test_get_list_for_user(client: TestClient, auth_user: dict) -> None:
    """Test return user list for user

    Args:
        client (TestClient): Test client fixture
        auth_user (dict): Auth headers fixture
    """
    resp = client.get(url=urls.users, headers=auth_user)
    assert resp.status_code == 403


def test_create(client: TestClient) -> None:
    """Test create user

    Args:
        client (TestClient): Test client fixture
    """
    data = {
        'username': 'test',
        'first_name': 'Test',
        'last_name': 'Test',
        'password': FAKE_PASSWORD,
    }
    resp = client.post(url=urls.users, json=data)
    resp_data = resp.json()

    assert resp.status_code == 400
    assert 'already exists' in resp_data['detail'].lower()

    data['username'] = 'test1'
    resp = client.post(url=urls.users, json=data)

    assert resp.status_code == 201
