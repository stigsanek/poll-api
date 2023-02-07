from fastapi.testclient import TestClient

from tests import urls


def test_no_auth(client: TestClient) -> None:
    """Test endpoints no auth

    Args:
        client (TestClient): Test client fixture
    """
    resp = client.get(url=urls.questions)
    assert resp.status_code == 401

    resp = client.get(url=f'{urls.questions}/1')
    assert resp.status_code == 401

    resp = client.patch(url=f'{urls.questions}/1')
    assert resp.status_code == 401

    resp = client.delete(url=f'{urls.questions}/1')
    assert resp.status_code == 401


def test_get_list(client: TestClient, auth_user: dict) -> None:
    """Test return question list

    Args:
        client (TestClient): Test client fixture
        auth_user (dict): Auth headers fixture
    """
    resp = client.get(url=urls.questions, headers=auth_user)
    resp_data = resp.json()

    assert resp.status_code == 200
    assert len(resp_data) == 2


def test_create(client: TestClient, auth_user: dict) -> None:
    """Test create question

    Args:
        client (TestClient): Test client fixture
        auth_user (dict): Auth headers fixture
    """
    data = {'text': 'Test'}

    resp = client.post(url=urls.questions, headers=auth_user, json=data)
    assert resp.status_code == 422

    data['choices'] = [{'text': 'Test1'}, {'text': 'Test2'}]
    resp = client.post(url=urls.questions, headers=auth_user, json=data)
    resp_data = resp.json()

    assert resp.status_code == 201
    assert len(resp_data['choices']) == 2


def test_get(client: TestClient, auth_user: dict) -> None:
    """Test return question

    Args:
        client (TestClient): Test client fixture
        auth_user (dict): Auth headers fixture
    """
    resp = client.get(url=f'{urls.questions}/10', headers=auth_user)
    assert resp.status_code == 404

    resp = client.get(url=f'{urls.questions}/1', headers=auth_user)
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data['user_id'] == 1


def test_update(client: TestClient, auth_user: dict) -> None:
    """Test update question

    Args:
        client (TestClient): Test client fixture
        auth_user (dict): Auth headers fixture
    """
    data = {'text': 'Test'}

    resp = client.patch(
        url=f'{urls.questions}/10',
        headers=auth_user,
        json=data
    )
    assert resp.status_code == 404

    resp = client.patch(
        url=f'{urls.questions}/1',
        headers=auth_user,
        json=data
    )
    assert resp.status_code == 403

    resp = client.patch(
        url=f'{urls.questions}/2',
        headers=auth_user,
        json=data
    )
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data['text'] == 'Test'


def test_delete(client: TestClient, auth_user: dict) -> None:
    """Test delete question

    Args:
        client (TestClient): Test client fixture
        auth_user (dict): Auth headers fixture
    """
    resp = client.delete(url=f'{urls.questions}/10', headers=auth_user)
    assert resp.status_code == 404

    resp = client.delete(url=f'{urls.questions}/1', headers=auth_user)
    assert resp.status_code == 403

    resp = client.delete(url=f'{urls.questions}/2', headers=auth_user)
    assert resp.status_code == 204
