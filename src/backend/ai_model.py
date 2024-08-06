import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
import numpy as np
import cv2

def build_model():
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False
    
    model = Sequential([
        base_model,
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(10, activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

def preprocess_frame(frame):
    frame = cv2.resize(frame, (224, 224))
    frame = tf.keras.applications.vgg16.preprocess_input(frame)
    return frame

def video_generator(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = preprocess_frame(frame)
        yield np.expand_dims(frame, axis=0)
    cap.release()

def train_model(model, train_images, train_labels):
    model.fit(train_images, train_labels, epochs=10, batch_size=32, validation_split=0.2)
    model.save('video_generator_model.h5')
    return model

# Example usage
# model = build_model()
# train_model(model, train_images, train_labels)
