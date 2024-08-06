from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import os
from ai_model import build_model, video_generator

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '3edbbddec62551fa96ef0e01d98a24a9aee48c892381b61083a48b962842a51c'
jwt = JWTManager(app)

model = build_model()

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    # Add your user authentication logic here
    if username == 'testuser' and password == 'testpassword':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/generate', methods=['POST'])
@jwt_required()
def generate():
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400
    video_path = os.path.join('/tmp', file.filename)
    file.save(video_path)
    
    for frame in video_generator(video_path):
        # Add frame processing logic here
        pass
    
    return jsonify(video_uri="ipfs://sample_video_uri")

@app.route('/mint', methods=['POST'])
@jwt_required()
def mint():
    video_uri = request.json.get('video_uri')
    # Add smart contract interaction logic here
    tx_hash = "sample_tx_hash"
    return jsonify(tx_hash=tx_hash)

if __name__ == '__main__':
    app.run(debug=True)
