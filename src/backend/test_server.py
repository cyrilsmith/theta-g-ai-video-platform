import pytest
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_login(client):
    response = client.post('/login', json={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_generate(client):
    response = client.post('/login', json={'username': 'testuser', 'password': 'testpassword'})
    token = response.get_json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    with open('sample_video.mp4', 'rb') as f:
        data = {'file': f}
        response = client.post('/generate', headers=headers, data=data)
        assert response.status_code == 200
        assert 'video_uri' in response.get_json()

def test_mint(client):
    response = client.post('/login', json={'username': 'testuser', 'password': 'testpassword'})
    token = response.get_json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    response = client.post('/mint', headers=headers, json={'video_uri': 'ipfs://sample_video_uri'})
    assert response.status_code == 200
    assert 'tx_hash' in response.get_json()
