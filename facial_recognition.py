import face_recognition
import cv2
import os
import threading
import time

def face_recognition_thread(frame, known_faces, known_names, face_names):
    # Encodage des visages dans la frame
    faces_locations = face_recognition.face_locations(frame)
    faces_encodings = face_recognition.face_encodings(frame, faces_locations)

    # Pour chaque visage détecté
    for face_encoding, face_location in zip(faces_encodings, faces_locations):
        # Comparaison avec les images d'entraînement
        matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.5)
        name = "Inconnu"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
            if name not in face_names:
                face_names.append(name)
            # Affichage du nom du visage détecté

# Charger les images d'entraînement
known_faces = []
known_names = []
for name in os.listdir("known_faces"):
    for filename in os.listdir(f"known_faces/{name}"):
        image = face_recognition.load_image_file(f"known_faces/{name}/{filename}")
        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 0:
            known_faces.append(encodings[0])
            known_names.append(name)

# Initialisation de la capture vidéo
cap = cv2.VideoCapture(0)
i = 0

# Initialisation de la liste des noms des visages détectés
face_names = []

while True:
    # Capture de la frame
    ret, frame = cap.read()
    if not ret:
        break
    
    if i % 10 == 0:
        # Lancement du thread de reconnaissance faciale
        t = threading.Thread(target=face_recognition_thread, args=(frame, known_faces, known_names, face_names))
        t.start()
    
    if i % 100 == 0:
        # Affichage des noms des visages détectés
        print("--------------------")
        for name in face_names:
            print("Elève présent: ", name)

    i += 1
    # Affichage de l'image avec les visages détectés et étiquetés
    cv2.imshow("Webcam", frame)

    # Arrêt si l'utilisateur appuie sur 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libération de la capture vidéo et fermeture des fenêtres
cap.release()
cv2.destroyAllWindows()
