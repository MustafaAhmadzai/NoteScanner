from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
import uuid

from scanner_version2 import extract_text_from_image_google_vision, post_API, create_pdf  # Adjust as needed

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/process/")
async def process_image(file: UploadFile = File(...)):
    try:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = extract_text_from_image_google_vision(file_path)

        summarized_text = post_API(extracted_text)

        pdf_file_name = create_pdf(summarized_text)

        return {"summary": summarized_text, "pdf_file": pdf_file_name}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{pdf_file}")
def download_pdf(pdf_file: str):
    file_path = os.path.join(os.getcwd(), pdf_file)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, media_type='application/pdf', filename=pdf_file)
    raise HTTPException(status_code=404, detail="PDF not found")
