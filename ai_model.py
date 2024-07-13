import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras import layers, models
import numpy as np

def build_model():
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(256, 256, 3))
    base_model.trainable = False  # Freeze the base model

    model = models.Sequential([
        base_model,
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1024, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def preprocess_input(video_file_path):
    import cv2
    cap = cv2.VideoCapture(video_file_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (256, 256))
        frames.append(frame)
    cap.release()
    frames = np.array(frames)
    frames = frames / 255.0  # Normalize to [0, 1]
    return frames

def train_model(model, train_images, train_labels):
    model.fit(train_images, train_labels, epochs=20, batch_size=32, validation_split=0.2)
    model.save('video_generator_model.h5')
