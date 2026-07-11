# tests/test_group_face.py

from app.services.face_service import group_face

person = group_face(
    "uploads/selfie.jpg",
    "selfie.jpg"
)

print(person)
