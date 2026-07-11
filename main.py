from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.responses import FileResponse
import os
from app.utils.hash_utils import generate_hash
from app.utils.metadata_utils import load_metadata,save_metadata
from app.services.embedding_service import get_image_embedding,get_text_embedding
from app.services.vector_db import add_embedding,search_embeddings, delete_embedding
from app.services.category_service import classify_image


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
    classification=classify_image(file_path)

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
        "category": classification["category"]
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
