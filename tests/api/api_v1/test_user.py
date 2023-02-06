from fastapi.testclient import TestClient

from poll_api.config import settings


def test_no_auth(client: TestClient) -> None:
    """Test return user list no auth

    Args:
        client (TestClient): Test client fixture
    """
    url = f'{settings.API_V1}/users'

    resp = client.get(url=url)
    assert resp.status_code == 401

    resp = client.get(url=f'{url}/1')
    assert resp.status_code == 401

    resp = client.patch(url=f'{url}/1')
    assert resp.status_code == 401

    resp = client.delete(url=f'{url}/1')
    assert resp.status_code == 401


def test_get_list_for_admin(client: TestClient, auth_admin: dict) -> None:
    """Test return user list for superuser

    Args:
        client (TestClient): Test client fixture
        auth_admin (dict): Auth headers fixture
    """
    resp = client.get(
        url=f'{settings.API_V1}/users',
        headers=auth_admin
    )
    resp_data = resp.json()

    assert resp.status_code == 200
    assert len(resp_data) == 3


def test_get_list_for_user(client: TestClient, auth_user: dict) -> None:
    """Test return user list for user

    Args:
        client (TestClient): Test client fixture
        auth_user (dict): Auth headers fixture
    """
    resp = client.get(
        url=f'{settings.API_V1}/users',
        headers=auth_user
    )
    assert resp.status_code == 403
