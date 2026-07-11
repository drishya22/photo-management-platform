import face_recognition
import numpy as np
from app.utils.face_utils import load_faces, save_faces

def get_face_encoding(image_path):
    image=face_recognition.load_image_file(image_path)
    encodings=face_recognition.face_encodings(image)
    if len(encodings)==0:
        return None
    return encodings[0].tolist()

def group_face(image_path,filename):
    encoding= get_face_encoding(image_path)

    if encoding is None:
        return None
    
    faces=load_faces()
    encoding=np.array(encoding)

    for person_id,data in faces.items():
        stored_encoding=np.array(data["encoding"])
        distance=np.linalg.norm(encoding-stored_encoding)
        if distance<0.6:
            if filename not in data["images"]:
                data["images"].append(filename)
            save_faces(faces)
            return person_id
    new_person_id=f'person_{len(faces)+1}'
    faces[new_person_id]={
        "encoding":encoding.tolist(),
        "images":[filename]
    }

    save_faces(faces)
    return new_person_id

