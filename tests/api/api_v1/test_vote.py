from fastapi.testclient import TestClient

from tests import urls


def test_no_auth(client: TestClient) -> None:
    """Test endpoints no auth

    Args:
        client (TestClient): Test client fixture
    """
    resp = client.get(url=urls.votes)
    assert resp.status_code == 401

    resp = client.post(url=urls.votes)
    assert resp.status_code == 401

    resp = client.delete(url=f'{urls.votes}/1')
    assert resp.status_code == 401


def test_get_list(client: TestClient, auth_user: dict) -> None:
    """Test return vote list

    Args:
        client (TestClient): Test client fixture
        auth_user (dict): Auth headers fixture
    """
    resp = client.get(url=f'{urls.votes}?question_id=1', headers=auth_user)
    resp_data = resp.json()

    assert resp.status_code == 200
    assert len(resp_data) == 3


def test_create(client: TestClient, auth_user: dict) -> None:
    """Test create vote

    Args:
        client (TestClient): Test client fixture
        auth_user (dict): Auth headers fixture
    """
    resp = client.post(
        url=urls.votes,
        headers=auth_user,
        json={'question_id': 10, 'choice_id': 2}
    )
    resp_data = resp.json()
    assert resp.status_code == 400
    assert 'incorrect choice or question' in resp_data['detail'].lower()

    resp = client.post(
        url=urls.votes,
        headers=auth_user,
        json={'question_id': 1, 'choice_id': 1}
    )
    resp_data = resp.json()
    assert resp.status_code == 400
    assert 'already exists' in resp_data['detail'].lower()

    resp = client.post(
        url=urls.votes,
        headers=auth_user,
        json={'question_id': 2, 'choice_id': 4}
    )
    resp_data = resp.json()
    assert resp.status_code == 201
    assert resp_data['question_id'] == 2
    assert resp_data['choice_id'] == 4


def test_delete(client: TestClient, auth_user: dict) -> None:
    """Test delete vote

    Args:
        client (TestClient): Test client fixture
        auth_user (dict): Auth headers fixture
    """
    resp = client.delete(url=f'{urls.votes}/10', headers=auth_user)
    assert resp.status_code == 404

    resp = client.delete(url=f'{urls.votes}/3', headers=auth_user)
    assert resp.status_code == 403

    resp = client.delete(url=f'{urls.votes}/2', headers=auth_user)
    assert resp.status_code == 204
