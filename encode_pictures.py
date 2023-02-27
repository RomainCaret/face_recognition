import face_recognition
import os
import pickle
import numpy as np
import os

# Charger les images d'entraînement
for name in os.listdir("known_faces"):
    for filename in os.listdir(f"known_faces/{name}"):
        image = face_recognition.load_image_file(f"known_faces/{name}/{filename}")
        encodings = face_recognition.face_encodings(image)

        # Create a directory for the name if it doesn't exist
        if not os.path.exists(f"known_faces_encode/{name}"):
            os.makedirs(f"known_faces_encode/{name}")

        np.save(f"known_faces_encode/{name}/{filename}.npy", encodings)