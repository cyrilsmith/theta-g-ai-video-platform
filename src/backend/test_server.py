import pytest
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from web3 import Web3
import os
from ai_model import build_model, video_generator, process_frame, save_video
import json
import ipfshttpclient
import time
import logging
from server import app, users, contract

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register(client):
    response = client.post('/register', json={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert response.get_json() == {"msg": "User registered successfully"}

def test_login(client):
    client.post('/register', json={'username': 'testuser', 'password': 'testpassword'})
    response = client.post('/login', json={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_generate(client):
    client.post('/register', json={'username': 'testuser', 'password': 'testpassword'})
    response = client.post('/login', json={'username': 'testuser', 'password': 'testpassword'})
    token = response.get_json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Create a sample video file for testing
    with open('/tmp/sample_video.mp4', 'wb') as f:
        f.write(b'sample data')
    
    with open('/tmp/sample_video.mp4', 'rb') as f:
        data = {'file': f}
        response = client.post('/generate', headers=headers, data=data)
        assert response.status_code == 200
        assert 'video_uri' in response.get_json()

def test_mint(client):
    client.post('/register', json={'username': 'testuser', 'password': 'testpassword'})
    response = client.post('/login', json={'username': 'testuser', 'password': 'testpassword'})
    token = response.get_json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    response = client.post('/mint', headers=headers, json={'video_uri': 'ipfs://sample_video_uri'})
    assert response.status_code == 200
    assert 'tx_hash' in response.get_json()
