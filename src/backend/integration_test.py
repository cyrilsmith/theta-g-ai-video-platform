import pytest
import requests

BASE_URL = "http://localhost:5000"

def test_login():
    response = requests.post(f"{BASE_URL}/login", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_generate_video():
    login_response = requests.post(f"{BASE_URL}/login", json={"username": "testuser", "password": "testpassword"})
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    with open('sample_video.mp4', 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{BASE_URL}/generate", files=files, headers=headers)
        
    assert response.status_code == 200
    assert "video_uri" in response.json()

def test_mint_nft():
    login_response = requests.post(f"{BASE_URL}/login", json={"username": "testuser", "password": "testpassword"})
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    video_uri = "ipfs://sample_video_uri"
    response = requests.post(f"{BASE_URL}/mint", json={"video_uri": video_uri}, headers=headers)
    
    assert response.status_code == 200
    assert "tx_hash" in response.json()
