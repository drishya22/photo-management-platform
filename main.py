from fastapi import FastAPI,UploadFile,File,HTTPException
import os

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
    file_path=os.path.join(UPLOAD_FOLDER,file.filename)
    with open(file_path,"wb") as buffer:
        buffer.write(await file.read())
    return {
        "filename":file.filename,
        "saved_to":file_path
    }