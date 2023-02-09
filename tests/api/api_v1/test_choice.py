from fastapi.testclient import TestClient

from tests import urls


def test_no_auth(client: TestClient) -> None:
    """Test endpoints no auth

    Args:
        client (TestClient): Test client fixture
    """
    resp = client.get(url=f'{urls.choices}/1')
    assert resp.status_code == 401

    resp = client.patch(url=f'{urls.choices}/1')
    assert resp.status_code == 401

    resp = client.delete(url=f'{urls.choices}/1')
    assert resp.status_code == 401


def test_get(client: TestClient, auth_user: dict) -> None:
    """Test return choice

    Args:
        client (TestClient): Test client fixture
        auth_user (dict): Auth headers fixture
    """
    resp = client.get(url=f'{urls.choices}/10', headers=auth_user)
    assert resp.status_code == 404

    resp = client.get(url=f'{urls.choices}/1', headers=auth_user)
    assert resp.status_code == 200


def test_update(client: TestClient, auth_user: dict) -> None:
    """Test update choice

    Args:
        client (TestClient): Test client fixture
        auth_user (dict): Auth headers fixture
    """
    data = {'text': 'Test'}

    resp = client.patch(
        url=f'{urls.choices}/10',
        headers=auth_user,
        json=data
    )
    assert resp.status_code == 404

    resp = client.patch(
        url=f'{urls.choices}/1',
        headers=auth_user,
        json=data
    )
    assert resp.status_code == 403

    resp = client.patch(
        url=f'{urls.choices}/4',
        headers=auth_user,
        json=data
    )
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data['text'] == 'Test'


def test_delete(client: TestClient, auth_user: dict) -> None:
    """Test delete choice

    Args:
        client (TestClient): Test client fixture
        auth_user (dict): Auth headers fixture
    """
    resp = client.delete(url=f'{urls.choices}/10', headers=auth_user)
    assert resp.status_code == 404

    resp = client.delete(url=f'{urls.choices}/1', headers=auth_user)
    assert resp.status_code == 403

    resp = client.delete(url=f'{urls.choices}/4', headers=auth_user)
    assert resp.status_code == 204
