from fastapi import FastAPI, UploadFile, File, Form, HTTPException, logger
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from fastapi import APIRouter, HTTPException
from extractors.passport_extractor import PassportExtractor
from extractors.dl_extractor import DLExtractor
import os
import logging
import json

app = FastAPI(title="KYC Identity Verification API")

# Add this CORS middleware configuration right after creating the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's address
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define directories
UPLOAD_DIRECTORY = "./uploads"
PROCESSED_DATA_DIRECTORY = "./processed_data"
PASSPORT_DIRECTORY = os.path.join(UPLOAD_DIRECTORY, "passport")
DL_DIRECTORY = os.path.join(UPLOAD_DIRECTORY, "DL")

# Create necessary directories
for directory in [UPLOAD_DIRECTORY, PROCESSED_DATA_DIRECTORY, PASSPORT_DIRECTORY, DL_DIRECTORY]:
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")

@app.get("/api/files/")
async def list_files():
    passport_files = os.listdir(PASSPORT_DIRECTORY)
    dl_files = os.listdir(DL_DIRECTORY)
    return passport_files + dl_files


@app.post("/api/upload/")
async def upload_document(
    file: UploadFile = File(...),
    documentType: str = Form(...)
):
    if documentType not in ["passport", "DL"]:
        raise HTTPException(status_code=400, detail="Invalid document type")

    # Choose the appropriate directory and extractor based on document type
    upload_dir = PASSPORT_DIRECTORY if documentType == "passport" else DL_DIRECTORY
    extractor = PassportExtractor() if documentType == "passport" else DLExtractor()
    
    try:
        # Save the uploaded file
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract data from the document
        extracted_data = extractor.extract(file_path)

        # Create JSON file name (same as image name but with .json extension)
        json_filename = os.path.splitext(file.filename)[0] + '.json'
        json_path = os.path.join(PROCESSED_DATA_DIRECTORY, json_filename)

        # Save extracted data as JSON
        with open(json_path, 'w') as json_file:
            json.dump({
                "filename": file.filename,
                "document_type": documentType,
                "extracted_data": extracted_data
            }, json_file, indent=2)

        return {
            "filename": file.filename,
            "documentType": documentType,
            "path": file_path,
            "extracted_data": extracted_data
        }

    except Exception as e:
        logging.error(f"Error processing document {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/verify/")
async def verify_all_documents():
    """Return all processed document data"""
    all_results = []
    
    try:
        # Read all JSON files from processed_data directory
        for filename in os.listdir(PROCESSED_DATA_DIRECTORY):
            if filename.endswith('.json'):
                file_path = os.path.join(PROCESSED_DATA_DIRECTORY, filename)
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    all_results.append(data)
        
        return all_results
    
    except Exception as e:
        logging.error(f"Error reading processed data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

