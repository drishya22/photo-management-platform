from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.responses import FileResponse
import os
from app.utils.hash_utils import generate_hash
from app.utils.metadata_utils import load_metadata,save_metadata
from app.services.embedding_service import get_image_embedding,get_text_embedding
from app.services.vector_db import add_embedding,search_embeddings, delete_embedding, find_similar_images
from app.services.category_service import classify_image
from app.services.face_service import group_face
from app.utils.face_utils import load_faces
from fastapi.responses import RedirectResponse
from app.services.google_photos_service import create_flow, create_picker_session, get_session, list_media_items
import requests


app=FastAPI(title="Photo Management Platform")

UPLOAD_FOLDER="uploads"

os.makedirs(UPLOAD_FOLDER,exist_ok=True)

ALLOWED_EXTENSIONS={".jpg",".jpeg",".png"}


@app.get("/")
def home():
    return {"message":"Photo Management Platform running"}

@app.post("/upload")
async def upload_image(file: UploadFile=File(...)):
    extension=os.path.splitext(file.filename)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only JPG,JPEG and PNG files are allowed"
        )
    file_bytes=await file.read()
    image_hash=generate_hash(file_bytes)
    metadata=load_metadata()
    for image in metadata:
        if image["hash"]==image_hash:
            return {
                "is_duplicate":True,
                "message":"Duplicate image detected",
                "existing_filename":image["filename"],
                "hash":image_hash
            }
    file_path=os.path.join(UPLOAD_FOLDER,file.filename)
    with open(file_path,"wb") as buffer:
        buffer.write(file_bytes)
    
    embedding=get_image_embedding(file_path)
    similar_images=find_similar_images(embedding,top_k=1)
    if len(similar_images["distances"][0])>0:
        distance=similar_images["distances"][0][0]
        if distance<0.20:
            if os.path.exists(file_path):
                os.remove(file_path)
            return {
                "is_near_duplicate":True,
                "distance": round(distance,4),
                "message":"Near duplicate image detected"
            }
    classification=classify_image(file_path)
    person_id=group_face(file_path,file.filename)

    add_embedding(
        image_id=image_hash,
        embedding=embedding,
        filename=file.filename
    )
    metadata.append({
        "filename":file.filename,
        "hash":image_hash,
        "file_type":extension,
        "category":classification["category"] 
    })
    save_metadata(metadata)
    return {
        "is_duplicate": False,
        "filename":file.filename,
        "saved_to":file_path,
        "file_type": extension,
        "hash":image_hash,
        "category": classification["category"],
        "person_id":person_id
    }

@app.get("/search")
def search_images(query: str):
    query_embeddings=get_text_embedding(query)
    results=search_embeddings(
        embedding=query_embeddings,
        top_k=5
    )
    formatted_results=[]
    documents=results["documents"][0]
    distances=results["distances"][0]

    for filename,distance in zip(documents,distances):
        formatted_results.append({
            "filename":filename,
            "distance":round(distance,4),
            "image_url":f"/images/{filename}"
        })
    return {
        "query":query,
        "results":formatted_results
    }

@app.get("/images/{filename}")
def get_image(filename:str):
    file_path=os.path.join(
        UPLOAD_FOLDER,
        filename
    )
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Image not found"
        )
    return FileResponse(file_path)

@app.get("/images")
def list_images():
    metadata=load_metadata()
    images=[]
    for image in metadata:
        images.append(
            {
                "filename":image["filename"],
                "file_type":image["file_type"],
                "image_url":f"/images/{image['filename']}",
                "category":image.get("category","unknown")
            }
        )
    return {
        "total_images":len(images),
        "images":images
    }

@app.delete("/images/{filename}")
def delete_image(filename: str):
    metadata=load_metadata()
    image_to_delete=None

    for image in metadata:
        if image["filename"]==filename:
            image_to_delete=image
            break

    if image_to_delete is None:
        raise HTTPException(
            status_code=404,
            detail="Image not found"
        )
    file_path=os.path.join(UPLOAD_FOLDER,filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # Clean database records even if file was already missing
    delete_embedding(image_to_delete["hash"])
    metadata.remove(image_to_delete)
    save_metadata(metadata)

    return {
        "message": f"{filename} deleted successfully"
    }

@app.get("/faces")
def get_face_groups():
    return load_faces()

google_flow = None
google_credentials=None

@app.get("/google-photos/connect")
def google_photos_connect():
    global google_flow

    google_flow = create_flow()

    auth_url, state = google_flow.authorization_url(
        access_type="offline"
    )

    return RedirectResponse(auth_url)



@app.get("/auth/callback")
def auth_callback(code: str):
    global google_flow
    global google_credentials

    google_flow.fetch_token(code=code)

    credentials = google_flow.credentials
    google_credentials=credentials

    return {
        "message": "Google Photos authentication successful",
        "token_available": credentials.token is not None,
        "token_type": credentials.token[:20]
    }

@app.get("/google-photos/status")
def google_photos_status():
    return {
        "connected": True,
        "provider": "Google Photos"
    }

@app.get("/google-photos/create-session")
def create_google_photos_session():

    global google_credentials

    if google_credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Please connect Google Photos first"
        )

    session = create_picker_session(
        google_credentials.token
    )

    return session

@app.get("/google-photos/session/{session_id}")
def get_google_session(session_id: str):

    global google_credentials

    return get_session(
        google_credentials.token,
        session_id
    )

@app.get("/google-photos/media-items/{session_id}")
def get_media_items(session_id: str):

    global google_credentials

    return list_media_items(
        google_credentials.token,
        session_id
    )