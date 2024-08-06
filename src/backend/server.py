from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from web3 import Web3
import os
from ai_model import build_model, video_generator, process_frame, save_video
import json
import ipfshttpclient
import time
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_folder='src/frontend/build', static_url_path='')
app.config['JWT_SECRET_KEY'] = '3edbbddec62551fa96ef0e01d98a24a9aee48c892381b61083a48b962842a51c'
jwt = JWTManager(app)

# In-memory store for users (username -> hashed_password)
users = {}

model = build_model()

# Web3 configuration
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/847ad4f9b62142ea9e09e2e593c9d327'))
contract_address = Web3.toChecksumAddress('0x3cb22617bdd8275875b358872d2c16c2b7ba011d')
with open('contractABI.json', 'r') as f:
    contract_abi = f.read()

contract = w3.eth.contract(address=contract_address, abi=contract_abi)
private_key = os.getenv('PRIVATE_KEY')
account_address = w3.eth.account.privateKeyToAccount(private_key).address

@app.route('/register', methods=['POST'])
def register():
    """
    Registers a new user with a username and password.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    
    if username in users:
        return jsonify({"msg": "User already exists"}), 400
    
    hashed_password = generate_password_hash(password)
    users[username] = hashed_password
    
    return jsonify({"msg": "User registered successfully"}), 200

@app.route('/login', methods=['POST'])
def login():
    """
    Logs in a user and returns a JWT token.
    """
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    
    user_password_hash = users.get(username)
    if not user_password_hash or not check_password_hash(user_password_hash, password):
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/generate', methods=['POST'])
@jwt_required()
def generate():
    """
    Generates a processed video and uploads it to IPFS.
    """
    try:
        if 'file' not in request.files:
            return jsonify({"msg": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"msg": "No selected file"}), 400
        video_path = os.path.join('/tmp', file.filename)
        file.save(video_path)
        
        processed_frames = []
        for frame in video_generator(video_path):
            processed_frame = process_frame(frame)
            processed_frames.append(processed_frame)
        
        processed_video_path = os.path.join('/tmp', 'processed_' + file.filename)
        save_video(processed_video_path, processed_frames)
        
        # Upload to IPFS
        client = ipfshttpclient.connect()
        res = client.add(processed_video_path)
        ipfs_uri = f"ipfs://{res['Hash']}"
        
        return jsonify(video_uri=ipfs_uri)
    except Exception as e:
        logging.error(f"Error in generate endpoint: {e}")
        return jsonify({"msg": "Error processing video"}), 500

@app.route('/mint', methods=['POST'])
@jwt_required()
def mint():
    """
    Mints an NFT with the provided video URI and metadata.
    """
    try:
        video_uri = request.json.get('video_uri')
        if not video_uri:
            return jsonify({"msg": "Missing video URI"}), 400
        
        # Metadata for the NFT
        metadata = {
            "name": "Video NFT",
            "description": "An NFT representing a processed video.",
            "video": video_uri,
            "attributes": [
                {"trait_type": "Resolution", "value": "1080p"},
                {"trait_type": "Frame Rate", "value": "30fps"},
                {"trait_type": "Duration", "value": "2 minutes"},
                {"trait_type": "Effects", "value": "Grayscale, Blur, Edge Detection, Object Detection, Face Blur, Color Adjustment, Motion Detection"}
            ]
        }
        
        # Upload metadata to IPFS
        client = ipfshttpclient.connect()
        res = client.add_json(metadata)
        metadata_uri = f"ipfs://{res}"
        
        nonce = w3.eth.getTransactionCount(account_address)
        txn = contract.functions.createNFT(metadata_uri).buildTransaction({
            'chainId': 11155111,  # Sepolia chain ID
            'gas': 2000000,
            'gasPrice': w3.toWei('20', 'gwei'),
            'nonce': nonce,
        })
        signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key)
        tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return jsonify(tx_hash=tx_hash.hex())
    except Exception as e:
        logging.error(f"Error in mint endpoint: {e}")
        return jsonify({"msg": "Error minting NFT"}), 500

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
