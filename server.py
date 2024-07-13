from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import tensorflow as tf
import numpy as np
import os
from ai_model import preprocess_input
from moviepy.editor import VideoFileClip, concatenate_videoclips

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

model = tf.keras.models.load_model('video_generator_model.h5')

users = {'testuser': 'testpassword'}

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username not in users or users[username] != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/generate', methods=['POST'])
@jwt_required()
def generate_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        file_path = os.path.join('/tmp', file.filename)
        file.save(file_path)
        input_data = preprocess_input(file_path)
        prediction = model.predict(input_data)
        # Example: Concatenate input video with a generated video clip
        input_clip = VideoFileClip(file_path)
        generated_clip = VideoFileClip('path_to_generated_clip.mp4')  # Placeholder path
        final_clip = concatenate_videoclips([input_clip, generated_clip])
        final_clip_path = '/tmp/final_output.mp4'
        final_clip.write_videofile(final_clip_path)
        response = {
            'video_uri': 'ipfs://generated-video-uri'  # Placeholder URI
        }
        return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
