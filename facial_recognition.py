import time
import face_recognition
import cv2
import os
import threading
import numpy as np
import requests
import smtplib, ssl


def create_mail_dict(names):
    # open the file in read mode
    file = open("mails.txt", "r")
    dict_mail = {}
    for line in file:
        # split the line into words
        words = line.split()
        # if the first word is in the list of names
        if words[0] in names:
            # add the name and the mail to the dictionary
            dict_mail[words[0]] = words[1]
    return dict_mail


    

def send_api_request(name):
    url = "http://localhost:3000/marge"
    data = {
        "nom": name,
        "date": time.strftime("%d/%m/%Y"),
        "heure": time.strftime("%H:%M:%S")
    }
    requests.post(url, data=data)
    print("Envoi de la reconnaissance faciale")

def send_mail(name, mail):
    email_address = "emargement.face.recognition@gmail.com"
    email_password = ""
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = email_address  # Enter your address
    receiver_email = mail  # Enter receiver address
    password = email_password
    message = """\
    Subject: Presence

    """+ name + """ est arrive(e) a precisement """ + time.strftime("%H:%M:%S") + """ le """ + time.strftime("%d/%m/%Y") + """."""

    print("Envoi du mail"+ message+ "à "+ mail)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

def face_recognition_thread(frame, known_faces, known_names, face_names, dict_mail):
    # Encodage des visages dans la frame
    faces_locations = face_recognition.face_locations(frame)
    if len(faces_locations) != 1:
        return
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
                send_mail(name, dict_mail[name])
                send_api_request(name)
        else:
            face_names.append(name)


# Charger les images d'entraînement encodées
known_faces = []
known_names = []
for name in os.listdir("known_faces_encode"):
    for filename in os.listdir(f"known_faces_encode/{name}"):
        encodings = np.load(f"known_faces_encode/{name}/{filename}")
        if len(encodings) > 0:
            known_faces.append(encodings[0])
            known_names.append(name)

dict_mail = create_mail_dict(known_names)
# Initialisation de la capture vidéo
cap = cv2.VideoCapture(0)
i = 0

# Initialisation de la liste des noms des visages détectés
face_names = []
nb_faces_detected = 0
nb_frames_validation = 0
while True:
    # Capture de la frame
    ret, frame = cap.read()
    if not ret:
        break

    frame_with_alpha = np.zeros((frame.shape[0], frame.shape[1], 4), dtype=np.uint8)
    frame_with_alpha[:, :, :3] = frame
    frame_with_alpha[:,:,3] = 0
    
    if i % 10 == 0:
        # Lancement du thread de reconnaissance faciale
        t = threading.Thread(target=face_recognition_thread, args=(frame, known_faces, known_names, face_names, dict_mail))
        t.start()

    # Affichage d'un oval vert au milieu de la frame
    cv2.ellipse(frame_with_alpha, (int(frame.shape[1]/2), int(frame.shape[0]/2)), (135, 160), 0, 0, 360, (0, 255, 0), 2)

    if len(face_names) > nb_faces_detected:
        
        if "Inconnu" in face_names:
            face_names.remove("Inconnu")
            nb_frames_validation = -100
        else :
            nb_faces_detected = len(face_names)
            nb_frames_validation = 100
            print("Validation de la reconnaissance faciale")
    if nb_frames_validation > 0:
        nb_frames_validation -= 1
        # Affichage de 2 lignes formant un v en bas à gauche de la frame en transparence
        cv2.line(frame_with_alpha, (100, frame.shape[0]-50), (130, frame.shape[0]-80), (0, 255, 0), 2)
        cv2.line(frame_with_alpha, (100, frame.shape[0]-50), (70, frame.shape[0]-100), (0, 255, 0), 2)
        # Affichage du nom du visage détecté en bas à droite de la frame en transparence
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame_with_alpha, face_names[-1], (frame.shape[1]-200, frame.shape[0]-20), font, 1.0, (0, 255, 0), 1)
    if nb_frames_validation < 0:
        nb_frames_validation += 1
        # Affichage dune croix rouge en bas à gauche de la frame en petit
        cv2.line(frame_with_alpha, (100, frame.shape[0]-50), (130, frame.shape[0]-100), (0, 0, 255), 2)
        cv2.line(frame_with_alpha, (130, frame.shape[0]-50), (100, frame.shape[0]-100), (0, 0, 255), 2)
        # Affichage de "t ki" en bas à droite de la frame en rouge
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame_with_alpha, "Inconnue", (frame.shape[1]-200, frame.shape[0]-20), font, 1.0, (0, 0, 255), 1)
    
    cv2.imshow("Webcam", frame_with_alpha)


    # Arrêt si l'utilisateur appuie sur 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    i += 1

# Libération de la capture vidéo et fermeture des fenêtres
cap.release()
cv2.destroyAllWindows()