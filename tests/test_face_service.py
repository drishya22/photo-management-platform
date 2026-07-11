# tests/test_face_service.py

from app.services.face_service import get_face_encoding

encoding = get_face_encoding(
    "uploads/selfie.jpg"
)

if encoding:
    print("Length:", len(encoding))
else:
    print("No face found")