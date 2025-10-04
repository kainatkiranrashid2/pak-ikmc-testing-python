from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import time
from process_image import *
from utils import extract_roll_number
from constants import *




app = FastAPI()


@app.post("/process-file/")
def process_file(file_path: str):
    """
    API endpoint to process a file given its absolute path.
    Verifies that the file exists and provides its metadata.
    """
    path = Path(file_path)
    print("Processing file : ", path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="File does not exist")
    elif not path.is_file():
        raise HTTPException(status_code=400, detail="The path is not a file")

    # Call extract_roll_number
    roll_number = extract_roll_number(file_path)
    print("Extracted roll number: ", roll_number)

    # Call process_image
    try:
        result = process_image_wt(file_path)
    except Exception as e:
        print(f"Exception occurred: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Image processing failed: {type(e).__name__}: {str(e)}")
        # return JSONResponse(content={"roll_number": roll_number, "result": ""})

    return JSONResponse(content={"roll_number": roll_number, "result": result})
