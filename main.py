from fastapi import FastAPI,UploadFile,File,HTTPException
import os
from app.utils.hash_utils import generate_hash
from app.utils.metadata_utils import load_metadata,save_metadata
from app.services.embedding_service import get_image_embedding,get_text_embedding
from app.services.vector_db import add_embedding,search_embeddings

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

    add_embedding(
        image_id=image_hash,
        embedding=embedding,
        filename=file.filename
    )
    metadata.append({
        "filename":file.filename,
        "hash":image_hash,
        "file_type":extension
    })
    save_metadata(metadata)
    return {
        "is_duplicate": False,
        "filename":file.filename,
        "saved_to":file_path,
        "file_type": extension,
        "hash":image_hash
    }

@app.get("/search")
def search_images(query: str):
    query_embeddings=get_text_embedding(query)
    results=search_embeddings(
        embedding=query_embeddings,
        top_k=5
    )
    return results