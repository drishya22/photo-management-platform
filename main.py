from fastapi import FastAPI,UploadFile,File,HTTPException
import os
from app.utils.hash_utils import generate_hash
from app.utils.metadata_utils import load_metadata,save_metadata 

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