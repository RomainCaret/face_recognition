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
        print("encodings:")
        print(encodings)
        # on sauvegarde l'encodage dans un fichier
        # Sauvegarder la liste
        # liste = [1, 2, 3, 4, 5]
        # with open('liste.pkl', 'wb') as f:
        #    pickle.dump(liste, f)

        # Create a directory for the name if it doesn't exist
        if not os.path.exists(f"known_faces_encode/{name}"):
            os.makedirs(f"known_faces_encode/{name}")

        np.save(f"known_faces_encode/{name}/{filename}.npy", encodings)
        
        # Charger l'encondage de l'image d'entraînement depuis le fichier
        test = np.load(f"known_faces_encode/{name}/{filename}.npy")
        print("test:")
        print(test)