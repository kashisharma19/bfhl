from fastapi import FastAPI, UploadFile, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import base64
import os

app = FastAPI()

# POST request data model
class RequestModel(BaseModel):
    data: List[str]
    file_b64: Optional[str] = None


@app.post("/bfhl")
async def process_request(request: RequestModel):
    try:
        # Constants for the user
        user_id = "john_doe_17091999"
        email = "john@xyz.com"
        roll_number = "ABCD123"

        # Extract data arrays
        raw_data = request.data
        numbers = [x for x in raw_data if x.isdigit()]
        alphabets = [x for x in raw_data if x.isalpha()]
        highest_lowercase = max([x for x in raw_data if x.islower()], default="")

        # File handling
        file_valid, mime_type, file_size_kb = False, None, None
        if request.file_b64:
            try:
                decoded_file = base64.b64decode(request.file_b64)
                file_valid = True
                mime_type = "application/octet-stream"  # Default MIME type
                file_size_kb = len(decoded_file) / 1024
            except Exception:
                file_valid = False

        # Response
        return {
            "is_success": True,
            "user_id": user_id,
            "email": email,
            "roll_number": roll_number,
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_lowercase_alphabet": [highest_lowercase],
            "is_prime_found": prime_found,
            "file_valid": file_valid,
            "file_mime_type": mime_type,
            "file_size_kb": file_size_kb,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/bfhl")
async def get_operation_code():
    return {"operation_code": 1}




