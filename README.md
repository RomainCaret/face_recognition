# Facial Recognition

Recognition by minimum norm between vectors (128D dlib descriptor)
![Alt Text](readme.gif)


### Prerequisites

#### Install requirements

Make sure to have the following libraries installed in your Python environment:

- opencv
- dlib
- numpy
- face_recognition

```
pip install opencv-python
pip install dlib-19.22.99-cp310-cp310-win_amd64.whl
pip install face_recognition
pip install requests
```

#### Setup faces to recognize

Update the `known_faces` directory with images of people you want to detect and be sure to crop around the faces as the Zuckerberg example (if you don't, the program execution might raise an error).

Please only use .jpg or .png image format files in the `known_faces` folder.

For instance, you may have the following files:

```
/known_faces/Zuckerberg.png
/known_faces/YourPicture.jpg
```

Note that the recognition name displayed is taken from the file name (without extension) it matches in the `known_faces` folder.

#### Camera

You need a camera connected to your PC since the program will stream the image of camera on your screen and will recognize the face displayed should the face be part of the `known_faces` folder.

### Run encode_pictures.py

For safety reasons, we do not use pictures directly but use vectors that enable to detect the face without having a full time access to pictures of people. After you run this script the folder `known_faces_encode` should have been created with all the vector of the faces.

## Run

```
python facial_recognition.py
```

You should see the camera detecting faces if everything is setup correctly

### Authors

Romain Caret
Moncif Matallah
Djalil El BG