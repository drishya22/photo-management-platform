import json
import os

FACE_FILE="data/faces.json"

def load_faces():
    if not os.path.exists(FACE_FILE):
        return {}
    with open(FACE_FILE,"r") as f:
        return json.load(f)
    
def save_faces(data):
    with open(FACE_FILE,"w") as f:
        json.dump(data,f,indent=4)

        
    