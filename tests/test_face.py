# tests/test_face.py

import sys

print("Python:", sys.executable)

try:
    import face_recognition_models
    print("face_recognition_models imported")
except Exception as e:
    print("models error:", e)

try:
    import face_recognition
    print("face_recognition imported")
except Exception as e:
    print("face_recognition error:", e)