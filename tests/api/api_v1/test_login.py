from fastapi.testclient import TestClient

from poll_api.config import settings
from tests import FAKE_PASSWORD


def test_success_login(client: TestClient) -> None:
    """Test success login

    Args:
        client (TestClient): Test client fixture
    """
    resp = client.post(
        url=f'{settings.API_V1}/login',
        data={'username': 'admin', 'password': FAKE_PASSWORD}
    )
    resp_data = resp.json()

    assert resp.status_code == 200
    assert 'access_token' in resp_data
    assert resp_data['access_token']


def test_err_login(client: TestClient) -> None:
    """Test error login

    Args:
        client (TestClient): Test client fixture
    """
    resp = client.post(
        url=f'{settings.API_V1}/login',
        data={'username': 'admin', 'password': 'test'}
    )
    resp_data = resp.json()

    assert resp.status_code == 400
    assert 'incorrect' in resp_data['detail'].lower()

    resp = client.post(
        url=f'{settings.API_V1}/login',
        data={'username': 'test', 'password': FAKE_PASSWORD}
    )
    resp_data = resp.json()

    assert resp.status_code == 400
    assert 'inactive' in resp_data['detail'].lower()
