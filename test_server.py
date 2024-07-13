import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_generate_video(client):
    response = client.post('/generate', json={'input': [0]*256*256*3})
    json_data = response.get_json()
    assert response.status_code == 200
    assert 'video_uri' in json_data
