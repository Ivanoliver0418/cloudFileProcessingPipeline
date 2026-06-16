from fastapi import FastAPI, File, UploadFile
from pathlib import Path
import shutil
from uuid import uuid4

# Creates a path called uploads
UPLOAD_DIR = Path("uploads")

# Creates uploads if it doesn't already exist
UPLOAD_DIR.mkdir(exist_ok=True)

# Temporary db
files_db = {}

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Cloud File Processing Pipeline API is running"}

# Checks if the API is alive
@app.get("/health")
def get_health():
    return {"status":"ok"}

# Client sends file to the req body
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Creates a unique filename for files with the same name
    stored_filename = f"{uuid4()}_{file.filename}"
    # Builds full path where the files will be saved
    file_path = UPLOAD_DIR / stored_filename
    
    # Open a new file in write binary mode so PDFs, images, videos, etc. could be uploaded
    with file_path.open("wb") as buffer:
        file_id = str(uuid4())
        
        # Copy the uploaded file's content into the new file. (fsrc = file.file, fdst = buffer)
        shutil.copyfileobj(file.file, buffer)
        
        # Return metadata from the uploaded file/s
    files_db[file_id] = {
        "id": file_id,
        "original_filename": file.filename,
        "stored_filename": stored_filename,
        "saved_path": str(file_path),
        "status": "uploaded"
        }
        
    return files_db[file_id]
    
@app.get("/files/{file_id}")
async def get_file(file_id: str):
    return files_db[file_id]