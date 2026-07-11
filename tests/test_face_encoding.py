# tests/test_face_encoding.py

import face_recognition

image = face_recognition.load_image_file(
    "uploads/selfie.jpg"
)

encodings = face_recognition.face_encodings(image)

print("Faces found:", len(encodings))

if len(encodings) > 0:
    print("Embedding length:", len(encodings[0]))